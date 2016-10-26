from routes.common import *

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

