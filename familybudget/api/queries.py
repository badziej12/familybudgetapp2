from .models import Families, Users, Transactions, Categories, Wallet, Goals, Members
from ariadne import convert_kwargs_to_snake_case

def listFamilyMembers_resolver(obj, info, id):
    try:
        members = [member.to_dict() for member in Members.query.all()]
        print(members)
        payload = {
            "success": True,
            "errors": [str(error)]
        }
        
    
    except Exception as error:
        payload = {
                "success": False,
                "errors": [str(error)]
        }
    return payload

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
            "families": families
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
            "categories": categories
        }
    except Exception as error:
        payload = {
                "success": False,
                "errors": [str(error)]
        }
    return payload
    

def listWallets_resolver(obj, info):
    try:
        wallets = [wallet.to_dict() for wallet in Wallet.query.all()]
        print(wallets)
        payload = {
            "success": True,
            "wallets": wallets
        }
    except Exception as error:
        payload = {
                "success": False,
                "errors": [str(error)]
        }
    return payload

def listGoals_resolver(obj, info):
    try:
        goals = [goal.to_dict() for goal in Goals.query.all()]
        print(goals)
        payload = {
            "success": True,
            "goals": goals
        }
    except Exception as error:
        payload = {
                "success": False,
                "errors": [str(error)]
        }
    return payload

def listMembers_resolver(obj, info):
    try:
        members = [member.to_dict() for member in Members.query.all()]
        print(members)
        
        payload = {
            "success": True,
            "members": members
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
        print(user)

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
def getMember_resolver(obj, info, user_id, family_id):
    try:
        member = Members.query.get([user_id, family_id])
        print(member.to_dict())

        payload = {
            "success": True,
            "member": member.to_dict()
        }
    except AttributeError: # todo not found
        payload = {
            "success": False,
            "errors": ["Member item matching {id} not found"]
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
            "errors": ["Family item matching {id} not found"]
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
            "errors": ["Category item matching {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def getWallet_resolver(obj, info, id):
    try:
        wallet = Wallet.query.get(id)
        payload = {
            "success": True,
            "wallet": wallet.to_dict()
        }
    except AttributeError: # todo not found
        payload = {
            "success": False,
            "errors": ["Wallet item matching {id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def getGoal_resolver(obj, info, id):
    try:
        goal = Goals.query.get(id)
        payload = {
            "success": True,
            "goal": goal.to_dict()
        }
    except AttributeError: # todo not found
        payload = {
            "success": False,
            "errors": ["Goal item matching {id} not found"]
        }
    return payload

