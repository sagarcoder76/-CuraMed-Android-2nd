import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.curamed.medicineassistant',
  appName: 'CuraMed',
  webDir: 'www',
  backgroundColor: '#f3faff',
  plugins: {
    LocalNotifications: {
      iconColor: '#005264'
    }
  }
};

export default config;
