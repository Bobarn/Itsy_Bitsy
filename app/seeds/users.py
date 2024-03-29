from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text
from faker import Faker

f = Faker(locale='en_US')
# Adds a demo user, you can add other users here if you want
def seed_users():
    demo = User(
        username='Demo', email='demo@aa.io', password='password', first_name='Demo', last_name='Lition')
    marnie = User(
        username='marnie', email='marnie@aa.io', password='password', first_name='Marnie', last_name='Halloween')
    bobbie = User(
        username='bobbie', email='bobbie@aa.io', password='password', first_name='Bobbie', last_name='Builder')

    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
    newUsers = []

    for i in range(7):
        newUser = User(
            username=f.user_name(),
            first_name=f.first_name(),
            last_name=f.last_name(),
            email=f.email(),
            password=f.password()
        )
        newUsers.append(newUser)
    db.session.add_all(newUsers)

    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
