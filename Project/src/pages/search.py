from app import*
from db import*

@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'GET':
        return render_template('search.html')

    else:
    	d = request.form
    	title = d['title']
    	id = db.findFileByTitle(title)
    	if id is None:
    		return render_template('noResult.html')
    	else:
	    	resp = make_response(redirect('results/' + id))
	    	return resp