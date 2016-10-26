from routes.common import *

@app.route('/')
@app.route('/store/')
def showStores():
	stores = session.query(Store).order_by(asc(Store.id))
	if 'username' not in login_session:
		state = makeState()
		return render_template('publicstores.html', stores=stores, state=state)
	else:
		return render_template('stores.html', stores=stores)

