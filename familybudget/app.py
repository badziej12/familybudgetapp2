from api import app, db
from sqlalchemy.sql import text
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify, render_template, json, session, redirect, url_for
from api.queries import getCategory_resolver, listCategories_resolver, \
 listUsers_resolver, getUser_resolver, listTransactions_resolver, \
  getTransaction_resolver, getFamily_resolver, listFamilies_resolver, \
    getWallet_resolver, getGoal_resolver, listGoals_resolver, listWallets_resolver, listMembers_resolver, getMember_resolver
from api.mutations import create_user_resolver, update_user_resolver, delete_user_resolver, \
 new_transaction_resolver, create_family_resolver, delete_family_resolver, create_category_resolver, \
    create_goal_resolver, create_wallet_resolver, delete_category_resolver, delete_goal_resolver, update_wallet_resolver, \
        update_goal_resolver, delete_wallet_resolver, add_family_member_resolver, delete_family_member_resolver, delete_transaction_resolver
from datetime import date

query = ObjectType("Query")
mutation = ObjectType("Mutation")
query.set_field("listUsers", listUsers_resolver)
query.set_field("getUser", getUser_resolver)
query.set_field("listTransactions", listTransactions_resolver)
query.set_field("getTransaction", getTransaction_resolver)
query.set_field("listFamilies", listFamilies_resolver)
query.set_field("getFamily", getFamily_resolver)
query.set_field("getCategory", getCategory_resolver)
query.set_field("listCategories", listCategories_resolver)
query.set_field("getWallet", getWallet_resolver)
query.set_field("getGoal", getGoal_resolver)
query.set_field("listWallets", listWallets_resolver)
query.set_field("listGoals", listGoals_resolver)
query.set_field("listMembers", listMembers_resolver)
query.set_field("getMember", getMember_resolver)
mutation.set_field("createUser", create_user_resolver)
mutation.set_field("updateUser", update_user_resolver)
mutation.set_field("deleteUser", delete_user_resolver)
mutation.set_field("newTransaction", new_transaction_resolver)
mutation.set_field("createFamily", create_family_resolver)
mutation.set_field("deleteFamily", delete_family_resolver)
mutation.set_field("createCategory", create_category_resolver)
mutation.set_field("createGoal", create_goal_resolver)
mutation.set_field("createWallet", create_wallet_resolver)
mutation.set_field("deleteCategory", delete_category_resolver)
mutation.set_field("deleteGoal", delete_goal_resolver)
mutation.set_field("updateWallet", update_wallet_resolver)
mutation.set_field("updateGoal", update_goal_resolver)
mutation.set_field("deleteWallet", delete_wallet_resolver)
mutation.set_field("addFamilyMember", add_family_member_resolver)
mutation.set_field("deleteFamilyMember", delete_family_member_resolver)
mutation.set_field("deleteTransaction", delete_transaction_resolver)


app.secret_key = 'why would I tell you my secret key?'

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route('/')
def main():
    if session.get('user'):
        return redirect('/userHome')
    else:
        return redirect('/signin')

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route('/signup')
def showSignUp():
    return render_template('signup.html')

@app.route('/api/signup', methods=["POST"])
def signUp():
    _email = request.form['inputEmail']
    _name = request.form['inputName']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        create_user_resolver(None, None, _name,_email, _password)
        return redirect('/signin')
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/signin')
def showSignin():
    return render_template('signin.html')

@app.route('/api/validateLogin', methods=['POST'])
def validateLogin():
    try:
        __username = request.form['inputEmail']
        __password = request.form['inputPassword']
        
    
        user = listUsers_resolver(None, None)

        for id in range(len(user['users'])):
            if user['users'][id]['email'] == __username:
                if user['users'][id]['password'] == __password:
                    user['users'][id].pop("wallet")
                    user['users'][id].pop("families")
                    session['user'] = user['users'][id]
                    return redirect('/userHome')
                else:
                    return render_template('signin.html', error='Nieprawidłowy email lub hasło')
            
        return render_template('signin.html', error='Nieprawidłowy email lub hasło')

    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/userHome', methods=['GET', 'POST'])
def userHome():
    if session.get('user'):
        today = date.today()

        return redirect(url_for('showBudget', month = today.month))
    else:
        return redirect('/signin', error = 'Unauthorized Access')

