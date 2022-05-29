from app import*
from db import*

app = CreateApp()
app.run(port=80, debug=True)
db.save(DB_FILE)