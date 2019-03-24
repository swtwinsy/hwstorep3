import string
import random
from database_setup import Base, Hardware_Category, Hardware_Item, User
import requests
from flask import make_response
import json
import httplib2
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from flask import session as login_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, asc
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash

app = Flask(__name__)


engine = create_engine('sqlite:///hardwarestorecatalogwithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Hardware Store Application"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# function to connect based on credentials passed from the login page
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        # print(response)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:'
    output += '150px;-webkit-border-radius: 150px;-moz-border-radius:'
    output += ' 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "success login!"
    return output


def createUser(login_session):
    url_picture = ('https://lh3.googleusercontent.com/G06Y0C1R5RuQJ_fYKl8qk5'
                   'WYPvl_hHbQgetP0GkCWvWB'
                   'gGCz3XULUoV13WbgG8OgDVHCp_4F8BLUNNHxKVwNVe7T1'
                   'DtPl80MFDI7yIxcg0P6ReSiDPQjW5ZJa'
                   'qNxYL1JhhiluiE-JdaUmGud2Q2IutK63A1GR9rPEiv3RWi41x_5Y6Kn'
                   'bPTIRru71N-'
                   'xVi9gI7iGBw3cuYves1H9S6-DGQJH7IEGiDxF9UUKXmcBoyxQI-'
                   'c7hcWZ18JLbIdICAqrWuoWTDFDjEgf3Dmk5oLCnntDor16kcSn3aRl4xk'
                   'Bpt8BC6MrJQ2tiQAwprH'
                   'XYUmKe0gG0VD6XsPiOWZeqhVHn84h0hWHg5BD7U3kdfppre6TKpPEWD1k'
                   'k11CkEr8UO8N50s3d2FW'
                   'iXfHyhud0-wIESCY7HN5F-AzI8OvYNia-NBRw104Pwo-'
                   'hQy6C74jObP5NePFkn8Yk6MYeuRiBFn47ZdkDC0IJ6VbdNndA0MFI4s4'
                   'l6J01fbi6uo0q4aX5l5a'
                   '3TlCFyf8PeBnqNhL8VZc89yGIkswEq52TemLh2kXaUEQ_hauWWkwcY61'
                   'pokePbd17ofP1nB6Ucj'
                   'D0P0myxHbhAmfiXP_G8hyP3tnUF4fX5zqNwt3vjdWthAdhiUIvL'
                   '5ZiYeBYfz0UaQ7boe4B8loa3'
                   'oPZmAtlgfc1OJMTep0Wl0hUAvUxeu7Sj3mkHG9vyZi0km1CWWgjne8i8'
                   '2zkez-rgc=w147'
                   '-h149-no')

    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=url_picture)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None

