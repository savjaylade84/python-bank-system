import json


class FileManager:
    @staticmethod
    def read_json(path:str) -> dict:
        
        with open(path,'r') as file:
            
            temp:dict = json.load(file)
            
            if temp:
                return temp
        
        raise FileNotFoundError(f"Either [ Unable to load a json file ] or [ No file exist ]")

    @staticmethod
    def write_json(path:str,data:dict) -> bool:
        
        with open(path,'w') as file:
            
            if data:
                json.dump(data, file, indent=4)
                return True
            
        return False