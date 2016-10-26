from routes.common import *

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
		state = makeState()
		return render_template('publiccatalog.html', store=store, 
													creator=creator, 
													categories=categories, 
													products=products, 
													section_title=section_title, 
													state=state)
	else:
		return render_template('catalog.html', store=store, 
												creator=creator, 
												categories=categories, 
												products=products, 
												section_title=section_title)

