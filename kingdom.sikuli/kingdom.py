from sikuli import *
from common import *
import random

Res_Food   = 0
Res_Wood   = 1
Res_Iron   = 2
Res_Silver = 3

resourceImages = ["1504627880561.png", "1504627956538.png", "1504627909370.png", "1504628011262.png"]
convoyImages = ["1505575078585.png", "1505575098288.png", "1505575069371.png", ""]
resZeroImages = ["1506443543752.png", "1506443034118.png", "1506443071581.png", ""]

resSet1 = [Res_Iron, Res_Wood, Res_Food]
resSet2 = [Res_Iron, Res_Food, Res_Wood]

Range1 = 0
Range2 = 1
Range3 = 2
Range4 = 3
Range5 = 4

rangeImages = ["1506033700476.png", "1506033821564.png", "1506033836072.png",
               "1506033848538.png", "1506033860871.png"]

NoTroops = 100

resources = []

def inOccupied(coord, occupied):
    Debug.log(1, "CALL kingdom.inOccupied %1$s %2$s", [coord, occupied])
    for p in occupied:
        dist = distance(coord, p)
        Debug.log(1, "Check for tile in already occupied: %1$s, Distance: %2$s", [p, dist])
        if distance(coord, p) < 15:
            Debug.log(1, "This tile IS already occupied")
            return True
    Debug.log(1, "This tile IS NOT occupied earlier")
    return False        

def findTiles(region, resSet):
    Debug.log(1, "CALL kingdom.findTiles %1$s", resSet)
    res = []
    region.setFindFailedResponse(SKIP)
    for r in resSet:
        Debug.log(1, "Trying to find resource kind %1$s", r)
        img = resourceImages[r]
        tiles = region.findAll(img)
        if tiles:
            Debug.log(1, "Resource found")
            res.extend(tiles)
    region.setFindFailedResponse(ABORT)
    return res
    
def occupyResource(region, resSet, occupied):
    Debug.log(1, "CALL kingdom.occupyResource %1$s. Already occupied: %2$s", [resSet, occupied])
    closePopups(region)
    tiles = findTiles(region, resSet)
    if not tiles: #empty list found
        return None
    for t in tiles:
        closePopups(region)
        Debug.log(1, "Trying to occupy tile at: %1$s", t)
        if inOccupied(t, occupied):
            continue
        clickRnd(t)
        occupy = region.exists("1504630391615.png", 2)
        if occupy:
            clickRnd(occupy)
            if region.exists("1505598796114.png", 2):
                clickBack()
                sleep(3)
                return NoTroops
            clickRnd( region.wait("1504630712884.png", 3) )
            if region.exists("1505602289803.png", 2):
                clickBackN(2)
                return NoTroops
            if region.exists("1504631086564.png", 2):
                clickBack()
                sleep(3)
            else:
                return t.getTopLeft()
        else:
            while True:
                p2 = pointRnd(region.grow(-120, -220))
                if distance(t.getCenter(), p2) > 100:
                    region.click(p2)
                    break
    return None

def moveRnd(owner, coords_for_shift):
    Debug.log(1, "CALL kingdom.moveRnd")
    beg_idx = random.randint(1, 7)
    while True:
        end_idx = random.randint(0, 7)
        if beg_idx != end_idx:
            break
    count = random.randint(1, 3)
    inner_reg = owner.grow(-100)
    print "owner: ", owner, "inner_reg: ", inner_reg
    beg_reg = screenPartToRegion(inner_reg, beg_idx)
    end_reg = screenPartToRegion(inner_reg, end_idx)
    for i in range(0, count):
        closePopups(owner)
        beg_point = pointRnd(beg_reg)
        end_point = pointRnd(end_reg)
        slowDragDrop(owner, beg_point, end_point)
        shift = Location(end_point.x - beg_point.x, end_point.y - beg_point.y)
        return shiftCoords(coords_for_shift, shift)

