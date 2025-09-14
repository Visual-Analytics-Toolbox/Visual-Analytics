import socket
import logging
from GameControlData import GameControlData
from pynput import keyboard
from vaapi.client import Vaapi
import os



def get_games():
    response = client.games.list()
    for game in response:
        print(game)





def get_logger(    
        LOG_FORMAT     = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        LOG_NAME       = '',
        LOG_FILE_INFO  = 'situation.log',
        LOG_FILE_ERROR = 'error.log'):

    log           = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)

    # comment this to suppress console output
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(log_formatter)
    # log.addHandler(stream_handler)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.INFO)

    return log



class GameController():
    """
    The GameController class is used to receive the infos of a game.
    If new data was received, it gets parsed and published on the blackboard.
    """

    def __init__(self):
        """
        Constructor.
        Init class variables and establish the udp socket connection to the GameController.
        """
        self.__source = None
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__socket.bind(('', 3838))
        self.__socket.settimeout(1)  # in sec
        #error messages in diffrent logs than the messages
        self.logger = get_logger()
    def run(self):
        try:
            data, address = self.__socket.recvfrom(8192)
            
            if len(data) > 0:
                if self.__source is None or address[0] == self.__source:
                    message = GameControlData(data)
                    self.logger.info(message.secsRemaining)
        except Exception as e:
            self.logger.error(e)


class Listener():
    def __init__(self,GameController):
        self.GameController = GameController
        with keyboard.Listener(
        on_release=self.on_release) as listener:
            listener.join()
        
    
    def on_release(self,key, injected):
    
        if key == keyboard.KeyCode(char='h'):            
            self.GameController.run()



if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    get_games()

    a = GameController()
    b = Listener(a)

