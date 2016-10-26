from routes.common import *

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

