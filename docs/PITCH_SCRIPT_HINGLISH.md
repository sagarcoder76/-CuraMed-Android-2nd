# Judge ke saamne kya bolna hai — Hinglish pitch script

Total time: ~5 minute. Har slide ke saath jo lines bolni hain, wahi neeche hain.
Roman Hinglish me likha hai, kyunki bolne me easy lagta hai.

---

## 0. Opening — 20 second (slide 1 khulte hi)

> "Sir / Ma'am, ek chhoti si baat se shuru karta hoon.
> India me ghar me dawa ka patta English me chhote-chhote aksharon me likha hota hai.
> Maa-papa padh nahi paate. To wo padosi se poochhte hain — 'bukhar ke liye kaunsi goli?'
> Aur jawab milta hai jo kisi ke liye kaam kiya tha, aapke liye zaroori nahi.
>
> Humne **Medsathi** banaya — *all info in one app*.
> Teen sawaal, ek app me: **ye dawa kya hai? kya lena hai? aur kab lena hai?**"

Agar judge poochhe "kitna kaam hua?" — bolna: *"App chal raha hai, APK ready hai, aur live demo de sakta hoon."*

---

## 1. Problem — 45 second (slide 2)

> "Problem ek nahi, teen hain. Pehla — label English me, 6 point ke akshar me, Hindi bolne wale ke liye padhna mushkil.
> Doosra — salah WhatsApp group se aati hai, doctor se nahi. Wahan koi dose nahi poochhta.
> Teesra — doosri aur teesri dose yaad nahi rehti, kyunki reminder phone me hai hi nahi.
>
> Result ek line me: **galat dawa, galat dose, galat time.**"

Yahan rukna. Judges ko ye line yaad reh jaati hai.

---

## 2. Solution — 40 second (slide 3)

> "Humne teeno sawaal ek hi jagah rakhe, kyunki user teeno ek hi minute me poochhta hai.
> Ek — dawa ka naam likho ya camera se strip scan karo, poori jaankari mil jaati hai.
> Do — symptom bolo ya likho, *Hindi, Hinglish ya English* me, suggestion mil jaata hai.
> Teen — reminder set karo, alarm phone se aata hai, app band ho to bhi.
>
> Aur sabse important: **internet ke bina bhi chalta hai.** Net aaye to data aur fresh ho jaata hai."

---

## 3. Feature demo — 60 second (slide 4)

> "Ye main live dikha deta hoon."

Screen par ye kar dikhana (order yahi rakho):

1. Home screen — **crimson card** dikhao: *"Check my symptom"*
2. Chip dabao — **"Sar dard"** → result screen
3. Bol do: *"Yahan user ne sirf do tap kiye, kuch type nahi kiya. Answer ready."*
4. Result me dikhao: ghar par kya karein, kaunsi OTC dawa, **kab doctor ke paas jaana hai**, aur **buy link** (1mg, PharmEasy, Netmeds)

Bolna:

> "Dekhiye, humne dawa ka naam nahi chipkaya. Pehle batate hain ghar par kya karein, phir OTC option, phir *'doctor ke paas kab jaana hai'*. Aur har medicine ke saath buy link, taaki user search karne me na bhatke."

Scan dikhana ho to:

> "Camera strip par — text phone ke andar hi padha jaata hai, photo bahar nahi jaati."

---

## 4. Technical — 45 second (slide 5)

> "Tech simple aur sasta hai, kyunki hume trusted banana tha, cool nahi.
>
> App **Capacitor** par hai — matlab ek hi HTML/CSS/JS code, native Android app ke andar.
> Backend **Python** ka standard library — koi bhaari framework nahi, koi cloud database nahi.
> Jo cheezein offline chahiye — dawa ki library, symptom data — wo app ke andar bundled hain.
> AI wahan lagaya hai jahan matlab banta hai: scan ke liye on-device OCR (Latin + Devanagari), aur symptom samajhne ke liye optional API.
>
> Aur ek cheez jo judges ko pasand aati hai — **hamara build khud chalta hai.** GitHub par push karo, 4 minute me naya APK ban jaata hai. Isliye jo aap dekh rahe hain, wahi build aap install kar sakte hain."

Agar poochhe "API key?" →

> "Teen options hain. User apni key Profile me daal de — phone me hi rehti hai. Ya hum GitHub secrets se build ke andar inject karte hain. Public release ke liye proxy mode, taaki key client par na aaye."

---

## 5. Safety — 45 second (slide 6, sabse strong slide)

