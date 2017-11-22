from sikuli import *
from java.lang import System
from common import *
import math

Pos_Support  = 0 
Pos_Gardens  = 1
Pos_Port     = 2
Pos_Castle   = 3
Pos_Embassy  = 4
Pos_Range    = 5
Pos_Barracks = 6
Pos_Stables  = 7
Pos_Fountain = 8
Pos_Wall     = 9
Pos_Keystone = 10
Pos_Zeppelin = 11
Pos_Exchange = 12
Pos_Farms1   = 13 # No image for this position
Pos_Farms2   = 14 # No image for this position

anchors = []

anchorImages = ["1504120963638.png", "1504121063996.png", "1504121099282.png", "1504121151165.png", "1504121222509.png",
                "1504176100796.png", "1504121301157.png", "1504121322775.png", "1504121347061.png", "1504121369569.png",
                "1504121399320.png", "1504121430441.png", "1505574509235.png", "", ""]

anchorOffsets = [Location(0,0), Location(272,-193), Location(471,-126), Location(-263,-163), Location(158,-39),
                 Location(-292,11), Location(-300,192), Location(-185,142), Location(-435,24), Location(221, 202),
                 Location(745,471), Location(404,-191), Location(251, -92), Location(488, 371), Location(778, 124)]

bagResources = ["1504818126267.png", "1504818137993.png", "1504818150387.png", "1504819557678.png", "1504818162044.png", "1504818171169.png", "1504818180876.png", "1504818190363.png", "1504818205776.png", "1504818218244.png",
                "1504818231664.png", "1504818243413.png", "1504818289542.png", "1504818760493.png", "1504818770714.png", "1504818780465.png", "1504818813360.png", "1504818825413.png", "1504818834752.png", "1504818865969.png"]

farmImages = ["1506944719575.png", "1506944746211.png", "1506944774051.png", "1511303699504.png"]
        
fountainImages = ["1511307260456.png", "1511307248325.png", "1511307271249.png", "1511307279403.png"]

class Anchor(object):
    mImg = None
    mOffset = None

    def __init__(self, img, loc):
        self.mImg = img
        self.mOffset = loc

    def getImg(self):
        return self.mImg

    def getOffset(self):
        return self.mOffset

    def getX(self):
        return self.mOffset.getX()

    def getY(self):
        return self.mOffset.getY()

def prepareAnchors():
    print "castle.prepareAnchors call"
    for i in range(len(anchorImages)):
        anch = Anchor(anchorImages[i], anchorOffsets[i])
        anchors.append(anch)

def checkForHints(owner):
    print "castle.checkForHints call"
    cargo = owner.exists("1504120900956.png", 2)
    if cargo:
        clickRnd(cargo)
        clickRnd( owner.wait("1503303285947.png", 2) )
    help = owner.exists("1504695520824.png", 2)
    if help:
        clickRnd(help)
        sleep(2)

