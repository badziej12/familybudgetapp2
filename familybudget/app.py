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
from datetime import date, datetime

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
        create_user_resolver(None, None, _name, _email, _password)
        return redirect('/signin')
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


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
        return render_template('error.html', error=str(e))


@app.route('/userHome', methods=['GET', 'POST'])
def userHome():
    if session.get('user'):
        today = date.today()

        return redirect(url_for('showBudget', month=today.month, year=today.year))
    else:
        return redirect('/signin', error='Unauthorized Access')


@app.route('/wallet/<month>+<year>', methods=['GET', 'POST'])
def showBudget(month, year):
    try:
        if session.get('user'):
            user = getUser_resolver(None, None, session['user']['id'])['user']

            months_dict = {"1": "Styczeń", "2": "Luty", "3": "Marzec", "4": "Kwiecień", "5": "Maj", "6": "Czerwiec",
                           "7": "Lipiec", "8": "Siepień", "9": "Wrzesień", "10": "Październik", "11": "Listopad", "12": "Grudzień"}

            selected_month = months_dict[str(month)]
            print(year)

            for wallet in user['wallet']:
                if int(wallet.month) == int(month) and int(wallet.year) == int(year):
                    current_wallet = wallet
                    break

            if 'current_wallet' not in locals():
                create_wallet_resolver(
                    None, None, 0, month, year, session['user']['id'])
                user = getUser_resolver(
                    None, None, session['user']['id'])['user']

            for wallet in user['wallet']:
                if int(wallet.month) == int(month) and int(wallet.year) == int(year):
                    current_wallet = wallet
                    break

            print(current_wallet)
            history = []
            goals = []
            donations = []

            for transaction in current_wallet.transaction:
                history_details = {'date': transaction.date, 'title': transaction.title,
                                   'ammount': "{:,.2f}".format(transaction.ammount)}
                if transaction.goal_id != None:
                    goal_donation = {'id': transaction.goal_id,
                                     'ammount': transaction.ammount}
                    donations.append(goal_donation)

                history.append(history_details)

            incoming = 0
            for goal in current_wallet.goals:
                if goal.paid == False:
                    to_pay = goal.price
                    delta = goal.deadline - date.today()
                    for donate in donations:
                        if donate['id'] == goal.id:
                            to_pay -= donate['ammount']
                    incoming += to_pay
                    goal_details = {'id': goal.id, 'title': goal.name, 'to_pay': "{:,.2f}".format(
                        to_pay), 'price': "{:,.2f}".format(goal.price), 'lasts': delta.days, 'description': goal.description}
                    goals.append(goal_details)

            Nickname = user['nickname']
            Result = reversed(history)
            ammount = current_wallet.balance
            print(current_wallet.id)
            Balance = "{:,.2f}".format(ammount)
            Categories = []

            errors = ['error1', 'error2', 'error3', 'error4']

            for error in errors:
                if error in session:
                    if error == 'error1':
                        error1 = session[error]
                        session.pop(error)
                        break
                    elif error == 'error2':
                        error2 = session[error]
                        session.pop(error)
                        break
                    elif error == 'error3':
                        error3 = session[error]
                        session.pop(error)
                        break
                    elif error == 'error4':
                        error4 = session[error]
                        session.pop(error)
                        break
                else:
                    error1 = ''
                    error2 = ''
                    error3 = ''
                    error4 = ''

            def eraseSession():
                for error in errors:
                    if error in session:
                        session.pop(error, None)

            for category in listCategories_resolver(None, None)['categories']:
                Categories.append(category['name'])

            return render_template('history.html', Balance=Balance, Nickname=Nickname, Result=Result, Goals=goals, Month=selected_month, MonthNumber=str(month), Year=str(year), Wallet_id=current_wallet.id,
                                   Categories=Categories, Incoming="{:,.2f}".format(incoming), error1=error1, error2=error2, error3=error3, error4=error4), eraseSession()

        else:
            return redirect('/signin', error='Nieautoryzowany dostęp!')

    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/api/newtransaction/<wallet_id>', methods=['POST'])
