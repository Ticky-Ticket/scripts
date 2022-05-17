from config import Settings
import psycopg2
import psycopg2.extras
import pprint


class Database : 
    def __init__(self, s : Settings) :
        self.s = s
    
    def connect(self) :
        self.conn = psycopg2.connect(
            host = s.POSTGRES_SERVER, 
            database = s.POSTGRES_DB, 
            user = s.POSTGRES_USER, 
            password = s.POSTGRES_PASSWORD, 
            port = s.POSTGRES_PORT
        )
    
    def processor(self, res) : 
        l = []
        for i in res : 
            d = {}
            for j in i :
                d[j] = i.get(j)
            l.append(d)
        return l
    
    def execute(self, query : str, *args) :
        self.connect()
        curr = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        if len(args)==0 :
            curr.execute(query)     
        else : 
            curr.execute(query, args)
        self.conn.commit()
        self.conn.close()
    
    def fetch(self, query : str, *args) :
        self.connect()
        curr = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        if len(args)==0 :
            curr.execute(query)     
        else : 
            curr.execute(query, args)
        try : 
            res = curr.fetchall()
            res = self.processor(res)
        except Exception as e: 
            print(e)
            res = None
        self.conn.commit()
        self.conn.close()
        return res


if __name__=="__main__":
    s = Settings()
    
    def main() : 
        db = Database(s)
        
        db.execute("DROP TABLE IF EXISTS tickets")
        db.execute("DROP TABLE IF EXISTS roles")
        db.execute("DROP TABLE IF EXISTS history")
        
        db.execute('''CREATE TABLE tickets (
            id SERIAL,
            client INTEGER NOT NULL,
            asignee INTEGER NOT NULL ) ''')

        db.execute('''INSERT INTO tickets (client, asignee)
            VALUES (%s, %s)''', 1, 2)
        db.execute('''INSERT INTO tickets (client, asignee)
            VALUES (%s, %s)''', 2, 3)
        db.execute('''INSERT INTO tickets (client, asignee)
            VALUES (%s, %s)''', 1, 3)
        
        res = db.fetch("SELECT * from tickets")
        
        if res : 
            for r in res : 
                pprint.pprint(r)
        else : 
            print("No result returned") 
    main()