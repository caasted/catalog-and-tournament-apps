from routes.common import *

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
