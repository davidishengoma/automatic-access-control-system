
import json

from settings import BASE_DIR

def fsdb_logger(level, msg):
    # logging function
    print(f"fsdb: {level} msg: {msg}")
    

def create_db():
    # creating the databse
    with open("db.json","w") as db:
        db.close()
        
    # initializing the database
    with open(BASE_DIR / "db.json","r+") as db:
        # check if the db is empty
        if db.read() == "":
            json.dump([], db)
        db.close()
        
        
def read_data() -> list:
    data = []
    
    try:
        with open("db.json", "r") as db:
            data = json.load(db)
            # print("data --> ", data)
            db.close()    
    except FileNotFoundError as e:
        fsdb_logger(f"{e}", "Database not created")
        fsdb_logger(f"Info", "Creating database")
        create_db()
        
    return data 
       

def data_exists(data, ls):
    x = [i for i in ls if i["name"] == data["name"]]
    if x != []:
        return True
    return False

def enter_data(name: str):
    
    entry = {
            "name": name
        }
        
    ind = 0
    
    try:
        current = read_data()
        ind = len(current) 
    except json.JSONDecodeError as e:
        fsdb_logger(f"{e}", "Creating new db file")
        create_db()
        current = read_data()
        ind = len(current)
        
        
    if data_exists(entry, current):
        fsdb_logger("Error", "Data already exists")
        return None
    
    
    with open("db.json", "w") as db:
        entry["id"] = ind + 1
        current.append(entry)
        json.dump(current, db)
        fsdb_logger("Successs","Data entry done")


def delete_data(id: int):
    
    try:
        current = read_data()
        for entry in current:
            if data_exists(entry, current) and entry["id"] == int(id):
                current.remove(entry)
                
        with open("db.json", "w") as db:
            json.dump(current, db)
            fsdb_logger("Successs","Data entry done")
            
    except json.JSONDecodeError as e:
        fsdb_logger(f"{e}", "Creating new db file")
        create_db()
        current = read_data()
        ind = len(current)
                 
class Data:
    
    def __init__(self, name, id=None) -> None:
        self.id = id
        self.name = name
        
    def save(self):
        enter_data(self.name)


def get_by_id(id: int) -> Data:
    try:
        rt = [ i for i in read_data() if i["id"] == id][0]
        return Data(**rt)
    except IndexError as e:
        fsdb_logger(f"{e}","no record")
        return None
    
    
def get_by_name(name: str) -> Data:
    try:
        rt = [ i for i in read_data() if i["name"] == name][0]
        return Data(**rt)
    except IndexError as e:
        fsdb_logger(f"{e}","no record")
        return None

