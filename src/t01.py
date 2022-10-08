from rethinkdb import RethinkDB
import shelve



def shelve2rethink():
    r = RethinkDB()
    db_file = f"/tmp/.files_db"
    db_file = '/mnt/5tb/Photovault/vault/.files_db'
    r.connect('localhost', 28015).repl()
    print("Connected")
    # r.db('test').table_create('vault').run()
    with shelve.open(db_file) as db:
        for k,v in db.items():
            r.table('vault').insert({'id':k,'p':v}).run()





if __name__ == '__main__':
    shelve2rethink()
