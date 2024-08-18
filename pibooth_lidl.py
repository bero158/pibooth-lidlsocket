# -*- coding: utf-8 -*-
"""Pibooth plugin for upload pictures to ConAdmin application."""
import pibooth
from lidl_sockets import LidlSockets, States
from pibooth.utils import LOGGER

__version__ = "1.0.2"
SECTION = 'Lidl'
TURNOFF = 'Turnoff'
TURNOFF_DEFAULT = '5'

def unescape(text):
    if (len(text)>1):
        if (text[0] == '"' and text[-1] == '"'):
            text = text[1:][:-1]
    return text


# --- Pibooth state-independent hooks ------------------------------------------
@pibooth.hookimpl
def pibooth_configure(cfg):
    """Actions performed after loading of the configuration file or when the
    plugin is enabled for the first time. The ``cfg`` object is an instance
    of :py:class:`ConfigParser` class.

    :param cfg: application configuration
    """
    """Declare the new configuration options"""
    cfg.add_option(SECTION, TURNOFF , TURNOFF_DEFAULT ,
                   "Turn off after (min)",
                   "Turn off (min)" , TURNOFF_DEFAULT )
    LOGGER.debug("pibooth_lidl - Configure options added" )
    

@pibooth.hookimpl
def pibooth_startup(cfg, app):
    """Actions performed at the startup of pibooth or when the plugin is enabled
    for the first time.

    :param cfg: application configuration
    :param app: application instance
    """
    LOGGER.info("pibooth_lidl - Hello from pibooth_lidl plugin")
    app.lidlSocket = LidlSockets()
    app.lidlSocket.autoTurnOffS = int(unescape(cfg.get(SECTION, TURNOFF ))) * 60
    LOGGER.debug("pibooth_lidl - Autoturnoff " + str(app.lidlSocket.autoTurnOffS) + "s")
    

@pibooth.hookimpl
def state_choose_enter(cfg, app, win):
    app.lidlSocket.turn()
    
@pibooth.hookimpl
def state_wait_do(cfg, app, win, events):
    """Actions performed when application is in Wait state.
    This hook is called in a loop until the application can switch
    to the next state.

    :param cfg: application configuration
    :param app: application instance
    :param win: graphical window instance
    :param events: pygame events generated since last call
    """
    app.lidlSocket.wait_do()

@pibooth.hookimpl
def pibooth_cleanup(app):
    """Actions performed at the cleanup of pibooth.

    :param app: application instance
    """
    app.lidlSocket.turn(action = States.OFF)