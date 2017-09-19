from sikuli import *
from common import *

Emul_Nox = 1

def defineWindow(type):
    print "emulator.defineWindow call. Type: ", type
    if type == Emul_Nox:
        leftPan = find("1503271552031.png")
        topPan = find("1505828573090.png")
        
        topPan.click( topPan.getCenter() )
        y = leftPan.getBottomLeft().getY() - topPan.getBottomLeft().getY()
        print "Emulator window detected"
        win = topPan.below(y)
        return win
    else:
        print "Unknown emulator type"
        return None

def runEmulator():
    doubleClick("1505689409707.png")
    sleep(180)

def closeEmulator(region):
    topPan = find("1505828573090.png")
    topPan.click("1505689555047.png")
    pop = region.wait("1505689585796.png", 5)
    pop.click("1505689610441.png")   
    sleep(120)

