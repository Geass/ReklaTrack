from flask import Flask, render_template, redirect, url_for, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reklamacje.db'
app.config['SECRET_KEY'] = 'Twoj_sekretny_klucz'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Baza danych reklamacji
class Reklamacja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tytul = db.Column(db.String(150), nullable=False)
    opis = db.Column(db.Text)
    numer = db.Column(db.String(50))
    indeksy = db.Column(db.Text)
    numery_fedex = db.Column(db.Text)
    status = db.Column(db.String(20), default='W oczekiwaniu')
    data_utworzenia = db.Column(db.DateTime, default=datetime.utcnow)
    data_realizacji = db.Column(db.DateTime)

    klient_imie = db.Column(db.String(50))
    klient_nazwisko = db.Column(db.String(50))
    klient_telefon = db.Column(db.String(20))
    klient_email = db.Column(db.String(100))
    notatki = db.Column(db.Text)

    def lista_indeksow(self):
        return json.loads(self.indeksy or '[]')

    def lista_fedex(self):
        return json.loads(self.numery_fedex or '[]')

# Baza użytkowników
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(256))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Błędne dane logowania')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Strona główna
@app.route('/')
@login_required
def index():
    reklamacje = Reklamacja.query.filter(Reklamacja.status != "Usunięta").order_by(Reklamacja.data_utworzenia.desc()).all()
    return render_template('index.html', reklamacje=reklamacje)

# Dodaj reklamację
@app.route('/dodaj', methods=['GET', 'POST'])
@login_required
def dodaj():
    if request.method == 'POST':
        reklamacja = Reklamacja(
            tytul=request.form['tytul'],
            opis=request.form['opis'],
            numer=request.form['numer'],
            indeksy=json.dumps(request.form.getlist('indeks[]')),
            numery_fedex=json.dumps(request.form.getlist('fedex[]')),
            klient_imie=request.form['klient_imie'],
            klient_nazwisko=request.form['klient_nazwisko'],
            klient_telefon=request.form['klient_telefon'],
            klient_email=request.form['klient_email'],
            notatki=request.form['notatki']
        )
        db.session.add(reklamacja)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('dodaj.html')

# Edytowanie
@app.route('/edytuj/<int:id>', methods=['GET', 'POST'])
@login_required
def edytuj(id):
    reklamacja = Reklamacja.query.get_or_404(id)
    if request.method == 'POST':
        reklamacja.tytul = request.form['tytul']
        reklamacja.opis = request.form['opis']
        reklamacja.numer = request.form['numer']
        reklamacja.indeksy = json.dumps(request.form.getlist('indeks[]'))
        reklamacja.numery_fedex = json.dumps(request.form.getlist('fedex[]'))
        reklamacja.klient_imie = request.form['klient_imie']
        reklamacja.klient_nazwisko = request.form['klient_nazwisko']
        reklamacja.klient_telefon = request.form['klient_telefon']
        reklamacja.klient_email = request.form['klient_email']
        reklamacja.notatki = request.form['notatki']
        reklamacja.status = request.form['status']
        reklamacja.data_realizacji = datetime.utcnow() if reklamacja.status == 'Zrealizowana' else None
        db.session.commit()
        return redirect(url_for('index'))

    reklamacja = Reklamacja.query.get_or_404(id)
    return render_template('edytuj.html', reklamacja=reklamacja)

# Podgląd
@app.route('/podglad/<int:id>')
@login_required
def podglad(id):
    reklamacja = Reklamacja.query.get_or_404(id)
    return render_template('podglad.html', reklamacja=reklamacja)

# Usuń (ustaw status)
@app.route('/usun/<int:id>')
@login_required
def usun(id):
    reklamacja = Reklamacja.query.get_or_404(id)
    reklamacja.status = "Usunięta"
    db.session.commit()
    return redirect(url_for('index'))

# Usuń trwale
@app.route('/usun_trwale/<int:id>')
@login_required
def usun_trwale(id):
    reklamacja = Reklamacja.query.get_or_404(id)
    db.session.delete(reklamacja)
    db.session.commit()
    return redirect(url_for('index'))

# Zmiana statusu
@app.route('/status/<int:id>/<string:status>')
@login_required
def zmien_status(id, status):
    reklamacja = Reklamacja.query.get_or_404(id)
    reklamacja.status = status
    if status == 'Zrealizowana':
        reklamacja.data_realizacji = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('index'))

# Eksport do Excel
@app.route('/export')
@login_required
def export():
    reklamacje = Reklamacja.query.all()
    df = pd.DataFrame([{
        'ID': r.id, 'Tytuł': r.tytul, 'Opis': r.opis,
        'Numer zamówienia': r.numer,
        'Imię': r.klient_imie, 'Nazwisko': r.klient_nazwisko,
        'Telefon': r.klient_telefon, 'Email': r.klient_email,
        'Indeksy': ", ".join(r.lista_indeksow()),
        'Numery FedEx': ", ".join(r.lista_fedex()),
        'Notatki': r.notatki, 'Status': r.status,
        'Zgłoszono': r.data_utworzenia.strftime('%Y-%m-%d'),
        'Zrealizowano': r.data_realizacji.strftime('%Y-%m-%d') if r.data_realizacji else ''
    } for r in Reklamacja.query.all()])
    filename = 'reklamacje.xlsx'
    df.to_excel(filename, index=False)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
