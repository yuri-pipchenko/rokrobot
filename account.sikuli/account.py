from sikuli import *
from common import *

Acc_Google = 1
Acc_Email  = 2

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
    
def enterGoogleAccount(region, accImage):
    Debug.log(1, "CALL account.enterGoogleAccount %1$s", accImage)
    backToNormalView(region)
    
    clickPersonRnd(region) 
    clickImagesRnd(region, ["1503304318097.png", "1503304337764.png", "1503304352149.png", "1506594490858.png", accImage])
    waitROKLoad(region)
    backToNormalView(region)
    Debug.log(1, "account.enterGoogleAccount finished")

def enterEmailAccount(region, user, password):
    Debug.log(1, "CALL account.enterEmailAccount %1$s", user)
    backToNormalView(region)
    
    clickPersonRnd(region) 
    clickImagesRnd(region, ["1503304318097.png", "1503304337764.png", "1503304352149.png", "1511192494324.png"])
    region.type("1511192873354.png", user)
    region.type("1511192934745.png", password)
    clickRnd( find("1511276221382.png") )
    waitROKLoad(region)
    backToNormalView(region)
    Debug.log(1, "account.enterEmailAccount finished")

def enterAccount(region, accType, accProps):
    Debug.log(1, "CALL account.enterAccount")
    if accType == Acc_Google:
        enterGoogleAccount(region, accProps) #accProps must be an image
    elif accType == Acc_Email:
        enterEmailAccount(region, accProps[0], accProps[1]) #accProps must be an list with name and password
    else:
        Debug.log(1, "Unknown account type")