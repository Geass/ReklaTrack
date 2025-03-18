# **ReklaTrack – System Zarządzania Reklamacjami**

🚀 **ReklaTrack** to prosta aplikacja webowa napisana w **Flask + SQLite**, umożliwiająca śledzenie reklamacji klientów. Umożliwia dodawanie zgłoszeń, edytowanie, przeglądanie, zmienianie statusów oraz eksport do Excela.

## **🔧 Funkcje aplikacji:**

✅ **Dodawanie reklamacji** – klient, opis problemu, numer zamówienia, indeksy produktów  
✅ **Zarządzanie statusem reklamacji** – W oczekiwaniu, W trakcie, Zrealizowana, Odrzucona  
✅ **Automatyczna data realizacji** – ustawiana po oznaczeniu jako „Zrealizowana”  
✅ **Eksport do Excela** – możliwość pobrania listy reklamacji  
✅ **Podgląd reklamacji** – przeglądanie szczegółowych informacji bez edycji  
✅ **Edytowanie i usuwanie zgłoszeń** – możliwość aktualizacji lub ukrycia reklamacji  
✅ **Numery FedEx** – możliwość dodania więcej niż jednego numeru przesyłki  
✅ **Dane klienta** – imię, nazwisko, telefon, e-mail, notatki  

---

## **📚 Jak uruchomić projekt?**

### **1️⃣ Klonowanie repozytorium**
```bash
git clone https://github.com/Geass/ReklaTrack.git
cd ReklaTrack
```

### **2️⃣ Instalacja zależności**
```bash
pip install -r requirements.txt
```

### **3️⃣ Uruchomienie aplikacji**
```bash
python app.py
```
📄 **Aplikacja działa lokalnie pod adresem:**  
```
http://localhost:5000
```

Aby udostępnić ją w sieci lokalnej, otwórz:  
```
http://192.168.X.X:5000
```

---

## **📦 Wymagania**
- Python 3.x  
- Flask  
- Flask-SQLAlchemy  
- Pandas  
- OpenPyXL  

Zależności można zainstalować jednym poleceniem:
```bash
pip install flask flask-sqlalchemy pandas openpyxl
```

---

## **🖼️ Zrzuty ekranu **
![image](https://github.com/user-attachments/assets/6d4a3f43-4295-48f1-9538-36ef4e47dc7c)


---

## **🛠️ Planowane funkcje (TODO)**
- 🔄 Powiadomienia e-mail o zmianie statusu reklamacji  
- 📊 Dashboard ze statystykami reklamacji  
- 🍿️ Obsługa różnych metod dostawy (DHL, UPS, InPost)  

---

## **📜 Licencja**
Ten projekt jest dostępny na licencji **MIT** – możesz go używać i modyfikować do własnych potrzeb.  

---

🛠️ **Stworzona z myślą o wygodzie zarządzania reklamacjami!** 🚀
