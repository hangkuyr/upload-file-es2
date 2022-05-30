from app import*
from db import*

@app.route('/recent', methods=['GET'])
def recentCallback():
    dbItems = db.getItemsSortedByDate(0, 10)
    return render_template('recent.html', items=GetItems(dbItems))