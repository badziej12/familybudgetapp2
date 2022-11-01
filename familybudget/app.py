
from api import app, db
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify, render_template, json, session, redirect
from api.queries import getCategory_resolver, listCategories_resolver, listUsers_resolver, getUser_resolver, listTransactions_resolver, getTransaction_resolver, getFamily_resolver, listFamilies_resolver
from api.mutations import create_user_resolver, update_user_resolver, delete_user_resolver, new_transaction_resolver, create_family_resolver, delete_family_resolver

query = ObjectType("Query")
mutation = ObjectType("Mutation")
query.set_field("listUsers", listUsers_resolver)
query.set_field("getUser", getUser_resolver)
query.set_field("listTransactions", listTransactions_resolver)
query.set_field("getTransaction", getTransaction_resolver)
query.set_field("listFamilies", listFamilies_resolver)
query.set_field("getFamily", getFamily_resolver)
query.set_field("listCategories", listCategories_resolver)
query.set_field("getCategory", getCategory_resolver)
mutation.set_field("createUser", create_user_resolver)
mutation.set_field("updateUser", update_user_resolver)
mutation.set_field("deleteUser", delete_user_resolver)
mutation.set_field("newTransaction", new_transaction_resolver)
mutation.set_field("createFamily", create_family_resolver)
mutation.set_field("deleteFamily", delete_family_resolver)

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
        create_user_resolver(None, None, _name,_email, _password, None, None, None, 0)
        return json.dumps({'html':'<span>All fields good !!</span>'})
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
                    session['user'] = user['users'][id]
                    return redirect('/userHome')
                else:
                    return render_template('signin.html', error='Invalid email or password')

    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/userHome', methods=['GET', 'POST'])
def userHome():
    if session.get('user'):
        transactions = listTransactions_resolver(None, None)
        Result = reversed(transactions['transactions'])
        ammount = session['user']['balance']
        Balance = "{:,.2f}".format(ammount)
        return render_template('profile.html', Result=Result, Balance=Balance)
    else:
        return redirect('/signin', error = 'Unauthorized Access')

@app.route('/profile')
def profile():
    email = session['user']['email']
    first_name = session['user']['first_name']
    last_name = session['user']['last_name']
    age = session['user']['age']
    nickname = session['user']['nickname']
    password = session['user']['password']
    

    return render_template('profile.html', Nickname = nickname, Email = email, First_name = first_name,
    Last_name = last_name, Age = age, Password = password)

@app.route('/profile/change')
def change():
    
    email = session['user']['email']
    first_name = session['user']['first_name']
    last_name = session['user']['last_name']
    age = session['user']['age']
    nickname = session['user']['nickname']
    password = session['user']['password']
    
    if 'error' in session:
        error = session['error']
    else:
        error = ' '
    
    def eraseSession():
        if 'error' in session:
            session.pop('error', None)
    

    return render_template('profile_change.html',Nickname = nickname, Email = email, First_name = first_name,
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
                return redirect('/profile/change')
                
        
        update_user_resolver(None, None, session['user']['id'], __username, None, None, __firstName, __lastName, __age, None)
        session['user']['nickname'] = __username
        session['user']['first_name'] = __firstName
        session['user']['last_name'] = __lastName
        session['user']['age'] = __age
        session.modified = True
        
                
        return redirect('/profile')
            
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/families')
def families():

    families = listFamilies_resolver(None, None)
    family_name = []
    
    for id in range(len(families['families'])):
        family_name.append(families['families'][id]['name'])

    print(family_name)
    
    
    

    return render_template('families.html', family_name = family_name)

@app.route('/families/create')
def families_create():
    

    return render_template('families_create.html')

@app.route('/api/familyCreate', methods=['POST'])
def familyCreate():
    try:
        __familyname = request.form['family_name']

        create_family_resolver(None, None, __familyname)
        

        return redirect('/families')

    except Exception as e:
        return render_template('error.html', error = str(e))
    