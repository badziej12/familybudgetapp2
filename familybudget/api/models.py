from app import db
from sqlalchemy.orm import relationship



class Members(db.Model):
    __tablename__ = "members"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), primary_key=True)
    user = db.relationship("Users", back_populates="families")
    family = db.relationship("Families", back_populates="members")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "family_id": self.family_id,
            "user": self.user,
            "family": self.family
        }


class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_at = db.Column(db.Date)

    wallet = db.relationship("Wallet", back_populates="user")
    families = db.relationship(
        "Members", back_populates="user"
    )
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "password": self.password,
            "wallet": self.wallet,
            "families": self.families,
            "created_at": str(self.created_at.strftime('%d-%m-%Y')),
            
        }

class Transactions(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    title = db.Column(db.String)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))
    ammount = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))

    wallet = db.relationship("Wallet", back_populates="transaction")
    goal = db.relationship("Goals", back_populates="transaction")
    category = relationship("Categories", back_populates="transaction")
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": str(self.date.strftime('%d-%m-%Y')),
            "title": self.title,
            "wallet_id": self.wallet_id,
            "ammount": self.ammount,
            "category_id": self.category_id,
            "goal_id": self.goal_id,
            "category": self.category,
            "goal": self.goal
        }

class Families(db.Model):
    __tablename__ = "family"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    goals = db.relationship("Goals", back_populates="family")
    members = db.relationship(
        "Members", back_populates="family"
    )
    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "goals": self.goals,
            "members": self.members,
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
            "transaction": self.transaction,
            "goals": self.goals
        }

class Goals(db.Model):
    __tablename__ = "goal"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date)
    deadline = db.Column(db.Date)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    family_id = db.Column(db.Integer, db.ForeignKey("family.id"))

    wallet = db.relationship("Wallet", back_populates="goals")
    category = db.relationship("Categories", back_populates="goals")
    family = db.relationship("Families", back_populates="goals")
    transaction = db.relationship("Transactions", back_populates="goal")

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "deadline": self.created_at,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "wallet_id": self.wallet_id,
            "wallet": self.wallet,
            "category_id": self.category_id,
            "category": self.category,
            "family_id": self.family_id,
            "family": self.family
        }

class Wallet(db.Model):
    __tablename__ = "wallet"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    month = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("Users", back_populates="wallet")
    transaction = db.relationship("Transactions", back_populates="wallet")
    goals = db.relationship("Goals", back_populates = "wallet")

    def to_dict(self):
        return {
            "id": self.id,
            "balance": self.balance,
            "month": self.month,
            "user_id": self.user_id,
            "user": self.user,
            "transaction": self.transaction
        }