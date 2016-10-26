from routes.common import *

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