def newTransaction(wallet_id):
    try:
        __title = request.form['inputTitle']
        __ammount = int(request.form['inputAmmount'])
        wallet = getWallet_resolver(None, None, wallet_id)['wallet']

        if __ammount <= 0:
            session['error1'] = "Wprowadź poprawną kwotę!"
            session.modified = True
            return redirect(url_for('showBudget', month=wallet['month'], year=wallet['year']))

        __category = request.form['inputCategory']

        category_id = None

        categories = listCategories_resolver(None, None)
        for category in categories['categories']:
            if category['name'] == __category:
                category_id = category['id']

        if category_id == None:
            session['error1'] = "Kategoria nie istnieje!"
            session.modified = True
            return redirect(url_for('showBudget', month=wallet['month'], year=wallet['year']))

        new_transaction_resolver(
            None, None, __title, wallet_id, __ammount, category_id, None)

        return redirect(url_for('showBudget', month=wallet['month'],  year=wallet['year']))

    except ValueError:
        session['error1'] = "Wprowadź poprawną kwotę!"
        session.modified = True
        wallet = getWallet_resolver(None, None, wallet_id)['wallet']
        return redirect(url_for('showBudget', month=wallet['month'], year=wallet['year']))

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/api/addBalance/<wallet_id>', methods=['POST'])
def addBalance(wallet_id):
    try:
        _ammount = float(request.form['inputBalance'])

        wallet = getWallet_resolver(None, None, wallet_id)['wallet']
        update_wallet_resolver(None, None, int(
            wallet_id), _ammount, None, None)

        return redirect(url_for('showBudget', month=wallet['month'], year=wallet['year']))

    except ValueError:
        session['error2'] = "Wprowadź poprawną liczbę!"
        session.modified = True
        wallet = getWallet_resolver(None, None, wallet_id)['wallet']
        return redirect(url_for('showBudget', month=wallet['month'], year=wallet['year']))

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/profile')
def profile():
    if 'error' in session:
        error = session['error']
    else:
        error = ''
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

    return render_template('profile.html', Nickname=nickname, Families_data=families_data, User_families=user_families, error=error), eraseSession()


@app.route('/profile/settings')
def change():

    user = getUser_resolver(None, None, session['user']['id'])
    nickname = user['user']['nickname']
    email = user['user']['email']
    password = user['user']['password']

    if 'error' in session:
        error = session['error']
    else:
        error = ' '

    def eraseSession():
        if 'error' in session:
            session.pop('error', None)

    return render_template('profileChange.html', Nickname=nickname, Email=email, Password=password, error=error), eraseSession()


@app.route('/api/profileChange', methods=['POST'])
def profileChange():
    try:
        __username = request.form['inputUsername']

        user = listUsers_resolver(None, None)

        for id in range(len(user['users'])):
            if user['users'][id]['nickname'] == __username and user['users'][id]['id'] != session['user']['id']:
                session['error'] = "Nazwa użytkownika już istnieje!"
                session.modified = True
                return redirect('/profile/settings')

        username = str(__username)

        update_user_resolver(
            None, None, session['user']['id'], username, None, None)

        return redirect('/profile')

    except ValueError:
        session['error'] = "Wprowadź poprawną nazwę użytkownika!"
        session.modified = True
        return redirect('/profile/settings')

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/family/<family_id>')
def familyShow(family_id):
    user = getUser_resolver(None, None, session['user']['id'])['user']

    goals_data = {'id': [], 'title': [],
                  'price': [], 'to_pay': [], 'lasts': [], 'description': []}
    members_names = []
    for family in user['families']:
        if int(family.family_id) == int(family_id):
            family_name = str(family.family.name)
            for member in family.family.members:
                members_names.append(str(member.user.nickname))
            for goal in family.family.goals:
                if goal.paid == False:
                    delta = goal.deadline - date.today()
                    goals_data['id'].append(goal.id)
                    goals_data['title'].append(goal.name)
                    goals_data['lasts'].append(delta.days)
                    goals_data['description'].append(goal.description)
                    goals_data['price'].append("{:,.2f}".format(goal.price))
                    to_pay = goal.price / members_names.__len__()
                    for wallet in user['wallet']:
                        for transaction in wallet.transaction:
                            if transaction.goal_id == goal.id:
                                to_pay -= transaction.ammount
                    goals_data['to_pay'].append("{:,.2f}".format(to_pay))

    errors = ['error1', 'error2', 'error3']

    for error in errors:
        if error in session:
            if error == 'error1':
                error1 = session[error]
                error2 = ''
                error3 = ''
                session.pop(error)
                break
            elif error == 'error2':
                error2 = session[error]
                error1 = ''
                error3 = ''
                session.pop(error)
                break
            elif error == 'error3':
                error3 = session[error]
                error2 = ''
                error1 = ''
                session.pop(error)
                break
        else:
            error1 = ''
            error2 = ''
            error3 = ''

    def eraseSession():
        for error in errors:
            if error in session:
                session.pop(error, None)

    Categories = []
    for category in listCategories_resolver(None, None)['categories']:
        Categories.append(category['name'])

    return render_template("family.html", Goals=goals_data, Members=members_names, Name=family_name, Family_id=family_id, Categories=Categories, error1=error1, error2=error2, error3=error3), eraseSession()


