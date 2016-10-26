from routes.common import *

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

