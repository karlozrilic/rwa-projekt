# RWA - projekt

## Upute za instalaciju
1. Kloniraj repozitorij
2. Kreiraj virtualnu okolinu
3. Aktiviraj virtualnu okolinu naredbom venv\Scripts\activate
4. Instaliraj potrebne stvari pomoću requirements.txt datoteke naredbom pip install -r requirements.txt
5. Pokreni naredbom python app.py
6. U web browseru upiši localhost:5000
7. To je to!

## Sadržaj web aplikacije
- Admin i User login
- Admin može dodavati brisati i uređivati pizze u bazi podataka i izlistati sve Usere
- User može samo izlistavati sve pizze, ali tako da ne dobije sve informacije vezane uz pojedinačnu pizzu
- Uz to User može uređivati svoje ime i prezime u bazi podataka
- Aplikacija služi kao baza podataka svih pizza koje samo admin može izmjenjivat dok user može samo pretraživati iste
