import logging
import logging.config
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


class Log:
    
    def __init__(self,log_file:str=''):
        with open('Log/.config/config.yaml','r') as file:
            __yaml = yaml.load(file,Loader=yaml.FullLoader)
        logging.config.dictConfig(__yaml)
        self.__logger = logging.getLogger(log_file)
        
    def open(self):
        return self.__logger