> "Ye slide meri favourite hai, kyunki health app me safety feature nahi, safety hi product hai.
>
> Pehli baat — **emergency guard.** 39 red-flag words hain: chest pain, saans lene me dikkat, behosh hona, lakwa, mirgi, khoon, zeher. Jis moment inme se koi aaya, app dawa suggest karna **band** kar deta hai aur sirf ek cheez bolta hai — **108 ya 112 par call karo.**
>
> Doosri baat — hum **diagnosis nahi karte.** Har screen par likha hai: ye general information hai, doctor ki salah nahi.
> Teesri — jitni dawaiyan prescription se aati hain, unpar hum dose nahi dete, likhte hain **'pharmacist se poochho.'**
> Chauti — user ka symptom, photo, history — sab **phone me hi** rehta hai. Koi account nahi, koi tracking nahi, kuch upload nahi hota.
> Aur paanchvi — source. WHO, NHS, National Health Portal India. Har result ke neeche source likha hota hai."

Judge ko yahan confident dikhna hai — ye wahi slide hai jahan aap jeette hain.

---

## 6. Status, impact, ask — 40 second (slide 7)

> "Aaj kya kaam kar raha hai: Android APK, GitHub se auto-build; symptom checker teen bhasha me; scan; offline search; reminder; history; dark mode; UI English, Hindi, Punjabi.
>
> Impact simple hai — **galat dawa kam, aur dose time par.**
> Aage kya: pehle launch par disclaimer accept karana, top 500 Indian brands ka verified data, aur symptom content ka **pharmacist review**, phir iOS.
>
> Aur humari ask chhoti hai: **ek clinic, 50 patients, ek pharmacist reviewer.**
> Isse pata chalega ki jo cheez screen par sahi lag rahi hai, kya wo asli ghar me bhi kaam karti hai.
>
> Medsathi — all info in one app. Thank you."

Bass. Yahan chup ho jao. Judge ko poochhne do.

---

## Q&A bank — jo 90% judges poochhte hain

**Q. Ye doctor ki jagah le raha hai?**
> "Nahi, sir. Hum dawa ka **suggestion** dete hain, **prescription** nahi likhte. Har result par 'doctor ki salah nahi' likha hai, aur serious symptoms me app dawa dena band kar deta hai — sirf hospital bhejta hai."

**Q. Galat suggestion de diya to?**
> "Do guard hain. Ek, hum sirf OTC aur common bimariyon tak limited hain — 15 conditions. Do, emergency me hum bold hi nahi dete. Aur aage pharmacist review karwa rahe hain, taaki content verify ho."

**Q. AI kahan use hua?**
> "Teen jagah. Scan me text padhne ke liye OCR, symptom ke shabdon ko samajhne ke liye normalisation, aur agar user ke paas key ho to Gemini se free-form symptom parse. Lekin app ka core AI ke bina bhi chalta hai — offline library se."

**Q. Data kahan jaata hai?**
> "Kahi nahi. Reminder, history, profile — sab `localStorage` me, user ke phone me. Koi login nahi, koi server database nahi. Photo phone ke andar padhi jaati hai."

**Q. Paisa kaise kamaoge?**
> "Abhi paisa target nahi hai. Buy links affiliate ki taraf le ja sakte hain, aur clinics ke liye adherence dashboard paid ho sakta hai. Lekin pehle trust — bina trust health app me monetisation ka matlab nahi."

**Q. Ye kitne logon ne use kiya?**
> "Abhi APK ready hai, pilot baaki hai — isliye aapke saamne ask rakha hai: ek clinic aur 50 patients. Main fake numbers nahi bataunga."

**Q. Isme naya kya hai? existing apps bhi hain?**
> "App store par medicine search hai, reminder apps hain. Lekin teen cheezein ek saath — symptom guidance Hinglish voice me, strip ka scan, aur reminder — kisi ek app me nahi milti. Aur jo sabse important hai: **emergency par rukna** — wo humne deliberately design kiya hai."

**Q. Team / time?**
> "Sach bataunga — code base kaafi bada hai, aur humne ise features ke hisaab se banaya, marketing ke hisaab se nahi." (apna real jawab daal lijiyega)

---

## Bolne ke rules

**Kar:**
- "Information, not diagnosis" — ye line har 2 minute me ek baar bolo
- Sankhya bolo: 15 conditions, 39 red flags, 3 bhasha, 4 minute build
- Live demo pehle, gyaan baad me
- Emergency guard ka demo/screenshot zaroor dikhao

**Mat kar:**
- "AI powered" ko headline mat banao — safety banao
- "Doctor replace" jaisa kuch mat bolo, ek baar bhi
- Jo nahi bana wo mat bolo (iOS, 500 brands — inko "next" hi rakho)
- Charts ya numbers invent mat karo — judges turant pakad lete hain
