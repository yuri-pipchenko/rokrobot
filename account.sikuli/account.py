from sikuli import *
from common import *

def waitROKLoad(region):
    Debug.log(1, "CALL account.waitROKLoad")
    Debug.log(1, "Waiting for cover")
    cover = region.exists("1505555097635.png", 60)
    if cover:
        Debug.log("Waiting for cover is closed")
        if cover.grow(50).waitVanish("1505555404394.png", 60):
            Debug.log(1, "ROK is successfully loaded")
            sleep(10)
            return True
        else:
            Debug.log(1, "Cover is not disappearing on Game start. Possible server update..")
            return False            
    else:
        Debug.log("ERROR. Cover is not appeared. Unknown state")
        return False
#    closePopups(region)
    
def changeAccount(region, acc):
    Debug.log(1, "CALL account.changeAccount")
    backToNormalView(region)
    
    clickPersonRnd(region) 
    clickImagesRnd(region, ["1503304318097.png", "1503304337764.png", "1503304352149.png", "1506594490858.png", acc])
    waitROKLoad(region)
    backToNormalView(region)
    Debug.log(1, "account.changeAccount finished")
