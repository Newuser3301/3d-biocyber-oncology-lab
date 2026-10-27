---
title: 3D Bio-Cyber Oncology Lab
emoji: 🧬
colorFrom: blue
colorTo: green
sdk: static
pinned: false
---

# 🧬 3D Bio-Cyber Oncology Lab // AI Diagnostic Core

UCI Machine Learning Repository'dagi **Breast Cancer Wisconsin (Diagnostic)** dataseti asosida **Decision Tree, K-Nearest Neighbors (KNN) va Random Forest** modellarining 3D fazodagi interaktiv vizualizatsiyasi va real-vaqtda qayta o'qitish (retraining) tizimi.

---

## ✨ Asosiy Imkoniyatlar

1. **Modelni Jonli Qayta O'qitish (Live Retraining):**
   * `train_test_split (Test ulushi)`: 10% dan 50% gacha. Test to'plami 3D fazoda wireframe halqalar bilan ajralib turadi.
   * `random_state (Seed)`: 🎲 Tasodifiy urug' tanlash va soniyaning ulushlarida barcha modellarni qayta o'qitish.
   * `max_depth`: Daraxt chuqurligini 1 dan 7 gacha sozlash.
   * `n_estimators`: Random Forest-dagi daraxtlar sonini 5 dan 25 gacha boshqarish.

2. **Qarorlar Daraxti uchun 3D Hologram Modellashtirish:**
   * 3D fazoda haqiqiy ierarxik shoxlangan kiber-daraxt (nodes, splitting rules, leaves).
   * `max_depth` o'zgarganda daraxt fazoda yangi shoxlar chiqarib o'sadi yoki qisqaradi.
   * Bemor ko'rsatkichlari bo'yicha ildizdan barggacha bo'lgan yo'l yorqin sariq lazer nuri bilan pulsatsiya qiladi.

3. **Random Forest uchun 3D Orbital Konstellatsiya:**
   * $N$ ta alohida daraxt markaziy **Aggregator Orb** atrofida 3D aylanma orbitada joylashgan kristallar ko'rinishida.
   * Har bir daraxt bemor tashxisi bo'yicha markazga qarab yashil (Benign) yoki qizil (Malignant) lazer nuri otadi.
   * Markaziy yadro barcha nurlarni yutib, ko'pchilik ovozini real vaqtda ko'rsatadi.

4. **3D Interaktiv Nuqtalar (Raycasting):**
   * Fazodagi istalgan hujayra biopsiyasini sichqoncha bilan bosish orqali zondni to'g'ridan-to'g'ri o'sha nuqtaga yo'naltirish mumkin.

---

## 🛠️ Lokal Ishga Tushirish

```bash
pip install -r requirements.txt
python app.py
```
Brauzerda: `http://localhost:5000`
