from sikuli import *
from common import *

Mode_Unknown = 0
Mode_Map     = 1
Mode_Castle  = 2
Mode_Kingdom = 3
Mode_World   = 4

def scaleOut(region):
    Debug.log(1, "CALL modes.scaleOut")
    backToNormalView(region)
    region.keyDown(Key.CTRL)
    region.wheel(region.getCenter(), Button.WHEEL_DOWN, 10)
    region.keyUp(Key.CTRL)

def currentMode(region):
    Debug.log(1, "CALL modes.currentMode")
    if region.exists("1503338839512.png", 1) != None:
        return Mode_Castle
    elif region.exists("1503342296835.png", 1) != None:
        return Mode_Map
    elif region.exists("1505426687401.png", 1) != None:
        return Mode_Kingdom
    else:
        return Mode_Unknown
    
def setMode(region, mode):
    Debug.log(1, "CALL modes.setMode. Target mode: %1$s", mode)
    cur_mode = currentMode(region)
    if cur_mode == mode:
        Debug.log(0, "Already in target mode")
    else:
        Debug.log(0, "Changing the mode")
        if mode == Mode_Map:
            if cur_mode == Mode_Kingdom:
                clickRnd( region.find("1505427992903.png") )
            else:
                clickRnd( region.find("1503338839512.png") )
        elif mode == Mode_Castle:
            if cur_mode == Mode_Kingdom:
                clickRnd( region.find("1505427992903.png") )
            clickRnd( region.wait("1503342296835.png", 10) )
        elif mode == Mode_Kingdom:
            if cur_mode == Mode_Castle:
                clickRnd( region.find("1503338839512.png") )
            clickRnd( region.wait("1505428512489.png", 10) )
        sleep(10)
    scaleOut(region)
    new_mode = currentMode(region)
    Debug.log(1, "modes.setMode finished. Current mode is: %1$s", new_mode)
    return mode == new_mode