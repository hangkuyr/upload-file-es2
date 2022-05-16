from app import*

@app.errorhandler(404)
def not_found(e):
    return render_template("NotFound.html")