# Module for turning Lidl SilverCrest socket On and Off.
# Model: 8 50 50 00075
# IAN: 390 530_2201
# Manufactured: 2022-06

from enum import Enum
import time
import rf_send
from pibooth.utils import LOGGER

class States(Enum):
        ON = 1
        OFF = 0
class LidlSockets:
    
    def __init__(self):
        self.autoTurnOffS = -1 #-1 = don't turn off
        self.sockets = {"A":{States.ON:"70CA1C",States.OFF:"71592C"},
                        "B":{States.ON:"723005",States.OFF:"746195"},
                        "C":{States.ON:"7387BE",States.OFF:"751D6E"},
                        "D":{States.ON:"7BB347",States.OFF:"78FCE7"},
                        }
        rf_send.protocol = 13 #custom protocol for Lidl socket. See https://github.com/bero158/rc-switch/tree/master
        
                        
    def getNextTurnOff(self, socket):
        if ("nextTurnOff" in self.sockets[socket].keys()):
                return self.sockets[socket]["nextTurnOff"]
                    
    def setNextTurnoff(self, socket):
        if (self.autoTurnOffS > 0 ): # and action == "ON"):
            now = time.time()
            next = now + self.autoTurnOffS
            self.sockets[socket]["nextTurnOff"] = next
            LOGGER.debug("Now: " + str(now ) + "Next Turnoff " + str(self.autoTurnOffS) + "s " +  socket + " at " + str(next))
      #   else:
      #      self.sockets[socket]["nextTurnOff"] = None

    def turn(self, socket = "A", action = States.ON):
        LOGGER.debug(f"Socket {socket} turning {action}.")
        rf_send.codeSend(int(self.sockets[socket][action],16))
        self.setNextTurnoff(socket)
        

    def wait_do(self):
        now = time.time()
        for socket in self.sockets:
            turnOffTime = self.getNextTurnOff(socket)
            if (turnOffTime):
                if (turnOffTime < now):
                    self.turn(socket,States.OFF)
