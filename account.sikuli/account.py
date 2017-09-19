from sikuli import *
from common import *

def waitROKLoad(region):
    Debug.log(1, "CALL account.waitROKLoad")
    Debug.log(1, "Waiting for cover")
    cover = region.exists("1505555097635.png", 60)
    if cover:
        Debug.log("Waiting for cover is closed")
        cover.grow(50).waitVanish("1505555404394.png", 60)
        sleep(10)
    else:
        Debug.log("ERROR. Cover is not appeared. Unknown state")
        raise ValueError('Cover is not appear on Game start.')
    closePopups(region)
    
def changeAccount(region, acc):
    Debug.log(1, "CALL account.changeAccount")
    backToNormalView(region)
    
    clickPersonRnd(region) 
    clickImagesRnd(region, ["1503304318097.png", "1503304337764.png", "1503304352149.png", "1503304365254.png", acc])
    waitROKLoad(region)
    backToNormalView(region)

def sendResources(region, whom, resKind):
    Debug.log(1, "CALL acount.sendResources")
    backToNormalView(region)
    
    clickImagesRnd(region, ["1503304318097-1.png", "1503304337764-1.png", "1503304352149-1.png", "1503304365254-1.png", acc])