@app.route('/wallet/<month>', methods=['GET', 'POST'])
def showBudget(month):
    try: 
        if session.get('user'):
            user = getUser_resolver(None, None, session['user']['id'])['user']

            months_dict = {"1": "Styczeń", "2": "Luty", "3": "Marzec", "4": "Kwiecień", "5": "Maj", "6": "Czerwiec",
                            "7": "Lipiec", "8": "Siepień", "9": "Wrzesień", "10": "Październik", "11": "Listopad", "12": "Grudzień"}

            selected_month = months_dict[str(month)]
            
            for wallet in user['wallet']:
                if int(wallet.month) == int(month):
                    current_wallet = wallet
                    break
            
            if 'current_wallet' not in locals():
                create_wallet_resolver(None, None, 0, month, session['user']['id'])
                user = getUser_resolver(None, None, session['user']['id'])['user']

            for wallet in user['wallet']:
                if int(wallet.month) == int(month):
                    current_wallet = wallet
                    break
            
            history = []
            goals = []
            donations = []

            for transaction in current_wallet.transaction:
                history_details = {'date': transaction.date, 'title': transaction.title, 'ammount': "{:,.2f}".format(transaction.ammount)}
                if transaction.goal_id != None:
                    goal_donation = {'id': transaction.goal_id, 'ammount': transaction.ammount}
                    donations.append(goal_donation)

                history.append(history_details)
            
            incoming = 0
            for goal in current_wallet.goals:
                to_pay = goal.price
                delta = goal.deadline - date.today()
                for donate in donations:
                    if donate['id'] == goal.id:
                        to_pay -= donate['ammount']
                incoming += to_pay
                goal_details = {'id': goal.id ,'title': goal.name, 'to_pay': "{:,.2f}".format(to_pay), 'price': "{:,.2f}".format(goal.price), 'lasts': delta.days}
                goals.append(goal_details)
            
            
            Nickname = user['nickname']
            Result = reversed(history)
            ammount = current_wallet.balance
            print(current_wallet.id)
            Balance = "{:,.2f}".format(ammount)
            Categories = []
            for category in listCategories_resolver(None,None)['category']:
                Categories.append(category['name'])

            return render_template('history.html', Balance = Balance, Nickname = Nickname, Result = Result, Goals = goals, Month = selected_month, Wallet_id = current_wallet.id,
                                    Categories = Categories, Incoming = "{:,.2f}".format(incoming))
        
        else:
            return redirect('/signin', error = 'Unauthorized Access')
    
    except Exception as e:
        return render_template("error.html", error = str(e))

@app.route('/api/newtransaction/<wallet_id>', methods=['POST'])
def newTransaction(wallet_id):
    try:
        __title = request.form['inputTitle']
        __ammount = int(request.form['inputAmmount'])
        wallet = getWallet_resolver(None, None, wallet_id)['wallet']
        
        if __ammount <= 0:
            session['error'] = "Plesase enter correct ammount!"
            session.modified = True
            return redirect(url_for('showBudget', month = wallet['month']))

        __category = request.form['inputCategory']
        print("wprowadzona kateogria" + __category)
        category_id = None

        categories = listCategories_resolver(None, None)
        for category in categories['category']:
            if category['name'] == __category:
                category_id = category['id']
        
        if category_id == None:
            session['error'] = "Category does not exist!"
            session.modified = True
            return redirect(url_for('showBudget', month = wallet['month']))

        new_transaction_resolver(None, None, __title, wallet_id, __ammount, category_id, None)

        return redirect(url_for('showBudget', month = wallet['month']))

    except ValueError:
        session['error'] = "Plesase enter correct ammount!"
        session.modified = True
        return redirect(url_for('showBudget', month = wallet['month']))
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/addBalance/<wallet_id>', methods=['POST'])
def addBalance(wallet_id):
    try:
        _ammount = float(request.form['inputBalance'])

        wallet = getWallet_resolver(None, None, wallet_id)['wallet']
        update_wallet_resolver(None, None, int(wallet_id), _ammount, None)

        return redirect(url_for('showBudget', month = wallet['month']))
    
    except ValueError:
        session['error'] = "Plesase enter correct ammount!"
        session.modified = True
        return redirect(url_for('showBudget', month = wallet['month']))
    
    except Exception as e:
        return render_template('error.html', error=str(e))  

