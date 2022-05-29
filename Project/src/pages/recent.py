from app import*
from db import*

class RecentItem:
    def __init__(self, link, title, timestamp):
        self.link = link
        self.title = title
        self.timestamp = timestamp

def GetItems(dbItems):
    items = []
    for id, dbItem in dbItems:
        items.append(RecentItem(id, dbItem.title, TimestampToStr(dbItem.timestamp)))
    return items

@app.route('/recent', methods=['GET'])
def recentCallback():
    dbItems = db.getItemsSortedByDate(0, 10)
    return render_template('recent.html', items=GetItems(dbItems))