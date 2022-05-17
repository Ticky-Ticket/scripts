from config import Settings
import psycopg2


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
    
    def execute(self, query : str, *args) :
        self.connect()
        curr = self.conn.cursor()
        if len(args)==0 :
            curr.execute(query)     
        else : 
            curr.execute(query, args)
        self.conn.commit()
        self.conn.close()
    
    def fetch(self, query : str, *args) :
        self.connect()
        curr = self.conn.cursor()
        if len(args)==0 :
            curr.execute(query)     
        else : 
            curr.execute(query, args)
        try : 
            res = curr.fetchall()
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
        print("Hello")
    
    main()