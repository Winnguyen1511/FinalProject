import json




def sysLogin(sysconfig_file, gate):
    #Simulate loging process
    # global sysconfig
    with open(sysconfig_file, 'r') as f:
        data = f.read()
    
    #parse the object:
    sysconfig = json.loads(data)[gate]
    # print(sysconfig["in"]["host"])
    print('> Logged in!')
    return True, sysconfig

def getRFID(lstRFID):
    return lstRFID.pop(-1)

def getParkingLotID(sysconfig):
    return sysconfig["parkinglotid"]

def getStaffID(sysconfig):
    return sysconfig["staffid"]
def getCameraID(sysconfig):
    return sysconfig["cameraid"]