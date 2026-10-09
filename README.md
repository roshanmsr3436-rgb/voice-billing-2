# VoiceBill Tamil

AI Powered Voice POS System designed for Departmental Stores and Fruit & Vegetable shops.

## Features
- AI Voice Billing in Tamil, Tanglish and English
- PWA Support (Installable on Windows & Android)
- POS Dashboard
- Dynamic Stock Management
- Real Thermal Printer Service Integration

## How to Run

1. Open PowerShell and navigate to this folder:
```powershell
cd "c:\Users\Roshan R\OneDrive\Desktop\voice billing web\VoiceBill-Tamil"
```

2. Create a virtual environment and activate it:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install requirements:
```powershell
pip install -r requirements.txt
```

4. Run the application:
```powershell
python backend/app.py
```
This will automatically create the database, run the seed script, and start the server on `http://localhost:5000`.

5. Login:
- Username: `admin`
- Password: `admin123`

## Convert to App
- Open Chrome or Edge, go to `http://localhost:5000/login`
- Click the "Install App" icon in the address bar.
