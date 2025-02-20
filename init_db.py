from app import create_app, db
from seed import seed_admin_user, insert_synthetic_data
app = create_app()


def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

        seed_admin_user()
        num_users = 100
        num_reports = 100
        insert_synthetic_data(num_users, num_reports)


init_db()
