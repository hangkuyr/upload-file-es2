from app import*
from db import*

class RecentItem:
    def __init__(self, link, title, timestamp):
        self.link = link
        self.title = title
        self.timestamp = timestamp

@app.route('/uploads', methods=['GET'])
def uploads():
    items = []
    print('db',db.size(), len( db.getItemsSortedByDate(0, 10)))
    for id, dbItem in db.getItemsSortedByDate(0, 10):
        items.append(RecentItem(id, dbItem.title, TimestampToStr(dbItem.timestamp)))
    return render_template('uploadsList.html', items=items)