from flask import Flask, request, redirect, render_template, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd, json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reklamacje.db'
db = SQLAlchemy(app)

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

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    reklamacje = Reklamacja.query.filter(Reklamacja.status != "Usunięta").order_by(Reklamacja.data_utworzenia.desc()).all()
    return render_template('index.html', reklamacje=reklamacje)

@app.route('/dodaj', methods=['GET', 'POST'])
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

@app.route('/edytuj/<int:id>', methods=['GET', 'POST'])
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
    return render_template('edytuj.html', reklamacja=reklamacja)

@app.route('/podglad/<int:id>')
def podglad(id):
    reklamacja = Reklamacja.query.get_or_404(id)
    return render_template('podglad.html', reklamacja=reklamacja)

@app.route('/usun/<int:id>')
def usun(id):
    reklamacja = Reklamacja.query.get_or_404(id)
    reklamacja.status = "Usunięta"
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/usun_trwale/<int:id>')
def usun_trwale(id):
    reklamacja = Reklamacja.query.get_or_404(id)
    db.session.delete(reklamacja)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/status/<int:id>/<string:status>')
def zmien_status(id, status):
    reklamacja = Reklamacja.query.get_or_404(id)
    if status in ['W oczekiwaniu', 'W trakcie', 'Zrealizowana', 'Odrzucona']:
        reklamacja.status = status
        reklamacja.data_realizacji = datetime.utcnow() if status == 'Zrealizowana' else None
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/export')
def export():
    reklamacje = Reklamacja.query.all()
    df = pd.DataFrame([{
        'ID': r.id,
        'Tytuł': r.tytul,
        'Opis': r.opis,
        'Numer zamówienia': r.numer,
        'Indeksy produktów': ', '.join(r.lista_indeksow()),
        'Numery FedEx': ", ".join(r.lista_fedex()),
        'Imię klienta': r.klient_imie,
        'Nazwisko klienta': r.klient_nazwisko,
        'Telefon klienta': r.klient_telefon,
        'Email klienta': r.klient_email,
        'Notatki': r.notatki,
        'Status': r.status,
        'Data utworzenia': r.data_utworzenia.strftime('%Y-%m-%d %H:%M'),
        'Data realizacji': r.data_realizacji.strftime('%Y-%m-%d %H:%M') if r.data_realizacji else ''
    } for r in reklamacje])

    filename = 'reklamacje.xlsx'
    df.to_excel(filename, index=False)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
