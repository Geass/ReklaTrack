from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    nowy_username = 'jrutkowski'
    nowy_password = 'BraniewoMebleOkmed'  # upewnij się, że ta zmienna jest zdefiniowana!

    user = User(
        username=nowy_username, 
        password=generate_password_hash(nowy_password, method='pbkdf2:sha256')
    )
    db.session.add(user)
    db.session.commit()

print("✅ Użytkownik dodany poprawnie!")
