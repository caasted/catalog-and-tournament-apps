from routes.common import *

@app.route('/store/<int:store_id>/catalog/<string:category>/<int:product_id>/')
def showProduct(store_id, category, product_id):
	store = session.query(Store).filter_by(id=store_id).one()
	creator = getUserInfo(store.user_id)
	categories = session.query(Product).filter_by(store_id=store_id).group_by(
														Product.category).all()
	product = session.query(Product).filter_by(id=product_id).one()
	if 'username' not in login_session or (creator.id != 
													login_session['user_id']):
		state = makeState()
		return render_template('publicproduct.html', store=store, 
													creator=creator, 
													categories=categories, 
													product=product, 
													state=state)
	else:
		return render_template('product.html', store=store, 
												creator=creator, 
												categories=categories, 
												product=product)

