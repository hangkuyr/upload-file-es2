from app import*
from db import*

@app.route('/search', methods=['GET', 'POST'])
def search():

	if request.method == 'GET':
		return render_template('search.html')

	else:
		d = request.form
		title = d['title']
		dbItems = db.findPublicDBItemsByTitle(title)
		if len(dbItems):
			return render_template('searchList.html', items=GetItems(dbItems))
		return render_template('noResult.html')