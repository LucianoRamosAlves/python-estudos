from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.couples import Couples
from datetime import date


app = create_app()

# with app.app_context():
#     db.create_all()

# with app.app_context():
    # user1 = User(
    #     first_name="Ana",
    #     last_name="Silva",
    #     email="ana.silva@example.com",
    #     password_hash="password123"
    # )

    # user2 = User(
    #     first_name="Pedro",
    #     last_name="Salos",
    #     email="pedro.salos@example.com",
    #     password_hash="password123"
    # )

    # db.session.add(user1)
    # db.session.add(user2)
    # db.session.commit()



# with app.app_context():
#     cuple1 = Couples(
#         user1_id=1,
#         user2_id=2,
#         relationship_date=date(2023,1,1),
#         relationship_status="Namorando",
#         couple_photo="couples/default.jpg"
#     )

#     db.session.add(cuple1)
#     db.session.commit()

# with app.app_context():
#     meus_users = User.query.all()
#     for user in meus_users:
#         print(f"ID: {user.id}, Nome: {user.first_name} {user.last_name}, Email: {user.email}")

# with app.app_context():
#     meus_users = Couples.query.all()
#     for user in meus_users:
#         print(f"ID: {user.id}, User1 ID: {user.user1_id}, User2 ID: {user.user2_id}, Relationship Date: {user.relationship_date}, Relationship Status: {user.relationship_status}, Couple Photo: {user.couple_photo}")


with app.app_context():
    meus_users = Couples.query.all()
    for user in meus_users:
        print(f"bem vindo o casal {user.user1.first_name} {user.user1.last_name} e {user.user2.first_name} {user.user2.last_name}, User1 ID: {user.user1_id}, User2 ID: {user.user2_id}, Relationship Date: {user.relationship_date}, Relationship Status: {user.relationship_status}, Couple Photo: {user.couple_photo}")
