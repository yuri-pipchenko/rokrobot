from common import *
import common
import account
import modes
import castle
import kingdom
import emulator
import math

reload(common)
reload(account)
reload(modes)
reload(castle)
reload(kingdom)
reload(emulator)

#Settings.OcrTextSearch = True
#Settings.OcrTextRead = True

    
def getProps():
    top = find("1503241270521.png").right(470)
    top.highlight(2)
    tWood = top.find("1503225093138.png").right(50)
    tWood.highlight()
    Wood = tWood.text()
    tMeal = top.find("1503230738347.png").right(50)
    tMeal.highlight()
    Meal = tMeal.text()
    tIron = top.find("1503227926880.png").right(50)
    tIron.highlight()
    Iron = tIron.text()
    return (Wood, Meal, Iron)

def runROK(win):
   win.click("1505205538684.png")
   account.waitROKLoad(win)

def closeROK(win):
    win.right(50).click("1505205664308.png")
    icon = win.find("1505205722817.png")
    dragDrop(icon, icon.right(500))
    sleep(20)
    

def dailyRoutine():
    Debug.log(1, "-------- DAILY ROUTINE --------")
    while True:
        emulator.runEmulator()
        win = emulator.defineWindow(emulator.Emul_Nox)    
        win.highlight(1)        
        runROK(win)
        for acc in range(0, len(accountImages)):
            try:
                account.changeAccount(win, accountImages[acc])
                if modes.setMode(win, modes.Mode_Castle):
                    castle.dragonChallenge(win)
                    castle.treasury(win)
                    castle.clearBag(win)
                castle.checkForHints(win)
                if modes.setMode(win, modes.Mode_Map):
                    kingdom.collectResources(win, accountRes[acc])
            except FindFailed:
                Debug.log(1, "EXCEPTION. FindFailed")
                continue
            except ValueError:
                Debug.log(1, "EXCEPTION. UnknownGameState")
                break
        emulator.closeEmulator(win)

def warMode():
    while True:
        runROK(win)
        for acc in range(0, len(accountImages)):
            sleepRnd(120)
            try:
                account.changeAccount(win, accountImages[acc])
                if modes.setMode(win, modes.Mode_Map):
                    kingdom.occupyRuins(win)
                    kingdom.setupCamps(win)
                    kingdom.returnCamps(win)
            except FindFailed:
                continue
        closeROK(win)



accountImages = ["1505069619124.png", "1505070250701.png", "1505070265885.png", "1505070277576.png", "1505070293164.png", "1505070305383.png", "1505070319898.png", "1505070338301.png"]
accountRes    = [kingdom.Res_Wood, kingdom.Res_Food,  kingdom.Res_Iron, kingdom.Res_Food, kingdom.Res_Food, kingdom.Res_Food, kingdom.Res_Food, kingdom.Res_Food]

#accountImages = ["1505070277576.png", "1505070293164.png", "1505070305383.png", "1505070319898.png", "1505070338301.png"]
#accountRes    = [kingdom.Res_Food, kingdom.Res_Food, kingdom.Res_Food, kingdom.Res_Food, kingdom.Res_Food]



Settings.MoveMouseDelay = 0.5
Settings.UserLogs = True
Settings.UserLogPrefix = "user"
Settings.UserLogTime = True

while False:
    kingdom.setupCamps(win)
    kingdom.returnCamps(win)
    sleep(20)

#kingdom.occupyRuins(win)
#kingdom.collectResources(win, kingdom.Res_Food)
#dailyRoutine()
#warMode()

win = emulator.defineWindow(emulator.Emul_Nox)    
win.highlight(2)
print "Emulator demensions:", win.w, win.h

#castle.dragonChallenge(win)
#castle.clearBag(win)
#modes.setMode(win, modes.Mode_Kingdom)
#castle.clearBag(win)
#castle.treasury(win)
#kingdom.sendResources(win, "Buzuk", kingdom.Res_Wood)
#castle.locate(win, castle.Pos_Gardens)



#locate(win, Pos_Gardens)

#setMode(win, Mode_Map)
#setMode(win, Mode_Castle)
#setMode(win, Mode_Castle)
#clickPersonRnd(win)

#collectResources(win, Res_Food)

#(W, M, I) = getProps()
#System.out.println("W: " + W + " M: " + M + " I: " + I)