import os 
from dotenv import load_dotenv

from pathlib import Path
env_path = os.path.join('.', '.env')
load_dotenv(dotenv_path=env_path)

class Settings :
    
    PROJECT_NAME : str = "Ticky Ticket"
    PROJECT_VERSION : str = "1.0.0"
    
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD : str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB : str = os.getenv("POSTGRES_DB")
    
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    def print(self) :
        print(self.PROJECT_NAME)
        print(self.PROJECT_VERSION)
        print(self.POSTGRES_USER)
        print(self.POSTGRES_SERVER)
        print(self.POSTGRES_PORT)
        print(self.POSTGRES_DB)
        print(self.DATABASE_URL)
        
if __name__=="__main__" :
    s = Settings()
    s.print()