import socket
from utils.GameControlData import GameControlData
from utils.logging import get_logger
from pynput import keyboard
from vaapi.client import Vaapi
import os
from queue import Queue
import threading
from iterfzf import iterfzf

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
        self.logger = get_logger()
        
    def run(self):
        try:
            data, address = self.__socket.recvfrom(8192)
            
            if len(data) > 0:
                if self.__source is None or address[0] == self.__source:
                    message = GameControlData(data)
                    self.logger.info(message.secsRemaining)
                    return message
        except Exception as e:
            self.logger.error(e)
            return None

class SituationMarker():
    def __init__(self,key:str='h'):
        self.key = key
        self.client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
        self.queue = Queue()
        self.controller = GameController()
        
        self.game = None
        
        self.menu()
        self.start_threads()
        

    def start_threads(self):
        listener_thread = threading.Thread(target=self.key_listener,args=(self.queue,),daemon=True)
        listener_thread.start()
        game_thread = threading.Thread(target=self.game_listener,args=(self.queue,),daemon=True)
        game_thread.start()
        
    def menu(self):
        games = self.client.games.list()
        
        game_map = {f"{game.start_time}: {game.team1} vs {game.team2} {game.half}": game for game in games}
        selected_str = iterfzf(game_map.keys())
        if selected_str:
            selected_game = game_map[selected_str]
            self.game = selected_game.id    
                
    def key_listener(self,q):
        def on_release(key):
            if key == keyboard.KeyCode.from_char(self.key):            
                q.put('msg')
            elif key == keyboard.Key.esc:
                quit()
        with keyboard.Listener(
        on_release=on_release,suppress=True) as listener:
            listener.join()
            
    def game_listener(self,q):
        while True:
            msg = q.get()
            if msg == 'msg':
                message = self.controller.run()
                if message:
                    print(f'sending this time  {message.secsRemaining} to db')
            q.task_done()
                
            
if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    
    response = client.situation.create()
    print(response)
    # m = SituationMarker()
    # try:
    #     # Keep the main thread alive
    #     while True:
    #         pass
    # except KeyboardInterrupt:
    #     print("Shutting down...")
    
    