@app.route('/api/createFamily', methods=['POST'])
def createFamily():
    try:
        _familyName = request.form['inputFamily']
        families = listFamilies_resolver(None, None)
        for family in families['families']:
            if family['name'] == _familyName:
                session['error3'] = "Rodzina już istnieje!"
                session.modified = True
                return redirect("/profile")

        create_family_resolver(None, None, _familyName, session['user']['id'])

        return redirect('/profile')

    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/api/addMember/<family_id>', methods=['POST'])
def addMember(family_id):
    try:
        check_id = int(family_id)
        _memberName = request.form['inputMember']
        users = listUsers_resolver(None, None)
        for user in users['users']:
            if user['nickname'] == _memberName:
                for family in user['families']:
                    if int(family.family_id) == check_id:
                        session['error1'] = "Użytkownik jest już w tej rodzinie!"
                        session.modified = True

                        return redirect(url_for('familyShow', family_id=check_id))

                add_family_member_resolver(None, None, user['id'], check_id)
                return redirect(url_for('familyShow', family_id=check_id))

        session['error1'] = "Użytkownik nie istnieje!"
        session.modified = True
        return redirect(url_for('familyShow', family_id=family_id))

    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/api/addGoal', methods=['POST'])
def addGoal():
    try:
        _goalTitle = request.form['inputGoalTitle']
        _goalPrice = float(request.form['inputPrice'])
        _goalCategory = request.form['inputCategory']
        _goalDeadline = request.form['inputDeadline']

        print(_goalDeadline, type(_goalDeadline))

        slicedDate = _goalDeadline.split("-")

        print(int(slicedDate[1]))

        user = getUser_resolver(None, None, session['user']['id'])['user']
        for wallet in user['wallet']:
            if int(wallet.month) == int(slicedDate[1]) and int(wallet.year) == int(slicedDate[0]):
                check_id = int(wallet.id)
                month = int(wallet.month)
                year = int(wallet.year)
                break

        if 'check_id' not in locals():
            wallet = create_wallet_resolver(
                None, None, 0, slicedDate[1], slicedDate[0], session['user']['id'])['wallet']
            print(wallet)
            check_id = int(wallet['id'])
            month = int(wallet['month'])
            year = int(wallet['year'])

        categories = listCategories_resolver(None, None)
        for category in categories['categories']:
            if category['name'] == _goalCategory:
                category_id = category['id']

        create_goal_resolver(None, None, _goalDeadline, _goalTitle,
                             _goalPrice, None, False, check_id, category_id, None)

        return redirect(url_for('showBudget', month=month, year=year))

    except ValueError:
        session['error3'] = "Wprowadź poprawną kwotę!"
        session.modified = True
        _goalDeadline = request.form['inputDeadline']
        slicedDate = _goalDeadline.split("-")
        user = getUser_resolver(None, None, session['user']['id'])['user']
        for wallet in user['wallet']:
            if int(wallet.month) == int(slicedDate[1]) and int(wallet.year) == int(slicedDate[0]):
                check_id = int(wallet.id)
                month = int(wallet.month)
                year = int(wallet.year)
                break

        return redirect(url_for('showBudget', month=month, year=year))

    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/api/addFamilyGoal/<id>', methods=['POST'])