@app.route('/profile')
def profile():
    if 'error' in session:
        error = session['error']
    else:
        error = ' '
    user = getUser_resolver(None, None, session['user']['id'])
    nickname = user['user']['nickname']
    user_families = []
    for family in user['user']['families']:
        user_families.append(family.family_id)

    
    families_data = {"id": [], "family_name": [], "members": []}
    
    i = 0
    for id in user_families:
        family = getFamily_resolver(None, None, id)
        families_data['family_name'].append(family['family']['name'])
        families_data['members'].append([user['user']['nickname']])
        members = []
        for member in family['family']['members']:
            members.append(int(member.user_id))
        
        for j in members:
            if j != int(session['user']['id']):
                member = getUser_resolver(None, None, j)
                families_data["members"][i].append(member['user']['nickname'])

        i += 1
    

    def eraseSession():
        if 'error' in session:
            session.pop('error', None)


    return render_template('profile.html', Nickname = nickname, Families_data = families_data, User_families = user_families, error = error), eraseSession()

@app.route('/profile/settings')
def change():
    
    user = getUser_resolver(None, None, session['user']['id'])
    nickname = user['user']['nickname']
    first_name = user['user']['first_name']
    last_name = user['user']['last_name']
    age = user['user']['age']
    email = user['user']['email']
    password = user['user']['password']
    
    if 'error' in session:
        error = session['error']
    else:
        error = ' '
    
    def eraseSession():
        if 'error' in session:
            session.pop('error', None)
    

    return render_template('profileChange.html',Nickname = nickname, Email = email, First_name = first_name,
    Last_name = last_name, Age = age, Password = password, error = error), eraseSession()

@app.route('/api/profileChange', methods=['POST'])
def profileChange():
    try:
        __username = request.form['inputUsername']
        __firstName = request.form['inputFirstName']
        __lastName = request.form['inputLastName']
        __age = request.form['inputAge']

        user = listUsers_resolver(None, None)
        
        for id in range(len(user['users'])):
            if user['users'][id]['nickname'] == __username and user['users'][id]['id'] != session['user']['id']:
                session['error'] = "Username already exist"
                session.modified = True
                return redirect('/profile/settings')

        conv = lambda i : i or None

        data = [__username, __age, __lastName, __firstName]
        
        res = [conv(i) for i in data]
                
        username = res[0]
        firstname = res[3]
        lastname = res[2]
        age = res[1]               
                
        update_user_resolver(None, None, session['user']['id'], username, None, None, firstname, lastname, age)
        
        return redirect('/profile')
            
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/family/<family_id>')
def familyShow(family_id):
    user = getUser_resolver(None, None, session['user']['id'])['user']    

    goals_data= {'id': [],'title': [], 'price': [], 'to_pay': [], 'lasts': []}
    members_names = []
    for family in user['families']:
        if int(family.family_id) == int(family_id):
            family_name = str(family.family.name)
            for member in family.family.members:
                members_names.append(str(member.user.nickname))
            for goal in family.family.goals:
                delta = goal.deadline - date.today()
                goals_data['id'].append(goal.id)
                goals_data['title'].append(goal.name)
                goals_data['lasts'].append(delta.days)
                goals_data['price'].append("{:,.2f}".format(goal.price))
                to_pay = goal.price / members_names.__len__()
                for wallet in user['wallet']:
                    for transaction in wallet.transaction:
                        if transaction.goal_id == goal.id:
                            to_pay -= transaction.ammount
                goals_data['to_pay'].append("{:,.2f}".format(to_pay))
    
    if 'error' in session:
        error = session['error']
    else:
        error = ' '
    
    def eraseSession():
        if 'error' in session:
            session.pop('error', None)

    Categories = []
    for category in listCategories_resolver(None,None)['category']:
        Categories.append(category['name'])

    return render_template("family.html", Goals = goals_data, Members = members_names, Name = family_name, Family_id = family_id, error = error, Categories = Categories), eraseSession()


@app.route('/api/createFamily', methods=['POST'])
def createFamily():
    try:
        _familyName = request.form['inputFamily']
        families = listFamilies_resolver(None, None)
        for family in families['families']:
            if family['name'] == _familyName:
                session['error'] = "Family name alredy exsist!"
                session.modified = True
                return redirect("/profile")
        
        create_family_resolver(None, None, _familyName, session['user']['id'])

        return redirect('/profile')
    
    except Exception as e:
        return render_template("error.html", error = str(e))

