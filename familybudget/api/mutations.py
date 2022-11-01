from datetime import date
from multiprocessing.sharedctypes import Value
from unicodedata import category
from ariadne import convert_kwargs_to_snake_case
from api import db
from api.models import Categorires, Families, Transactions, Users
from psycopg2 import IntegrityError

@convert_kwargs_to_snake_case
def create_user_resolver(obj, info, nickname, email, password, first_name, last_name, age, balance):
    try:
        today = date.today()
        user = Users(
            nickname=nickname, first_name=first_name, email=email, password=password,
             last_name=last_name, age=age, balance=balance, created_at=today.strftime("%b-%d-%Y")
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
            "errors": ["Nickname {nickname} already exists"]
        } 

    return payload

@convert_kwargs_to_snake_case
def new_transaction_resolver(obj, info, title, recipient, recipient_id, sender, sender_id, ammount):
    try:
        today = date.today()
        transaction = Transactions(
            date = today.strftime("%b-%d-%Y"),
            title=title, recipient=recipient, recipient_id=recipient_id, sender=sender,
            sender_id=sender_id, ammount=ammount
        )
        decrease = 0 - ammount

        update_user_resolver(None, None, recipient_id, None, None, None, None, None, None, ammount)
        update_user_resolver(None, None, sender_id, None, None, None, None, None, None, decrease)
        
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
            "errors": ["Nickname {nickname} already exists"]
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
            "errors": ["Nickname {nickname} already exists"]
        }
    return payload

@convert_kwargs_to_snake_case
def create_category_resolver(obj, info, name):
    try:
        
        category = Categorires(
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
            "errors": ["Name {name} already exists"]
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
def update_user_resolver(obj, info, id, nickname, email, password, first_name, last_name, age, balance):
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
            if balance != None:
                user.balance += balance
        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "user": user.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
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