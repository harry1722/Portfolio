from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Tabelat u krijuan me sukses.")
