import sys
from network_security.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self,err_msg,err_details:sys):
        self.err_msg=err_msg
        _,_,exc_tb = error_details.exc_info() ## not initialised bcoz never used outside init
        
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename 

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.err_msg))


# if __name__=='__main__':
#     try:
#         logging.logging.info("Enter the try block")
#         a=1/0
#         print("This will not be printed",a)
#     except Exception as e:
#            raise NetworkSecurityException(e,sys)


