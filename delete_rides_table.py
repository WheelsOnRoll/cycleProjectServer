import sqlite3

db = sqlite3.connect("file::memory:?cache=shared",
                            check_same_thread=False)
cur = db.cursor()
cur.execute("delete from rides")
db.commit()
