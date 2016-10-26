from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from models.base import Base
from models.user import User
from models.store import Store
from models.product import Product

app = Flask(__name__)

CLIENT_ID = json.loads(
				open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "catalog"

engine = create_engine('sqlite:///productcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/store/')
def showStores():
	stores = session.query(Store).order_by(asc(Store.id))
	if 'username' not in login_session:
		return render_template('publicstores.html', stores=stores)
	else:
		return render_template('stores.html', stores=stores)

@app.route('/store/new/', methods=['GET', 'POST'])
def newStore():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newStore = Store(name=request.form['name'], 
						user_id=login_session['user_id'])
		session.add(newStore)
		flash('New Store %s Successully Created!' % newStore.name)
		session.commit()
		return redirect(url_for('showCatalog', store_id=newStore.id))
	else:
		return render_template('newstore.html')

@app.route('/store/<int:store_id>/edit/', methods=['GET', 'POST'])
def editStore(store_id):
	store = session.query(Store).filter_by(id=store_id).one()
	creator = getUserInfo(store.user_id)
	if 'username' not in login_session:
		return redirect('/login')
	elif creator.id != login_session['user_id']:
		flash("You don't have permission to edit this store.")
		return redirect(url_for('showCatalog', store_id=store_id))
	if request.method == 'POST':
		if request.form['name']:
			store.name = request.form['name']
			session.add(store)
			session.commit()
			flash('Store "%s" Succcessfully Edited' % store.name)
			return redirect(url_for('showCatalog', store_id=store_id))
	else:
		return render_template('editstore.html', store=store)

@app.route('/store/<int:store_id>/delete/', methods=['GET', 'POST'])
def deleteStore(store_id):
	store = session.query(Store).filter_by(id=store_id).one()
	creator = getUserInfo(store.user_id)
	if 'username' not in login_session:
		return redirect('/login')
	elif creator.id != login_session['user_id']:
		flash("You don't have permission to delete this store.")
		return redirect(url_for('showCatalog', store_id=store_id))
	if request.method == 'POST':
		session.delete(store)
		session.commit()
		flash('%s Successfully Deleted' % store.name)
		return redirect(url_for('showStores'))
	else:
		return render_template('deletestore.html', store=store)

@app.route('/store/<int:store_id>/')
@app.route('/store/<int:store_id>/catalog/')
@app.route('/store/<int:store_id>/catalog/<string:category>/')
def showCatalog(store_id, category=''):
	store = session.query(Store).filter_by(id=store_id).one()
	creator = getUserInfo(store.user_id)
	categories = session.query(Product).filter_by(
						store_id=store_id).group_by(Product.category).all()
	if category != '':
		products = session.query(Product).filter_by(
						store_id=store_id).filter_by(category=category).all()
		section_title = "%s Products" % (category, )
	else:
		products = session.query(Product).filter_by(
						store_id=store_id).order_by(Product.id.desc()).limit(10)
		section_title = "Latest Products"
	if 'username' not in login_session or (creator.id != 
													login_session['user_id']):
		return render_template('publiccatalog.html', store=store, 
													creator=creator, 
													categories=categories, 
													products=products, 
													section_title=section_title)
	else:
		return render_template('catalog.html', store=store, 
												creator=creator, 
												categories=categories, 
												products=products, 
												section_title=section_title)

@app.route('/store/<int:store_id>/catalog/<string:category>/<int:product_id>/')
def showProduct(store_id, category, product_id):
	store = session.query(Store).filter_by(id=store_id).one()
	creator = getUserInfo(store.user_id)
	categories = session.query(Product).filter_by(store_id=store_id).group_by(
														Product.category).all()
	product = session.query(Product).filter_by(id=product_id).one()
	if 'username' not in login_session or (creator.id != 
													login_session['user_id']):
		return render_template('publicproduct.html', store=store, 
													creator=creator, 
													categories=categories, 
													product=product)
	else:
		return render_template('product.html', store=store, 
												creator=creator, 
												categories=categories, 
												product=product)

@app.route('/store/<int:store_id>/catalog/new/', methods=['GET', 'POST'])
def newProduct(store_id):
	store = session.query(Store).filter_by(id=store_id).one()
	creator = getUserInfo(store.user_id)
	if 'username' not in login_session:
		return redirect('/login')
	elif creator.id != login_session['user_id']:
		flash("You don't have permission to add products in this store.")
		return redirect(url_for('showCatalog', store_id=store_id))
	if request.method == 'POST':
		newItem = Product(name=request.form['name'], 
							category=request.form['category'], 
							description=request.form['description'], 
							price=request.form['price'], 
							store_id=store_id, 
							user_id=login_session['user_id']
							)
		session.add(newItem)
		session.commit()
		flash('New Product "%s" Successfully Created' % (newItem.name, ))
		return redirect(url_for('showProduct', store_id=store_id, 
												category=newItem.category, 
												product_id=newItem.id))
	else:
		return render_template('newproduct.html', store_id=store_id)

@app.route('/store/<int:store_id>/catalog/<int:product_id>/edit/', 
			methods=['GET', 'POST'])
def editProduct(store_id, product_id):
	store = session.query(Store).filter_by(id=store_id).one()
	creator = getUserInfo(store.user_id)
	product = session.query(Product).filter_by(id=product_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	elif creator.id != login_session['user_id']:
		flash("You don't have permission to edit products in this store.")
		return redirect(url_for('showProduct', store_id=store_id, 
												category=product.category, 
												product_id=product.id))
	if request.method == 'POST':
		if request.form['name']:
			product.name = request.form['name']
		if request.form['category']:
			product.category = request.form['category']
		if request.form['description']:
			product.description = request.form['description']
		if request.form['price']:
			product.price = request.form['price']
		session.add(product)
		session.commit()
		flash('Product "%s" Successfully Edited' % (product.name, ))
		return redirect(url_for('showProduct', store_id=store_id, 
												category=product.category, 
												product_id=product.id))
	else:
		return render_template('editproduct.html', store_id=store_id, 
								product=product)

@app.route('/store/<int:store_id>/catalog/<int:product_id>/delete/', 
			methods=['GET', 'POST'])
def deleteProduct(store_id, product_id):
	store = session.query(Store).filter_by(id=store_id).one()
	creator = getUserInfo(store.user_id)
	product = session.query(Product).filter_by(id=product_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	elif creator.id != login_session['user_id']:
		flash("You don't have permission to delete products in this store.")
		return redirect(url_for('showProduct', store_id=store_id, 
												category=product.category, 
												product_id=product.id))
	if request.method == 'POST':
		session.delete(product)
		session.commit()
		flash('Product "%s" Successfully Deleted' % (product.name, ))
		return redirect(url_for('showCatalog', store_id=store_id))
	else:
		return render_template('deleteproduct.html', store_id=store_id, 
								product=product)

# JSON APIs to view Store and Product Information
@app.route('/store/JSON')
def storeJSON():
    stores = session.query(Store).all()
    return jsonify(stores=[s.serialize for s in stores])

@app.route('/store/<int:store_id>/catalog/JSON')
def catalogJSON(store_id):
    store = session.query(Store).filter_by(id=store_id).one()
    products = session.query(Product).filter_by(
        store_id=store_id).all()
    return jsonify(Product=[p.serialize for p in products])

@app.route('/store/<int:store_id>/catalog/<int:product_id>/JSON')
def productJSON(store_id, product_id):
    item = session.query(Product).filter_by(id=product_id).one()
    return jsonify(Product=item.serialize)

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Connect user with Google OAuth
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
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

    stored_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_token is not None and gplus_id == stored_gplus_id:
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
    login_session['email'] = data['email']

    # see if user exists, if it doesn't, create a new user
    user_id = getUserID(login_session['email'])
    if not user_id:
    	user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("You are now logged in as %s" % login_session['username'])
    # print "done!"
    print "User ID %s has logged in." % login_session['user_id']
    return output

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Disconnect - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    if access_token is None:
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' 
    											% login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
	del login_session['access_token'] 
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	# response = make_response(json.dumps('Successfully disconnected.'), 200)
    	# response.headers['Content-Type'] = 'application/json'
    	# return response
    	flash("Successfully logged out.")
    	return redirect(url_for('showStores'))
    else:
    	response = make_response(json.dumps(
    							'Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8000)
