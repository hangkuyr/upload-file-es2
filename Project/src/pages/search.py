from app import*

@app.route('/search')
def search():
    return render_template('search.html')
