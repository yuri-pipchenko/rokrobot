from common import *
import common
import account
import kingdom

accountImages = ["1505069619124.png", "1505070250701.png", "1505070265885.png", "1505070277576.png", "1505070293164.png", "1505070305383.png", "1505070319898.png", "1505070338301.png"]
sendToImages = ["1506553279198.png", "1506292276572.png", "1506528760102.png", "1506528776655.png"]

def semicolonStrToIntList(s):
    words = s.strip().split(";")
    res = []
    for w in words:
        res.append(int(w))
    return res

def readCsvConfig(fileName):
    Debug.log(1, "CALL readCsfConfig %1$s", fileName)
    cfg = []
    f = open(fileName)    
    for line in f.readlines():
        Debug.log(1, "process line: %1$s", line)
        (sAccType, sAccProps, sActList, sResList, sMaterialDest, sFoodDest) = line.strip().split(",")
        accType = int(sAccType)
        if accType == account.Acc_Google:
            accProps = sAccProps.strip()
        else:
            (sName, sPass) = sAccProps.strip().split(";")
            accProps = [sName, sPass]
        actions = semicolonStrToIntList(sActList)
        resources = semicolonStrToIntList(sResList)
        (rng, img1, img2) = sMaterialDest.strip().split(";")
        matDest = [int(rng)-1, img1, img2]
        (rng, img1, img2) = sFoodDest.strip().split(";")
        foodDest = [int(rng)-1, img1, img2]
        cfg.append([accType, accProps, actions, resources, matDest, foodDest])
    f.close()
    return cfg

