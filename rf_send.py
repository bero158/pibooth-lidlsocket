# -*- coding: utf-8 -*-
import os
from pibooth.utils import LOGGER

rpiUtilsFolder = "/home/pi/pibooth/wiringPi/433Utils/RPi_utils"
protocol = 1
RC_ON = 0
RC_OFF = 1


def command(cmd):
    if cmd:
        status = os.system(cmd)
        LOGGER.debug(f"Executed: {cmd} with status: {status}")
    
def send(systemCode, unitCode, state = True):
    cmd = None
    if state:
        cmd = f"{rpiUtilsFolder}/send {systemCode} {unitCode} {RC_ON}"
    else:
        cmd = f"/home/pi/pibooth/pibooth-disco/send {systemCode} {unitCode} {RC_OFF}"
    command(cmd)

def codeSend(code):
    cmd = f"{rpiUtilsFolder}/codesend {code} {protocol}"
    command(cmd)