def collectResources(owner, resSet):
    Debug.log(1, "CALL kingdom.collectResources")
    occupied = []
    closePopups(owner)
    if owner.exists("1504626448184.png"):
        return
    for i in range(0, 30): #After 30 attemps exit. No tiles found
        tile = occupyResource(owner, resSet, occupied)
        if tile == NoTroops:
            return()
        if tile == None:
            occupied = moveRnd(owner, occupied)
        else:
            occupied.append(tile)
    print "kingdom.collectResources finished"

def returnTroops(region):
    print "kingdom.returnTroops call"
    while True:
        back = region.exists("1505250782722.png", 1)
        if back:
            clickRnd(back)
            clickRnd( wait("1505250997789.png", 3) )            
        else:
            break
    print "kingdom.returnTroops finished"

def checkForOccupied(region):
    print "kingdom.checkForOccupied call"
    try:
        for b in region.findAll("1505250782722.png"):
            occupied = b.left(200).exists("1505303404123.png", 1)
            if occupied != None:
                occupied.highlight(2)
                print "Ruins are already occupied."
                return True
    except FindFailed:
        print "No back buttons found. Ready to seek for ruins"
    return False

def occupyRuins(region):
    print "kingdom.occupyRuins call"
    if checkForOccupied(region):
        return()
    while True:
        ruin = region.exists("1505252015491.png", 1)
        if ruin != None:
            print "Ruins found"
            ruin = moveToCenter(region, ruin)
            clickRnd(ruin)
            region.click("1505252255407.png")
            if region.exists("1505431811409.png"):
                print "One march is in ruins."
                clickBack()
                return()
            buttons = region.findAll( precise("1505252417217.png") )
            sorted_buttons = sorted(buttons, key=lambda m:m.y, reverse=True)
            for sb in sorted_buttons:
                try:
                    clickRnd(sb)
                    if exists("1505431404084.png"):
                        print "Maximum number of march"
                        clickBack()
                        return()
                    else:
                        clickRnd( region.find("1505253180540.png") )
                        print "Ruins are occupied"
                        return()
                except FindFailed:
                    continue
        else:
            print "Ruins not found, moving random"
            moveRnd(region, [])

def underShild(region):
    print "kingdom.underShild call"
    res = False
    print "kingdom.underShild returns:", res
    return res

def setupCamps(region):
    print "kingdom.setupCamps call"
    backToNormalView(region)
    while True:
        for i in range(0, 15):
            p1 = pointRnd(region.grow(-120, -220))
            region.click(p1)
            tp = region.exists("1505392746272.png")
            if tp != None:
                try:
                    clickRnd( tp.right(150).grow(20).find("1505392863162.png") )
                    if region.exists("1505393098116.png") != None:
                        print "Can't set up a camp. Maximum march number"
                        clickBack()
                    else:
                        clickRnd( find("1505392924678.png") )
                    return True
                except FindFailed:
                    print "Seize button not found or another strange things occur"
            clickRnd(region.grow(-150, -200))
            sleep(2)
            while True:
                p2 = pointRnd(region.grow(-120, -220))
                if distance(p1, p2) > 100:
                    region.click(p2)
                    backToNormalView(region)
                    break
        moveRnd(region, [])

def returnCamps(region):
    Debug.log(1, "kingdom.returnCamps call")
    backToNormalView(region)
    more = region.exists("1504626448184.png", 0)
    if more:
        clickRnd(more)
    try:
        for b in region.findAll( precise("1505250782722.png")):
            print "Back button checking"
            iscamp = b.left(200).exists("1505395766638.png", 1)
            
            if iscamp != None:
                print "Troops are returning from the camp."
                clickRnd(b)
                clickRnd( wait("1505395550716.png", 2) )
                return True
            else:
                print "It is not a camp"
    except FindFailed:
        print "No back buttons found. No troops to return."
        return False

def troopsMustGo(region):
    print "kingdom.troopsMustGo call"
    occupyRuins(region)
    if not underShild(reguin):
        returnCamps(region)
        setupCamps(region)
    print "kingdom.troopsMustGo finished"
    
def showSafeZone(region, zone):
    print "kingdom.showSafeZone call"
    if modes.setMode(win, modes.Mode_Kingdom):
        clickRnd(zone)
    modes.setMode(win, modes.Mode_Map)
    print "kingdom.showSafeZone finished"

