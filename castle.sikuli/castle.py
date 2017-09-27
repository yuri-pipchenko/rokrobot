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

anchors = []

anchorImages = ["1504120963638.png", "1504121063996.png", "1504121099282.png", "1504121151165.png", "1504121222509.png",
                "1504176100796.png", "1504121301157.png", "1504121322775.png", "1504121347061.png", "1504121369569.png",
                "1504121399320.png", "1504121430441.png", "1505574509235.png"]

anchorOffsets = [Location(0,0), Location(272,-193), Location(471,-126), Location(-263,-163), Location(158,-39),
                 Location(-292,11), Location(-300,192), Location(-185,142), Location(-435,24), Location(221, 202),
                 Location(745,471), Location(404,-191), Location(251, -92)]

bagResources = ["1504818126267.png", "1504818137993.png", "1504818150387.png", "1504819557678.png", "1504818162044.png", "1504818171169.png", "1504818180876.png", "1504818190363.png", "1504818205776.png", "1504818218244.png",
                "1504818231664.png", "1504818243413.png", "1504818289542.png", "1504818760493.png", "1504818770714.png", "1504818780465.png", "1504818813360.png", "1504818825413.png", "1504818834752.png", "1504818865969.png"]

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
        fast = owner.exists("1505649506701.png", 2)
        if fast:
            clickRnd(fast)
            sleep(3)
            clickBack()
        normal = owner.exists("1503360222830.png", 1)
        if normal:
            clickRnd(normal)
            clickRnd( owner.wait("1503361031868.png", 4) )
        else:
            cont = owner.exists("1503359163762.png", 1)
            if cont:
                clickRnd(cont)
            else:
                return()    
        while owner.exists("1503304190750.png", 5) == None:
            step = findOneOf(owner, ["1503397709059.png", "1503400697703.png"])
            if step:
                owner_y = owner.getCenter().getY()
                step_y = step.getCenter().getY()
                if step_y < owner_y:
                    drag_reg = Region(owner.getX()+ 20, owner.getY() + 80, 40, 70)
                    beg_loc = pointRnd(drag_reg)
                    end_loc = pointRnd( drag_reg.offset(0, owner_y - step_y) )
                    print "castle.dragonChallenge DragDrop From:", beg_loc, "To:", end_loc
                    owner.dragDrop(beg_loc, end_loc)
                    step = owner.wait(step.getImage(), 10) #refind sword after dragdrop
                step.highlight(1)
                clickRnd( step.offset(0, step.getH()+10) )
                print "castle.dragonChallenge Fire next monster"
                fire = owner.exists("1503398071679.png", 2)
                if fire:
                    clickRnd(fire)
                while findOneOf(owner, ["1503401790750.png",
                    "1503303641987.png",
                    "1503303905110.png",
                    "1503304124989.png"] ):
                        print "castle.dragonChallenge Popup ignoring"
                        clickBack()
                        sleep(1)
        clickBack()
        clickImagesRnd(owner, ["1505426172474.png", "1505426273902.png", "1505426300565.png"])
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
    beg_free = owner.exists("1503611041801.png", 1)
    if beg_free == None:
        clickBack()
        return()
    clickRnd(beg_free)
    while True:
        reject = exists("1504764983306.png", 3)
        
        if reject != None:
            clickBackN(2)
            return()
        cubes = owner.exists("1503611083109.png", 3)
        if cubes != None:
            clickRnd( cubes.above(100) )
            sleep(10)
        else:
            break
    clickRnd( owner.wait("1503612318821.png", 2) )
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
    for i in range(0, 3):
        for img in resImages:
            useBagResource(owner, img)
        if i < 3:
            beg_reg = screenPartToRegion(inner_reg, 6)
            end_reg = screenPartToRegion(inner_reg, 2)
            closePopups(owner)
            beg_point = pointRnd(beg_reg)
            end_point = pointRnd(end_reg)
            owner.dragDrop(beg_point, end_point)
    print "castle.useBagResources finished"

def clearBag(owner):
    Debug.log(1, "CALL castle.clearBag")
    closePopups(owner)
    clickRnd( owner.find("1504800698750.png") )
    sleep(2)
    clickBack()
    clickRnd( owner.find("1504800698750.png") )
    useBagResources(owner, bagResources)
    clickBack()
    print "castle.clearBag finished"



forFuture = ["1504800889579.png", "1504801297878.png", "1504801315145.png", "1504801496648.png", "1504801572720.png", "1504801619073.png", "1504801639638.png", "1505546729697.png", "1505547223657.png", "1505547235933.png", "1505549564410.png"]


prepareAnchors()


    
    
    