########


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':

        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps(
            'Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('showcategories'))
        flash('Successfully Disconnected')
        return response
    else:

        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Displaying all categories currently available for all register users
# that are for public view
@app.route('/')
@app.route('/categories/')
def showcategories():
    # query all hardware categories present
    categories = session.query(Hardware_Category).order_by(
        asc(Hardware_Category.name))
    # verify if the user has login
    if 'username' not in login_session:
        # if the user did not logs in then show all hardware
        # categories but do NOt allow to create a new one
        return render_template(
            'publicshowcategories.html', categories=categories)
    else:

        # if the user logs in then display all categories
        # and allow them to create a new categoery
        return render_template('showcategories.html', categories=categories)


#################################

# List all items included in this category
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/List/')
def showItems(category_id):
    hwcategory = session.query(
        Hardware_Category).filter_by(id=category_id).one()
    creator = getUserInfo(hwcategory.user_id)
    items = session.query(Hardware_Item).filter_by(
        categoryid=hwcategory.id).all()
    if ('username'not in login_session or
            creator.id != login_session['user_id']):
        return render_template(
            'publicshowitems.html', items=items,
            category=hwcategory, creator=creator)
    else:
        return render_template(
            'showItems.html', items=items,
            category=hwcategory, creator=creator)


#######################################
# Show item content
@app.route('/categories/item/<int:item_id>/')
def showItem(item_id):
    showitem = session.query(Hardware_Item).filter_by(id=item_id).one()
    hwcategory = session.query(Hardware_Category).filter_by(
        id=showitem.categoryid).one()
    creator = session.query(User).filter_by(id=showitem.user_id).one()
    if 'username' not in login_session:
        return render_template(
            'publicshowItem.html', item=showitem,
            category=hwcategory, creator=creator)
    if creator.id == login_session['user_id']:
        return render_template(
            'showItem.html', item=showitem,
            category=hwcategory, creator=creator)
    else:
        return render_template(
            'publicshowItem.html', item=showitem,
            category=hwcategory, creator=creator)


#######################################
# Show item public content
@app.route('/categories/item/<int:item_id>/')
def publicshowItem(item_id):
    pubshowitem = session.query(Hardware_Item).filter_by(id=item_id).one()
    pubhwcategory = session.query(Hardware_Category).filter_by(
        id=pubshowitem.categoryid).one()
    creator = session.query(User).filter_by(id=pubshowitem.user_id).one()
    if 'username' not in login_session:
        return redirect('/login')

    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        pubitems = session.query(Hardware_Item).filter_by(
            categoryid=pubhwcategory.id).all()
        return render_template(
            'showitems.html', items=pubitems,
            category=pubhwcategory, creator=creator)
    else:
        return render_template(
            'publicshowItem.html', item=pubshowitem,
            category=pubhwcategory, creator=creator)


#################################
@app.route('/categories/new/', methods=['GET', 'POST'])
def newhwcategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newhwcategory = Hardware_Category(
            name=request.form['name'],
            description=request.form['description'],
            user_id=login_session['user_id'])
        session.add(newhwcategory)
        flash('New Hardware Category %s Successfully Created' %
              newhwcategory.name)
        session.commit()
        return redirect(url_for('showcategories'))
    else:
        return render_template('newhwcategory.html')


# Edit a hardware category, you reach this page only if you are the
# one that created it
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def edithwcategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedcategory = session.query(
        Hardware_Category).filter_by(id=category_id).one()
    if editedcategory.user_id != login_session['user_id']:
        flash('You are not authorized to edit this Hardware Category.'
              'Please create your own Hardware Cateory in order to Edit.')
        return redirect(url_for('showcategories'))

    if request.method == 'POST':
        if request.form['name']:
            editedcategory.name = request.form['name']
        if request.form['description']:
            editedcategory.description = request.form['description']
        session.add(editedcategory)
        session.commit()
        flash('Hardware Category Successfully Edited %s' %
              editedcategory.name)
        return redirect(url_for('showcategories'))
    else:
        return render_template('edithwcategory.html', category=editedcategory)


###################################
# JSON APIs Category Info
@app.route('/categories/<int:category_id>/showItems/JSON')
def showItemsxcategoryJSON(category_id):
    # category = session.query(
    # Hardware_Category).filter_by(id=category_id).one()
    items = session.query(Hardware_Item).filter_by(
        categoryid=category_id).all()
    # CHECK THIS line add a break
    return jsonify(hwItems=[i.serialize for i in items])


######################################
# json object for an item within a category
@app.route('/categories/<int:category_id>/item/<int:item_id>/JSON')
def showItemInCategoryJSON(category_id, item_id):
    item = session.query(Hardware_Item).filter_by(
        id=item_id, categoryid=category_id).one()
    return jsonify(hwitem=item.serialize)


##################################################
# return all the categories in a json format
@app.route('/categories/JSON')
def showcategoriesJSON():
    categories = session.query(Hardware_Category).all()
    return jsonify(hwcategories=[c.serialize for c in categories])

#########################################


@app.route(
    '/categories/<int:category_id>/list/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    hwdcategory = session.query(
        Hardware_Category).filter_by(id=category_id).one()

    if hwdcategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('Your are not authorized"\
               " to delete this Hardware Category. Please create your own"\
               " Hardware Category in order to add a new hardware  item.');}"\
               "</script><body onload='myFunction()''>"

    if request.method == 'POST':
        newItem = Hardware_Item(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            categoryid=hwdcategory.id,
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New  Item %s  Successfully Created' % (newItem.name))
        return redirect(url_for('showItems', category_id=hwdcategory.id))
    else:
        return render_template('newhwItem.html', category_id=hwdcategory.id)


# Edit a hardware Item item
@app.route(
    '/categories/<int:category_id>/list/<int:item_id>/edit',
    methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Hardware_Item).filter_by(id=item_id).one()
    category = session.query(
        Hardware_Category).filter_by(id=category_id).one()

    if category.user_id != login_session['user_id']:
        return "<script>function myFunction()"
        "{alert('You are not authorized to edit Hardware Items "
        "under this Hardware Category. Please create your own "
        "Hardware Category in order to edit Hardware Items.');}"
        "</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']

        session.add(editedItem)
        session.commit()
        flash('Hardware Item Successfully Edited')
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template(
            'edithwItem.html', category_id=category_id, item=editedItem)


# Delete a hardware item
@app.route(
    '/categories/<int:category_id>/list/<int:item_id>/delete',
    methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    category = session.query(
        Hardware_Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Hardware_Item).filter_by(id=item_id).one()

    if 'username' not in login_session:
        return redirect('/login')

    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction()"
        " {alert('You are not authorized to delete hardware items"
        " under this Hardware Category. Please create your own "
        "hardware category in order to delete hardware items.');}"
        "</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Hardware Item Successfully Deleted')
        return redirect(url_for('showItems', category_id=category.id))
    else:
        return render_template(
            'deletehwItem.html', item=itemToDelete,
            category_id=category.id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
