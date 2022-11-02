from .models import Families, Users, Transactions, Categories
from ariadne import convert_kwargs_to_snake_case

def listUsers_resolver(obj, info):
    try:
        users = [user.to_dict() for user in Users.query.all()]
        print(users)
        payload = {
            "success": True,
            "users": users
        }
    except Exception as error:
        payload = {
                "success": False,
                "errors": [str(error)]
        }
    return payload

def listTransactions_resolver(obj, info):
    try:
        transactions = [transaction.to_dict() for transaction in Transactions.query.all()]
        
        print(transactions)
        print(len(transactions))
        payload = {
            "success": True,
            "transactions": transactions
        }
    except Exception as error:
        payload = {
                "success": False,
                "errors": [str(error)]
        }
    return payload

def listFamilies_resolver(obj, info):
    try:
        families = [family.to_dict() for family in Families.query.all()]
        print(families)
        payload = {
            "success": True,
            "family": families
        }
    except Exception as error:
        payload = {
                "success": False,
                "errors": [str(error)]
        }
    return payload

def listCategories_resolver(obj, info):
    try:
        categories = [category.to_dict() for category in Categories.query.all()]
        print(categories)
        payload = {
            "success": True,
            "category": categories
        }
    except Exception as error:
        payload = {
                "success": False,
                "errors": [str(error)]
        }
    return payload
    


@convert_kwargs_to_snake_case
def getUser_resolver(obj, info, id):
    try:
        user = Users.query.get(id)
        user_transactions = []
        transactions = listTransactions_resolver(user, None)
        print(transactions)
        for transaction in transactions:
            if transaction.recipient_id == int(id) or transaction.sender_id == int(id):
                user_transactions.append(transaction)
        
        print(user.to_dict())
        userdict = user.to_dict()

        userdict.update({"transaction": user_transactions})
        

        payload = {
            "success": True,
            "user": user.to_dict()
        }
    except AttributeError: # todo not found
        payload = {
            "success": False,
            "errors": ["Users item matching {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def getTransaction_resolver(obj, info, id):
    try:
        transaction = Transactions.query.get(id)
        payload = {
            "success": True,
            "transaction": transaction.to_dict()
        }
    except AttributeError: # todo not found
        payload = {
            "success": False,
            "errors": ["Transaction item matching {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def getFamily_resolver(obj, info, id):
    try:
        family = Families.query.get(id)
        payload = {
            "success": True,
            "family": family.to_dict()
        }
    except AttributeError: # todo not found
        payload = {
            "success": False,
            "errors": ["Transaction item matching {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def getCategory_resolver(obj, info, id):
    try:
        category = Categories.query.get(id)
        payload = {
            "success": True,
            "category": category.to_dict()
        }
    except AttributeError: # todo not found
        payload = {
            "success": False,
            "errors": ["Transaction item matching {id} not found"]
        }
    return payload

