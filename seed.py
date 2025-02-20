from app import db
from faker import Faker
from datetime import datetime
import random
from app.models import User, Report


def seed_admin_user():
    # Create an admin user
    email = "admin@thehexaa.com"
    password = "admin"
    admin_user = User(
        email=email,
        is_admin=True,
        email_verified=True
    )
    admin_user.set_password(password)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print('Superuser already exists!')
        return

    db.session.add(admin_user)
    db.session.commit()

    print('Admin user seeded successfully!')


def insert_synthetic_data(num_users, num_reports):
    faker = Faker()
    if 'en_US' in faker.locales:
        fake = Faker('en_US')
    else:
        # Handle the case where the locale is not available
        print("Locale 'en_US' is not available for this provider.")
    # Check if the 'user' table is empty
    if Report.query.count() > 0:
        print("Database tables already contain data. Skipping the seeding process.")
        return

    # Generate synthetic data for 'user' table
    user_ids = []
    for _ in range(num_users):
        email = faker.email()

        # Check if the email already exists
        while User.query.filter_by(email=email).first():
            email = faker.email()

        password = faker.password()
        is_admin = faker.boolean()
        email_verified = faker.boolean()

        user = User(
            email=email,
            is_admin=is_admin,
            email_verified=email_verified
        )
        user.set_password(password)

        db.session.add(user)
        db.session.flush()  # Flush to get the user ID
        user_ids.append(user.id)  # Store the user ID

    db.session.commit()

    # Generate synthetic data for 'report' table
    for _ in range(num_reports):
        date = faker.date_this_decade()
        tasks_completed = faker.text()
        challenges_faced = faker.text() if faker.boolean() else None
        hours_worked = round(random.uniform(1, 12), 2)
        additional_notes = faker.text() if faker.boolean() else None
        timestamp = datetime.now()
        # Assuming user IDs start from 1
        user_id = random.choice(user_ids)

        report = Report(
            date=date,
            tasks_completed=tasks_completed,
            challenges_faced=challenges_faced,
            hours_worked=hours_worked,
            additional_notes=additional_notes,
            timestamp=timestamp,
            user_id=user_id
        )

        db.session.add(report)

    db.session.commit()

    print(f" Inserted {num_users} rows into all tables.")
