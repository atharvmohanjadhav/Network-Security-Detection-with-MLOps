import sys 
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_msg,error_details:sys):
        self.error_msg = error_msg
        _,_,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in python script name [{self.filename}] line number [{self.lineno}] error message [{str(self.error_msg)}]"
    

