from routes.common import *

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

