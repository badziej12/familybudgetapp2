from datetime import date
from ariadne import convert_kwargs_to_snake_case
from api import db
from api.models import Families, Transactions, Users, Categories, Goals, Wallet
from psycopg2 import IntegrityError

@convert_kwargs_to_snake_case
def create_wallet_resolver(obj, info, balance):
    try:
        wallet = Wallet(balance=balance)
        db.session.add(wallet)
        db.session.commit()
        payload = {
            "success": True,
            "wallet": wallet.to_dict()
        }
    except IntegrityError:
        payload = {
            "success": False,
            "errors": ["Wallet {wallet.id} already exsist!"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_wallet_resolver(obj, info, id):
    try:
        wallet = Wallet.query.get(id)
        db.session.delete(wallet)
        db.session.commit()
        payload = {
            "success": True,
            "wallet": wallet.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Wallet with id {id} does not exsist!"]
        }
    return payload

@convert_kwargs_to_snake_case
def update_wallet_resolver(obj, info, id, balance):
    try:
        wallet = Wallet.query.get(id)
        wallet.balance += balance

        db.session.add(wallet)
        db.session.commit()
        payload = {
            "success": True,
            "wallet": wallet.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Wallet with id {id} not found."]
        }
    return payload

@convert_kwargs_to_snake_case
def create_goal_resolver(obj, info, name, price, category_id, family_id):
    try:
        goal = Goals(
            name=name, price=price, category_id=category_id, family_id=family_id
        )

        db.session.add(goal)
        db.session.commit()
        payload = {
            "success": True,
            "goal": goal.to_dict()
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def update_goal_resolver(obj, info, id, price):
    try:
        goal = Goals.query.get(id)

        goal.price += price

        db.session.add(goal)
        db.session.commit()
        payload = {
            "success": True,
            "goal": goal.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Goal with id {id} not found."]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_goal_resolver(obj, info, id):
    try:
        goal = Goals.query.get(id)

        db.session.delete(goal)
        db.session.commit()
        payload = {
            "success": True,
            "goal": goal.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Goal with id {id} not found."]
        }
    return payload


@convert_kwargs_to_snake_case
def create_user_resolver(obj, info, nickname, email, password, first_name, last_name, age, wallet_id):
    try:
        today = date.today()
        user = Users(
            nickname=nickname, first_name=first_name, email=email, password=password,
             last_name=last_name, age=age, wallet_id=wallet_id, created_at=today.strftime("%b-%d-%Y")
        )
        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "user": user.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    except IntegrityError:
        payload = {
            "success": False,
            "errors": ["Nickname {nickname} or email {email} already exists"]
        } 

    return payload

@convert_kwargs_to_snake_case
def new_transaction_resolver(obj, info, title, recipient_id, sender_id, ammount, category_id):
    try:
        today = date.today()
        transaction = Transactions(
            date = today.strftime("%b-%d-%Y"),
            title=title, recipient_id=recipient_id,
            sender_id=sender_id, ammount=ammount, category_id=category_id
        )
        decrease = 0 - ammount

        update_wallet_resolver(None, None, recipient_id, ammount)
        update_wallet_resolver(None, None, sender_id, decrease)
        
        db.session.add(transaction)
        db.session.commit()
        payload = {
            "success": True,
            "transaction": transaction.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    except IntegrityError:
        payload = {
            "success": False,
            "errors": ["Transaction {transaction.id} already exists"]
        } 

    return payload

@convert_kwargs_to_snake_case
def create_family_resolver(obj, info, name, member_id):
    try:
        
        family = Families(
            name = name
        )
        db.session.add(family)
        db.session.commit()
        member = Members(
            user_id = member_id,
            family_id = family.id
        )
        db.session.add(member)
        db.session.commit()
        payload = {
            "success": True,
            "family": family.to_dict()
        }
    except IntegrityError:
        payload = {
            "success": False,
            "errors": ["Family {family.id} already exists"]
        }
    return payload

@convert_kwargs_to_snake_case
def create_category_resolver(obj, info, name):
    try:
        
        category = Categories(
            name = name
        )
        db.session.add(category)
        db.session.commit()
        payload = {
            "success": True,
            "category": category.to_dict()
        }
    except IntegrityError:
        payload = {
            "success": False,
            "errors": ["Category {name} already exists"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_category_resolver(obj, info, id):
    try:
        
        category = Categories.query.get(id)
        db.session.delete(category)
        db.session.commit()
        payload = {
            "success": True,
            "category": category.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Category with id {id} does not exists"]
        }
    return payload


@convert_kwargs_to_snake_case
def add_family_member_resolver(obj, info, member_id, family_id):
    try:
        member = Members(
            user_id = member_id,
            family_id = family_id
        )
        db.session.add(member)
        db.session.commit()
        payload = {
            "success": True
        }
    except IntegrityError:
        payload = {
            "success": False,
            "errors": ["Member is wrong"]
        }
    return payload

@convert_kwargs_to_snake_case
def update_user_resolver(obj, info, id, nickname, email, password, first_name, last_name, age):
    try:
        user = Users.query.get(id)
        if user:
            if nickname != None:
                user.nickname = nickname
            if email != None:
                user.email = email
            if password != None:
                user.password = password
            if first_name != None:
                user.first_name = first_name
            if last_name != None:
                user.last_name = last_name
            if age != None:
                user.age = age
            
        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "user": user.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["Item matching id {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_user_resolver(obj, info, id):
    try:
        user = Users.query.get(id)
        db.session.delete(user)
        db.session.commit()
        payload = {"success": True, "user": user.to_dict()}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_family_resolver(obj, info, id):
    try:
        family = Families.query.get(id)
        db.session.delete(family)
        db.session.commit()
        payload = {"success": True, "family": family.to_dict()}
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }
    return payload