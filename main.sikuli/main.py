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
   return account.waitROKLoad(win)

def closeROK(win):
    win.right(50).click("1505205664308.png")
    icon = win.find("1505205722817.png")
    dragDrop(icon, icon.right(500))
    sleep(20)
    

def dailyRoutine():
    Debug.log(1, "-------- DAILY ROUTINE --------")
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
#                castle.clearBag(win)
                castle.useFountain(win, kingdom.Res_Iron)
                castle.checkForHints(win)
                castle.clearFarms(win)
                kingdom.obtainGifts(win)
        except FindFailed:
            Debug.log(1, "EXCEPTION. FindFailed")
            continue
        except ValueError:
            Debug.log(1, "EXCEPTION. UnknownGameState")
            break
    emulator.closeEmulator(win)
    Debug.log(1, "-- DAILY ROUTINE FINISHED --")

def farming():
    Debug.log(1, "-------- FARMING --------")
    while True:
        emulator.runEmulator()
        win = emulator.defineWindow(emulator.Emul_Nox)    
        win.highlight(1)
        if runROK(win):
            Debug.log(1, "Begin rotating accounts")
            for acc in range(0, len(accountImages)):
                try:
                    account.changeAccount(win, accountImages[acc])
                    Debug.log(1, "Do actions in CASTLE mode")
                    if modes.setMode(win, modes.Mode_Castle):
                        closePopups(win)
                        castle.checkForHints(win)
                    Debug.log(1, "Do actions in MAP mode")
                    if modes.setMode(win, modes.Mode_Map):
#                        kingdom.sendResources(win)
                        kingdom.collectResources(win, accountRes[acc])
                        kingdom.returnCamps(win)
                        kingdom.obtainGifts(win)
                except FindFailed:
                    Debug.log(1, "EXCEPTION. FindFailed")
                    continue
                except ValueError:
                    Debug.log(1, "EXCEPTION. UnknownGameState")
                    break
        else:
            Debug.log(1, "Game is not started. Try later..")
            sleep(300)
        emulator.closeEmulator(win)
    Debug.log(1, "---- FARMING FINISHED ----")

def warMode():
    Debug.log(1, "-------- WAR MODE --------")
    while True:
        emulator.runEmulator()
        win = emulator.defineWindow(emulator.Emul_Nox)    
        win.highlight(1)
        if runROK(win):
            Debug.log(1, "Begin rotating accounts")
            for acc in range(0, len(accountImages)):
                try:
                    account.changeAccount(win, accountImages[acc])
                    Debug.log(1, "Do actions in CASTLE mode")
                    if modes.setMode(win, modes.Mode_Castle):
                        closePopups(win)
                        castle.checkForHints(win)
                    if modes.setMode(win, modes.Mode_Kingdom):
                        Debug.log(1, "Go to safe zone")
                        clickRnd(Region(22,641,152,101))
                        if modes.setMode(win, modes.Mode_Map):
                            kingdom.occupyRuins(win)
                            kingdom.setupCamps(win)
                            kingdom.returnCamps(win)
                except FindFailed:
                    Debug.log(1, "EXCEPTION. FindFailed")
                    continue
                except ValueError:
                    Debug.log(1, "EXCEPTION. UnknownGameState")
                    break
        else:
            Debug.log(1, "Game is not started. Try later..")
            sleep(300)
        emulator.closeEmulator(win)    

def adjustWinSize(win):
    p1 = win.getBottomRight()
    p2 = Location(p1.x + 546 - win.w, p1.y + 969 - win.h)
    slowDragDrop(win, p1, p2)

accountImages = ["1505069619124.png", "1505070250701.png", "1505070265885.png", "1505070277576.png", "1505070293164.png", "1505070305383.png", "1505070319898.png", "1505070338301.png"]
accountRes    = [kingdom.resSet4, kingdom.resSet4, kingdom.resSet1, kingdom.resSet1, kingdom.resSet1, kingdom.resSet1, kingdom.resSet2, kingdom.resSet2]
#accountRes    = [kingdom.resSet3, kingdom.resSet3, kingdom.resSet3, kingdom.resSet3, kingdom.resSet3, kingdom.resSet3, kingdom.resSet3, kingdom.resSet3]

#accountImages = ["1505070265885.png", "1505070277576.png", "1505070293164.png", "1505070305383.png", "1505070319898.png", "1505070338301.png"]
#accountRes    = [kingdom.resSet1, kingdom.resSet1, kingdom.resSet1, kingdom.resSet1, kingdom.resSet2, kingdom.resSet2]



Settings.MoveMouseDelay = 0.5
Settings.UserLogs = True
Settings.UserLogPrefix = "user"
Settings.UserLogTime = True

while False:
    kingdom.setupCamps(win)
    kingdom.returnCamps(win)
    sleep(20)

#kingdom.occupyRuins(win)
#dailyRoutine()
farming()
#warMode()
#win = emulator.defineWindow(emulator.Emul_Nox)    
#win.highlight(2)
#print "Emulator demensions:", win.w, win.h

#kingdom.setupCamps(win)

#castle.useFountain(win, kingdom.Res_Iron)
#adjustWinSize(win)
#castle.clearFarms(win)
#ingdom.collectResources(win, kingdom.resSet1)
#kingdom.sendResources(win)
#print "Emulator demensions:", win.w, win.h
#Correct size: 546x969
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