def zeroResources(region, resKinds):
    Debug.log(1, "CALL kingdom.zeroResources, %1$s", resKinds)
    head = Region(region)
    head.setH(40)
    zeros = []
    for i in resZeroImages:
        zeros.append( head.exists(Pattern(i).similar(0.9), 0) )
    sum_zero = True
    for r in resKinds:
        sum_zero = sum_zero and zeros[r]
    if sum_zero:
        return None
    else:
        return zeros

def openMemberPage(region, alRange, memberIcon, memberNamePic):
    Debug.log(1, "CALL kingdom.openMemberPage %1$s, %2$s", [alRange, memberIcon])
    backToNormalView(region)
    clickImagesRnd(region, ["1505574780483.png", "1505574802226.png"])
    while True:
        sleep(2)
        up = region.exists(Pattern("1506033387460.png").exact())
        if not up:
            break
        clickRnd(up)
    Debug.log(1, "click Range line..")    
    clickRnd( region.find(rangeImages[alRange]) )
    no_member = True
    for i in range(0, 5):
        Debug.log(1, "seek for member icon..")
        icon = region.exists(Pattern(memberIcon).similar(0.9), 3)
        if icon:
            icon.setH(icon.h + 30)
            icon.setW(icon.w + 30)
            clickRnd(icon)
            no_member = False
            break
        Debug.log(1, "..member icon not found yet, scrolling..")    
        beg_reg = screenPartToRegion(region, 6)
        end_reg = screenPartToRegion(region, 2)
        beg_point = pointRnd(beg_reg)
        end_point = pointRnd(end_reg)
        slowDragDrop(region, beg_point, end_point)
        sleep(2)
    sleep(1)    
    if no_member:
        Debug.log(1, "Member not found in the alliance, exiting..")    
        clickBackN(2)
        return False
    if not exists(memberNamePic, 2):
        Debug.log(1, "Wrong member is opened. Trying again..")
        clickBackN(3)
        return False
    return True
    
def sendRes(region, alRange, memberIcon, memberNamePic, resKinds):
    Debug.log(1, "CALL kingdom.sendRes")
    zeros = zeroResources(region, resKinds)
    if not zeros:
        Debug.log(1, "No resources to send")        
        return None
    if not openMemberPage(region, alRange, memberIcon, memberNamePic):
        return None
    clickRnd( region.find("1505574921021.png") )
    if region.exists("1505393098116.png", 1):
        Debug.log(1, "No empty marches, exiting")
        clickBackN(4)
        return False
    for r in resKinds:
        if not zeros[r]:
            res = region.find( convoyImages[r] )
            beg_point = pointRnd( res.right(200).find("1505574963232.png") )
            end_point = pointRnd( res.right(700).find("1506291390404.png").left(30) )
            slowDragDrop(region, beg_point, end_point)
    sleep(1)
    if region.exists(Pattern("1506083074416.png").similar(0.90)):
        Debug.log(1, "Nothing to send, exiting")
        clickBackN(4)
        return False
    clickRnd( region.find("1505575027073.png") )
    sleep(2)
    return True
    
def sendResources(region):
    Debug.log(1, "CALL kingdom.sendResources")
    try:
        Debug.log(1, "Sending Iron and Wood to main Buzuk")
        while False:
            if region.exists("1504626448184.png", 0):
                break
            if not sendRes(region, Range4, "1506553279198.png", "1506292276572.png", [Res_Iron, Res_Wood]):
                break
        Debug.log(1, "Sending Food to bu ZZZ uk")
        for i in range(0, 3): #Maximum attempts for problem with last caravan
            if region.exists("1504626448184.png", 0):
                break
            if not sendRes(region, Range2, "1506528760102.png", "1506528776655.png", [Res_Iron, Res_Wood, Res_Food]):                
                break
    except FindFailed:
        Debug.log(1, "EXCEPTION. Image not found in kingdom.sendResources")

def obtainGifts(region):
    Debug.log(1, "CALL kingdom.obtainGifts")
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
    Debug.log(1, "kingdom.obtainGifts finished")
