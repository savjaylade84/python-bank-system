import logging
import logging.config
from pathlib import Path
import yaml


''' 
    this module will log every module in the system

    in the constructor of the module_log:

    --log_name - the name of the logger of the module
    --disable_log - this will disable the log of the entire logs in
                    module

    in every function in module_log:
    --message - the message that will input
    --disable - this will exclude a log from disabling the entire logs in
                the constructor 

'''

CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.yaml"


def load_config(path: Path = CONFIG_PATH) -> dict:
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(path,'r') as file:
        return yaml.load(file,Loader=yaml.FullLoader)

class Log:

        
    def initLogging(self, log_file:str):
        
        if not str:
            raise ValueError("Empty log file name")
        
        __yaml = load_config()
        
        if not __yaml:
            raise ValueError("fetch empty or failed to fetch config")
        
        logging.config.dictConfig(__yaml)
        self.__logger = logging.getLogger(log_file)
        return self.__logger
    
