"""Medicine Assistant web app using only Python standard library + existing modules."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json, sqlite3
from datetime import datetime

from database.database import get_connection, initialize_database, DB_PATH
from database.seed_data import seed_demo_data
from medicine.search import search_medicines

ROOT=Path(__file__).resolve().parent
HTML=(ROOT/'templates'/'index.html').read_text(encoding='utf-8')

def setup_db():
    conn=get_connection(DB_PATH); initialize_database(conn); seed_demo_data(conn)
    conn.execute('''CREATE TABLE IF NOT EXISTS reminders (
      id INTEGER PRIMARY KEY AUTOINCREMENT, medicine_name TEXT NOT NULL, dosage TEXT,
      reminder_time TEXT NOT NULL, repeat_type TEXT NOT NULL DEFAULT 'daily',
      enabled INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, last_taken TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS dose_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT, reminder_id INTEGER NOT NULL,
      action TEXT NOT NULL, action_time TEXT NOT NULL)''')
    conn.commit(); return conn

def send_json(h,data,status=200):
    raw=json.dumps(data,ensure_ascii=False).encode(); h.send_response(status); h.send_header('Content-Type','application/json; charset=utf-8'); h.send_header('Content-Length',str(len(raw))); h.end_headers(); h.wfile.write(raw)

def row(r): return dict(r) if r else None

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        u=urlparse(self.path); path=u.path
        if path=='/':
            raw=HTML.encode(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw); return
        conn=setup_db()
        try:
            if path=='/api/reminders': return send_json(self,[row(r) for r in conn.execute('SELECT * FROM reminders ORDER BY reminder_time')])
            if path=='/api/history': return send_json(self,[row(r) for r in conn.execute('SELECT d.*,r.medicine_name,r.dosage FROM dose_logs d JOIN reminders r ON r.id=d.reminder_id ORDER BY d.action_time DESC LIMIT 100')])
            if path=='/api/search':
                q=parse_qs(u.query).get('q',[''])[0].strip(); results=search_medicines(conn,q) if q else []
                return send_json(self,[{'id':m.medicine.id,'name':m.medicine.medicine_name,'generic':m.medicine.generic_name,'brand':m.medicine.brand_name,'strength':m.medicine.strength,'match_type':r.match_type} for r in results])
            if path.startswith('/api/medicine/'):
                mid=path.rsplit('/',1)[-1]; r=conn.execute('SELECT * FROM medicines WHERE id=?',(mid,)).fetchone()
                return send_json(self,row(r) or {'error':'Medicine not found'},200 if r else 404)
            return send_json(self,{'error':'Not found'},404)
        finally: conn.close()
    def body(self):
        n=int(self.headers.get('Content-Length','0')); return json.loads(self.rfile.read(n) or '{}')
    def do_POST(self):
        path=urlparse(self.path).path; data=self.body(); conn=setup_db()
        try:
            if path=='/api/reminders':
                med=str(data.get('medicine_name','')).strip(); t=str(data.get('reminder_time','')).strip(); dosage=str(data.get('dosage','')).strip(); rep=data.get('repeat_type','daily')
                if not med or not t: return send_json(self,{'error':'Medicine and time are required'},400)
                try: datetime.strptime(t,'%H:%M')
                except ValueError: return send_json(self,{'error':'Time must be HH:MM'},400)
                if rep not in ('daily','weekdays','once'): rep='daily'
                cur=conn.execute('INSERT INTO reminders(medicine_name,dosage,reminder_time,repeat_type,enabled,created_at) VALUES(?,?,?,?,1,?)',(med,dosage,t,rep,datetime.now().isoformat(timespec='seconds'))); conn.commit()
                return send_json(self,row(conn.execute('SELECT * FROM reminders WHERE id=?',(cur.lastrowid,)).fetchone()),201)
            if path.startswith('/api/reminders/') and path.endswith('/log'):
                rid=path.split('/')[-2]; action=data.get('action','taken')
                if action not in ('taken','skipped','snoozed'): return send_json(self,{'error':'Invalid action'},400)
                now=datetime.now().isoformat(timespec='seconds');
                if not conn.execute('SELECT 1 FROM reminders WHERE id=?',(rid,)).fetchone(): return send_json(self,{'error':'Reminder not found'},404)
                conn.execute('INSERT INTO dose_logs(reminder_id,action,action_time) VALUES(?,?,?)',(rid,action,now))
                if action=='taken': conn.execute('UPDATE reminders SET last_taken=? WHERE id=?',(now,rid))
                conn.commit(); return send_json(self,{'ok':True,'action':action,'action_time':now})
            return send_json(self,{'error':'Not found'},404)
        finally: conn.close()
    def do_PATCH(self):
        path=urlparse(self.path).path; data=self.body(); conn=setup_db()
        try:
            if path.startswith('/api/reminders/'):
                rid=path.rsplit('/',1)[-1]; fields=[]; vals=[]
                if 'enabled' in data: fields.append('enabled=?'); vals.append(1 if data['enabled'] else 0)
                if 'reminder_time' in data: fields.append('reminder_time=?'); vals.append(data['reminder_time'])
                if 'dosage' in data: fields.append('dosage=?'); vals.append(data['dosage'])
                if not fields:return send_json(self,{'error':'No changes'},400)
                vals.append(rid); conn.execute('UPDATE reminders SET '+','.join(fields)+' WHERE id=?',vals); conn.commit(); r=conn.execute('SELECT * FROM reminders WHERE id=?',(rid,)).fetchone(); return send_json(self,row(r) or {'error':'Reminder not found'},200 if r else 404)
            return send_json(self,{'error':'Not found'},404)
        finally: conn.close()
    def do_DELETE(self):
        path=urlparse(self.path).path; conn=setup_db()
        try:
            if path.startswith('/api/reminders/'):
                rid=path.rsplit('/',1)[-1]; conn.execute('DELETE FROM reminders WHERE id=?',(rid,)); conn.execute('DELETE FROM dose_logs WHERE reminder_id=?',(rid,)); conn.commit(); return send_json(self,{'ok':True})
            return send_json(self,{'error':'Not found'},404)
        finally: conn.close()

if __name__=='__main__':
    setup_db().close(); server=ThreadingHTTPServer(('0.0.0.0',5000),Handler); print('Medicine Assistant: http://127.0.0.1:5000'); server.serve_forever()