def locate(owner, locIdx):
    Debug.log(1, "CALL castle.locate %1$s", locIdx)
    trg = anchors[locIdx]
    trgR = exists(trg.getImg(), 1)
    if trgR != None:
        trgR.highlight(1)
        return
    for anch in anchors:
        closePopups(owner)
        rgn = owner.exists(anch.getImg(), 1)
        if rgn != None:
            rgn.highlight(1)
            center = owner.getCenter()
            shift = Location(center.x - rgn.getCenter().x + anch.getX() - trg.getX(), center.y - rgn.getCenter().y + anch.getY() - trg.getY())
            print "Summary shift:", shift
            count_x = int( math.ceil( abs(shift.x) / 0.6 / owner.w ) )
            count_y = int( math.ceil( abs(shift.y) / 0.6 / owner.h ) )
            print "count_x:", count_x, "count_y:", count_y
            count = max(count_x, count_y)
            shift_step = Location(shift.x // count, shift.y // count)
            half_step = Location(shift_step.x // 2, shift_step.y // 2)
            center_reg = Region(center.x - 30, center.y - 30, 60, 60)
            for i in range(0, count):
                closePopups(owner)
                rnd_center = pointRnd(center_reg)
                beg_point = Location(rnd_center.x - half_step.x, rnd_center.y - half_step.y)
                end_point = Location(rnd_center.x + half_step.x, rnd_center.y + half_step.y)
                slowDragDrop(owner, beg_point, end_point)
            break

def dragonChallenge(owner):
    Debug.log(1, "CALL ---- DRAGON CHALLENGE -----")
    closePopups(owner)
    checkForHints(owner)
    locate(owner, Pos_Gardens)
    checkForHints(owner)
    try:
        clickImagesRnd(owner, ["1504525543350.png", "1505126524054.png"])
        fast = owner.exists(Pattern("1505649506701.png").similar(0.90), 2)
        if fast:
            Debug.log(1, "Fast mode started")
            clickRnd(fast)
            fin = owner.exists("1507502064164.png", 30)
            if fin:
                clickRnd(fin)
                clickRnd( owner.wait("1507502207166.png", 3) )
        normal = owner.exists("1503360222830.png", 1)
        if normal:
            Debug.log(1, "Challenge is accepted")
            clickRnd(normal)
            sleep(2)
            clickRnd( owner.wait("1503361031868.png", 2) )
        else:
            cont = owner.exists("1503359163762.png", 1)
            if cont:
                clickRnd(cont)
            else:
                return()    
        while owner.exists("1503304190750.png", 5) == None:
            step = findOneOf(owner, ["1503397709059.png", "1503400697703.png", "1511301786195.png"])
            if step:
#                owner_y = owner.getCenter().getY()
#                step_y = step.getCenter().getY()
#                if step_y < owner_y:
#                    drag_reg = Region(owner.getX()+ 20, owner.getY() + 80, 40, 70)
#                    beg_loc = pointRnd(drag_reg)
#                    end_loc = pointRnd( drag_reg.offset(0, owner_y - step_y) )
#                    print "castle.dragonChallenge DragDrop From:", beg_loc, "To:", end_loc
#                    owner.dragDrop(beg_loc, end_loc)
#                    step = owner.wait(step.getImage(), 10) #refind sword after dragdrop
#                step.highlight(1)
                clickRnd( step.offset(0, step.getH()+10) )
                print "castle.dragonChallenge Fire next monster"
                fire = owner.exists("1503398071679.png", 2)
                if fire:
                    clickRnd(fire)
                sleep(7)
                while findOneOf(owner, ["1503401790750.png",
                    "1503303641987.png",
                    "1503303905110.png",
                    "1503304124989.png"] ):
                        print "castle.dragonChallenge Popup ignoring"
                        clickBack()
                        sleep(2)
        clickBack()
        Debug.log(1, "Treating the troops")
        clickRnd( find("1505426172474.png") )
        if owner.exists("1506636887579.png", 1):
            Debug.log(1, "Troops are in hospital already")
            clickBack()
        clickImagesRnd(owner, ["1505426273902.png", "1505426300565.png"])
    except FindFailed:
        print "ERROR. Something wrong on threat troops at Dragon Challenge"
    clickBackN(2)
    print "castle.dragonChallenge finished"

def treasury(owner):
    Debug.log(1, "CALL ---- TREASURY ----")
    closePopups(owner)
    checkForHints(owner)
    clickImagesRnd(owner, ["1504525543350.png", "1505126562813.png"])
    
    sleep(5)
    fin = owner.exists("1503612318821.png", 1)
    if fin:
        Debug.log(1, "Finish button found. Click it.")
        clickRnd(fin)
        sleep(5)
    for i in range(0, 1):       
        beg_free = owner.exists("1503611041801.png", 1)
        if beg_free == None:
            Debug.log(1, "No Begin button found. Exiting..")
            clickBack()
            return()
        clickRnd(beg_free)
        while True:
            reject = owner.exists(Pattern("1504764983306.png").similar(0.90), 3) #No coins to continue
            if reject:
                Debug.log(1, "No coins for continue. Exiting..")
                clickBackN(2)
                return()
            if owner.exists(Pattern("1505132726391.png").similar(0.95)):
                Debug.log(1, "Maximum attempts achieved")
                return()
            cubes = owner.exists("1503611083109.png", 3)
            if cubes != None:
                Debug.log(1, "Run cubes rotation")
                clickRnd( cubes.above(100) )
                sleep(13)
            else:
                break
        clickRnd( owner.wait("1503612318821.png", 1) )
        sleep(5)
    clickBack()
    print "castle.treasury finished"

def useBagResource(owner, resImage):
    try:
        tile = owner.find(resImage)
        clickRnd(tile)
        clickRnd( owner.find("1504802506615.png") )
        slider = owner.exists("1504802574818.png", 2)
        if slider:
            plus = find("1504802740774.png")
            beg_pos = pointRnd(slider)
            end_pos = pointRnd(plus)
            owner.dragDrop(beg_pos, end_pos)
            clickRnd( owner.find("1504815746534.png") )
        else:
            okbtn = owner.exists("1504816402635.png", 1)
            if okbtn:
                clickRnd(okbtn)
            else:
                clickRnd(tile) # Because the resource can not be used
        sleep(2)
        if not owner.exists("1505512790345.png", 2):
            print "Returning to the Bag"
            clickBack()
        sleep(1)
    except FindFailed:
        print "Resource not found in the Bag"
    
def useBagResources(owner, resImages):
    Debug.log(1, "CALL castle.useBagResources")
    inner_reg = owner.grow(-100)
    for img in resImages:
        useBagResource(owner, img)
    for i in range(0, 3):
        moveByParts(inner_reg, mD) #scroll down for three times
    for img in resImages:
        useBagResource(owner, img)
    Debug.log(1, "castle.useBagResources finished")

def clearBag(region):
    Debug.log(1, "CALL ---- CLEAR BAG ----")
    closePopups(region)
    clickRnd( region.find("1504800698750.png") )
    sleep(3)
    clickBack()
    sleep(2)
    clickRnd( region.find("1504800698750.png") )
    useBagResources(region, bagResources)
    clickBack()
    Debug.log(1, "castle.clearBag finished")

def findFarms(region):
    Debug.log(1, "CALL castle.findFarms")
    res = []
    region.setFindFailedResponse(SKIP)
    for i in farmImages:
        Debug.log(1, "Trying to find farm %1$s", i)
        tiles = region.findAll(i)
        if tiles:
            Debug.log(1, "Farms found")
            res.extend(tiles)
    region.setFindFailedResponse(ABORT)
    return res    

def clearFarms(region):
    Debug.log(1, "CALL ---- CLEAR INTERNAL FARMS ----")
    closePopups(region)
    locate(region, Pos_Farms1)
    checkForHints(region)
    for f in findFarms(region):
        clickRnd(f)
    locate(region, Pos_Farms2)
    checkForHints(region)
    for f in findFarms(region):
        clickRnd(f)
    Debug.log(1, "castle.clearFarms finished")


def useFountain(region, resKind):
    Debug.log(1, "CALL ---- USE FOUNTAIN RESOURCES ----")
    closePopups(region)
    locate(region, Pos_Fountain)
    clickImagesRnd(region, ["1507131360536.png", "1507131412687.png"] )
    img = region.exists(fountainImages[resKind])
    btn_reg = img.grow(100, 0).below(150)
    while True:
        btn = btn_reg.exists("1507131841641.png", 1)
        if btn:
            Debug.log(1, "got resource in Fountain")
            clickRnd(btn)
            sleep(2)
        else:
            Debug.log(1, "No more free resource in Fountain")
            break
    while not region.exists("1507132059228.png"):
        clickBack()
    clickBack()
    Debug.log(1, "castle.useFountain finished")

def obtainGifts(region):
    Debug.log(1, "CALL castle.obtainGifts")
    try:
        clickRnd( region.find("1507130336689.png") )
        while True: 
                btn = region.exists( Pattern("1507130453183.png").similar(0.90) )
                if btn:
                    clickRnd(btn)
                    sleep(4)
                else:
                    break
        clickBack()
    except FindFailed:
        Debug.log(1, "EXCEPTION. Image not found in kingdom.sendResources")
    Debug.log(1, "castle.obtainGifts finished")

def unpackLetters(region, mailBoxImg):
    Debug.log(1, "CALL castle.unpackLetters %1$s", mailBoxImg)
    clickRnd( region.wait(mailBoxImg, 3) )
    while region.exists("1511280679178.png"):
        clickImagesRnd(region, ["1511280591126.png", "1511280620859.png", "1511280635267.png", "1511280759807.png", "1511280591126.png", "1511280620859.png", "1511280646045.png", "1511280831675.png"])
        clickBack()
    sleep(1)
    clickBack()
    
    
def getMailGifts(region):
    Debug.log(1, "CALL castle.getMailGifts")
    closePopups(region)
    clickRnd( region.find("1511280158316.png") )
    unpackLetters(region, "1511280229081.png")
    unpackLetters(region, "1511280470444.png")
    unpackLetters(region, "1511280484286.png")
    unpackLetters(region, "1511280492527.png")
    clickBack()
    Debug.log(1, "castle.getMailGifts finished")

forFuture = ["1504800889579.png", "1504801297878.png", "1504801315145.png", "1504801496648.png", "1504801572720.png", "1504801619073.png", "1504801639638.png", "1505546729697.png", "1505547223657.png", "1505547235933.png", "1505549564410.png"]


prepareAnchors()


    
    
    
