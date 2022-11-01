from app import db
from sqlalchemy.orm import relationship

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
    families = db.relationship(
        "Families", secondary=members_table, back_populates="members"
    )
    outcome = db.relationship("Transactions", backref="sender", lazy="dynamic",
     foreign_keys="Transactions.sender_id")
    income = db.relationship("Transactions", backref="recipient", lazy="dynamic",
     foreign_keys="Transactions.recipient_id")
    
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
            "created_at": str(self.created_at.strftime('%d-%m-%Y')),
            "income": self.income,
            "outcome": self.outcome
        }

class Transactions(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    title = db.Column(db.String)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ammount = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = relationship("Categories", back_populates="transaction")
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
            "category_id": self.category_id,
            "category": self.category
        }


class Families(db.Model):
    __tablename__ = "family"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"))

    goals = db.relationship("Goals", back_populates="family")
    members = db.relationship(
        "Users", secondary=members_table, back_populates="families"
    )
    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "goal_id": self.goal_id,
            "goals": self.goals,
            "members": self.members
        }

class Categories(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    transaction = db.relationship("Transactions", back_populates="category")
    goals = db.relationship("Goals", back_populates="category")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "transaction": self.transaction
        }

class Goals(db.Model):
    __tablename__ = "goal"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    category = db.relationship("Categories", back_populates="goals")
    family = db.relationship("Families", back_populates="goals")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category_id": self.category_id,
            "category": self.category,
            "family": self.family
        }