@app.route('/api/addMember/<family_id>', methods=['POST'])
def addMember(family_id):
    try:
        check_id = int(family_id)
        _memberName = request.form['inputMember']
        users = listUsers_resolver(None, None)
        for user in users['users']:
            print(user)
            print("id rodziny", check_id)
            if user['nickname'] == _memberName:
                print("nickname się zgadza")
                for family in user['families']:
                    print(family.family_id)
                    if int(family.family_id) == check_id:
                        print("Przeszło ifa")
                        session['error'] = "User is already in this family!"
                        session.modified = True
                        
                        return redirect(url_for('familyShow', family_id = check_id))
    
                add_family_member_resolver(None, None, user['id'], check_id)
                print("Przeszło elsa")
                return redirect(url_for('familyShow', family_id = check_id))

        session['error'] = "User does not exsist!"
        session.modified = True
        print("Przeszło całą funkcje")
        return redirect(url_for('familyShow', family_id = family_id))
    
    except Exception as e:
        return render_template("error.html", error = str(e))

@app.route('/api/addGoal/<id>', methods=['POST'])
def addGoal(id):
    try:
        check_id = int(id)
        _goalTitle = request.form['inputGoalTitle']
        _goalPrice = float(request.form['inputPrice'])
        _goalCategory = request.form['inputCategory']
        _goalDeadline = request.form['inputDeadline']

        categories = listCategories_resolver(None, None)
        for category in categories['category']:
            if category['name'] == _goalCategory:
                category_id = category['id']

        create_goal_resolver(None, None, _goalDeadline, _goalTitle, _goalPrice, None, check_id, category_id, None)

        return redirect('/userHome')

    except Exception as e:
        return render_template("error.html", error = str(e))

@app.route('/api/addFamilyGoal/<id>', methods=['POST'])
def addFamilyGoal(id):
    try:
        check_id = int(id)
        _goalTitle = request.form['inputGoalTitle']
        _goalPrice = float(request.form['inputPrice'])
        _goalCategory = request.form['inputCategory']
        _goalDeadline = request.form['inputDeadline']

        categories = listCategories_resolver(None, None)
        for category in categories['category']:
            if category['name'] == _goalCategory:
                category_id = category['id']

        create_goal_resolver(None, None, _goalDeadline, _goalTitle, _goalPrice, None, None, category_id, check_id)

        return redirect(url_for('familyShow', family_id = check_id))

    except Exception as e:
        return render_template("error.html", error = str(e))


@app.route('/api/goalTransaction/<id>', methods=['POST'])
def goalTransaction(id):
    try:
        print("Fukncja się zaczęła")

        check_id = int(id)
        _ammount = float(request.form["inputAmmount"])
        _goal_id = request.form["inputGoalID"]

        print("Wpłacono", _ammount, "PLN na rzecz rodziny o id: ", check_id, "na cel o id: ", _goal_id)

        user = getUser_resolver(None, None, session['user']['id'])['user']
        for wallet in user['wallet']:
            if wallet.id == check_id:
                month = wallet.month
                for goal in wallet.goals:
                    goal_name = str(goal.name)
                    goal_category = int(goal.category.id)
                    break

        new_transaction_resolver(None, None, goal_name, check_id, _ammount, goal_category, _goal_id)

        return redirect(url_for('showBudget', month = month))

    except Exception as e:
        return render_template("error.html", error = str(e))

@app.route('/api/familyGoalTransaction', methods=['POST'])
def familyGoalTransaction():
    try:
        print("Fukncja się zaczęła")

        _ammount = float(request.form["inputAmmount"])
        _goal_id = request.form["inputGoalID"]

        print("Wpłacono", _ammount, "na cel o id: ", _goal_id)

        user = getUser_resolver(None, None, session['user']['id'])['user']
        goal = getGoal_resolver(None, None, _goal_id)


        goal_month = goal['goal']['deadline']
    
        print(goal_month.month)

        goal_category = goal['goal']['category_id']
        goal_name = goal['goal']['name']

        for wallet in user['wallet']:
            if int(wallet.month) == int(goal_month.month):
                check_id = wallet.id
                break

        new_transaction_resolver(None, None, goal_name, int(check_id), _ammount, goal_category, _goal_id)

        return redirect('/userHome')

    except Exception as e:
        return render_template("error.html", error = str(e))

@app.route('/api/leaveFamily/<family_id>', methods=['POST'])
def leaveFamily(family_id):
    try:
        check_id = int(family_id)
        delete_family_member_resolver(None, None, session['user']['id'], check_id)
        family = getFamily_resolver(None, None, check_id)['family']
        if family['members'] == []:
            print("Rodzina była pusta!")
            delete_family_resolver(None, None, check_id)
        else:
            print ("W rodzinie są jeszce członkowie")
        return redirect('/profile')
    except Exception as e:
        return render_template("error.html", error = str(e))