def addFamilyGoal(id):
    try:
        check_id = int(id)
        _goalTitle = request.form['inputGoalTitle']
        _goalPrice = float(request.form['inputPrice'])
        _goalCategory = request.form['inputCategory']
        _goalDeadline = request.form['inputDeadline']

        categories = listCategories_resolver(None, None)
        for category in categories['categories']:
            if category['name'] == _goalCategory:
                category_id = category['id']

        create_goal_resolver(None, None, _goalDeadline, _goalTitle,
                             _goalPrice, None, False, None, category_id, check_id)

        return redirect(url_for('familyShow', family_id=check_id))

    except ValueError:
        session['error2'] = "Wprowadź poprawną kwotę!"
        session.modified = True
        check_id = int(id)
        return redirect(url_for('familyShow', family_id=check_id))

    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/api/goalTransaction/<id>', methods=['POST'])
def goalTransaction(id):
    try:
        check_id = int(id)
        _ammount = float(request.form["inputAmmount"])
        _goal_id = request.form["inputGoalID"]

        user = getUser_resolver(None, None, session['user']['id'])['user']
        for wallet in user['wallet']:
            if wallet.id == check_id:
                month = wallet.month
                year = wallet.year
                for goal in wallet.goals:
                    if goal.id == int(_goal_id):
                        goal_name = str(goal.name)
                        goal_category = int(goal.category.id)
                        goal_price = float(goal.price)
                        break
            if wallet.month == int(datetime.now().month) and wallet.year == int(datetime.now().year):
                wallet_id = wallet.id

        paid = 0
        for wallet in user['wallet']:
            for transaction in wallet.transaction:
                if transaction.goal_id == int(_goal_id):
                    paid += transaction.ammount
        if paid + _ammount >= goal_price:
            _ammount = goal_price - paid
            update_goal_resolver(None, None, int(
                _goal_id), None, None, None, None, True)

        new_transaction_resolver(
            None, None, goal_name, wallet_id, _ammount, goal_category, int(_goal_id))

        return redirect(url_for('showBudget', month=month, year=year))

    except ValueError:
        session['error4'] = 'Wprowadź poprawną kwotę!'
        session.modified = True
        user = getUser_resolver(None, None, session['user']['id'])['user']
        for wallet in user['wallet']:
            if wallet.id == check_id:
                month = wallet.month
                year = wallet.year

        return redirect(url_for('showBudget', month=month, year=year))
    except Exception as e:
        return render_template("error.html", error=str(e))


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
            if int(wallet.month) == int(goal_month.month) and int(wallet.year) == int(goal_month.year):
                check_id = wallet.id
                break

        new_transaction_resolver(None, None, goal_name, int(
            check_id), _ammount, goal_category, _goal_id)

        return redirect('/userHome')

    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/api/leaveFamily/<family_id>', methods=['POST'])
def leaveFamily(family_id):
    try:
        check_id = int(family_id)
        delete_family_member_resolver(
            None, None, session['user']['id'], check_id)
        family = getFamily_resolver(None, None, check_id)['family']
        if family['members'] == []:
            print("Rodzina była pusta!")
            delete_family_resolver(None, None, check_id)
        else:
            print("W rodzinie są jeszce członkowie")
        return redirect('/profile')
    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/dashboards', methods=['GET'])
