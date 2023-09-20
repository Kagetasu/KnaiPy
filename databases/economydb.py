import sqlite3
db = './databases/economy.db'

with sqlite3.connect(db) as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS ECONOMY
                (ID INT PRIMARY KEY    NOT NULL,
                BALANCE    INT   NOT NULL);''')
    conn.commit()

def create(user_id: int, bal:int = 0):
    with sqlite3.connect(db) as conn:
        conn.execute("INSERT INTO ECONOMY (ID,BALANCE) VALUES (?, ?);", (user_id, bal))
        conn.commit()
    
    

def update(user_id: int, mode: str, amnt: int):
    check(user_id)
    with sqlite3.connect(db) as conn:
        if(mode == 'set'):
            conn.execute("UPDATE ECONOMY set BALANCE = ? where ID = ?;", (str(amnt), str(user_id)))
        else:
            currAmnt =  conn.execute("SELECT balance from ECONOMY where ID = ?", (str(user_id),)).fetchone()[0]
            if(mode == '+'):
                conn.execute("UPDATE ECONOMY set BALANCE = ? where ID = ?", (str(currAmnt+amnt), str(user_id)))
            elif(mode == '-'):
                conn.execute("UPDATE ECONOMY set BALANCE = ? where ID = ?", (str(currAmnt-amnt), str(user_id)))
        conn.commit()

def delete(user_id: int):
    with sqlite3.connect(db) as conn:
        conn.execute("DELETE from ECONOMY where ID = ?;", (str(user_id),))
        conn.commit()
    

def view(user_id: int):
    check(user_id)
    with sqlite3.connect(db) as conn:
        try:
            cursor = conn.execute("SELECT balance,locked from ECONOMY where ID = ?", (str(user_id),)).fetchone()
            return cursor
        except:
            raise
    
def check(user_id: int):
    with sqlite3.connect(db) as conn:
        cursor = conn.execute("SELECT balance from ECONOMY where ID = ?", (str(user_id),)).fetchone()
        if (cursor == None):
            create(user_id=user_id)
    

def lock(user_id: int, amnt: int):
    with sqlite3.connect(db) as conn:
        update(user_id, '-', amnt)
        locked = view(user_id)[1]
        conn.execute("UPDATE ECONOMY set LOCKED = ? where ID = ?", (str(locked+amnt), str(user_id)))

def unlock(user_id: int, amnt: int):
    with sqlite3.connect(db) as conn:
        update(user_id, '+', amnt)
        locked = view(user_id)[1]
        conn.execute("UPDATE ECONOMY set LOCKED = ? where ID = ?", (str(locked-amnt), str(user_id)))
    
    
    
