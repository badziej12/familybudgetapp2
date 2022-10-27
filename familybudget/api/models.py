from app import db
from sqlalchemy.orm import declarative_base, relationship

members_table = db.Table(
    "members",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
    db.Column("family_id", db.ForeignKey("family.id"), primary_key=True)
)

class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    balance = db.Column(db.Float)
    created_at = db.Column(db.Date)
    families = relationship(
        "Families", secondary=members_table, back_populates="members"
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "balance": self.balance,
            "created_at": str(self.created_at.strftime('%d-%m-%Y'))
        }

class Transactions(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    title = db.Column(db.String)
    recipient = db.Column(db.String)
    sender = db.Column(db.String)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ammount = db.Column(db.Float)

    recipient_rel = relationship("Users", foreign_keys=[recipient_id])
    sender_rel = relationship("Users", foreign_keys=[sender_id])
    def to_dict(self):
        return {
            "id": self.id,
            "date": str(self.date.strftime('%d-%m-%Y')),
            "title": self.title,
            "recipient": self.recipient,
            "sender": self.sender,
            "recipient_id": self.recipient_id,
            "sender_id": self.sender_id,
            "ammount": self.ammount,
        }


class Families(db.Model):
    __tablename__ = "family"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    members = relationship(
        "Users", secondary=members_table, back_populates="families"
    )
    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name
        }