def showDashboards():
    # try:
    user = getUser_resolver(None, None, session['user']['id'])['user']
    categories = listCategories_resolver(None, None)['categories']

    category_chart = {}
    category_chart_by_month = {}
    years = []

    planned_chart = {}
    planned_chart_by_month = {}

    months_names = {}

    months_dict = {"1": "Styczeń", "2": "Luty", "3": "Marzec", "4": "Kwiecień", "5": "Maj", "6": "Czerwiec",
                        "7": "Lipiec", "8": "Siepień", "9": "Wrzesień", "10": "Październik", "11": "Listopad", "12": "Grudzień"}

    for wallet in user['wallet']:
        if str(wallet.year) not in years:
            years.append(str(wallet.year))
            months_names[str(wallet.year)] = []

    print(years)

    for year in years:
        category_chart_by_month[year] = {}
        planned_chart_by_month[year] = {}

    print(category_chart_by_month)

    for year in category_chart_by_month:
        for month in months_dict:
            for wallet in user['wallet']:
                if wallet.month == int(month) and str(wallet.year) == year:
                    months_names[year].append(months_dict[month])
                    category_chart_by_month[year][months_dict[month]] = {}
                    planned_chart_by_month[year][months_dict[month]] = {}

    # for month in months_dict:
    #     for wallet in user['wallet']:
    #         if wallet.month == int(month):
    #             months_names.append(months_dict[month])
    #             category_chart_by_month[months_dict[month]] = {}
    #             planned_chart_by_month[months_dict[month]] = {}

    print(category_chart_by_month)
    print(planned_chart_by_month)

    for category in categories:
        category_chart[category['name']] = 0
        planned_chart[category['name']] = 0
        for year in category_chart_by_month:
            for month in category_chart_by_month[year]:
                category_chart_by_month[year][month][category['name']] = 0
                planned_chart_by_month[year][month][category['name']] = 0

    print(category_chart_by_month)
    print(planned_chart_by_month)

    for wallet in user['wallet']:
        for year in category_chart_by_month:
            for month in category_chart_by_month[year]:
                if months_dict[str(wallet.month)] == month and str(wallet.year) == year:

                    for transaction in wallet.transaction:
                        for category in category_chart_by_month[year][month]:
                            if transaction.category.name == category:
                                category_chart_by_month[year][month][category] += transaction.ammount

                    for goal in wallet.goals:
                        for category in planned_chart_by_month[year][month]:
                            if goal.category.name == category:
                                planned_chart_by_month[year][month][category] += goal.price

        # for chart in planned_chart_by_month:
        #     if months_dict[str(wallet.month)] == chart:
        #         for goal in wallet.goals:
        #             for category in planned_chart_by_month[chart]:
        #                 if goal.category.name == category:
        #                     planned_chart_by_month[chart][category] += goal.price

    print(category_chart_by_month)
    print(planned_chart_by_month)
    print(months_names)
    for wallet in user['wallet']:
        for goal in wallet.goals:
            for data in planned_chart:
                if str(goal.category.name) == data:
                    planned_chart[data] += goal.price
        for transaction in wallet.transaction:
            for data in category_chart:
                if str(transaction.category.name) == data:
                    category_chart[data] += transaction.ammount

    return render_template("dashboards.html", Category_chart=category_chart, Planned_chart=planned_chart, Chart_months=months_names, Category_chart_by_month=category_chart_by_month,
                           Planned_chart_by_month=planned_chart_by_month, Moje='hahah')

    # except Exception as e:
    #     return render_template("error.html", error=str(e))


@app.route('/api/updateDescription/<id>', methods=['POST'])
def updateDescription(id):
    try:
        check_id = int(id)
        __description = request.form['descriptionInput']
        __goalID = request.form['inputGoalID']

        user = getUser_resolver(None, None, session['user']['id'])['user']
        for wallet in user['wallet']:
            if wallet.id == check_id:
                month = wallet.month
                year = wallet.year
            for goal in wallet.goals:
                if goal.id == int(__goalID):
                    update_goal_resolver(None, None, int(
                        __goalID), None, None, None, __description, None)

        print(__description, type(__description))

        return redirect(url_for('showBudget', month=month, year=year))

    except Exception as e:
        return render_template("error.html", error=str(e))


@app.route('/api/updateFamilyDescription/<id>', methods=['POST'])
def updateFamilyDescription(id):
    try:
        check_id = int(id)
        __description = request.form['descriptionInput']
        __goalID = request.form['inputGoalID']

        print(__description)
        print(__goalID)

        family = getFamily_resolver(None, None, check_id)['family']
        for goal in family['goals']:
            if goal.id == int(__goalID):
                update_goal_resolver(None, None, int(
                    __goalID), None, None, None, __description, None)

        print(__description, type(__description))

        return redirect(url_for('familyShow', family_id=check_id))

    except Exception as e:
        return render_template("error.html", error=str(e))


if __name__ == '__main__':
    app.run()
