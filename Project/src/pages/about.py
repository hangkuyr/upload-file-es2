from app import*

@app.route('/about', methods=['GET'])
def aboutCallback():
    return render_template('about.html')