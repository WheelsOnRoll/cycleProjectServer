import sqlite3

def execute_db(*args):
    db = sqlite3.connect("file::memory:?cache=shared")
    cur = db.cursor()
    try:
        with db:
            cur = db.cursor()
            # massage `args` as needed
            cur.execute(*args)
            db.commit()
            return True
    except Exception as why:
        print(why)
        return False

if __name__ == '__main__':
    bool1 = execute_db("create table name(name text)")
    bool2 = execute_db("insert into name values('Hello')")
    bool3 = execute_db("select * from name")

    print(bool1)
    print(bool2)
    print(bool3)