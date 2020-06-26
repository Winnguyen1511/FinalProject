import platerecognition as pr
import recognitionmodules as rm
import PostgreSQLQuery as psq
from Tables.Table import *
import os
import cv2
import math
from datetime import datetime as DT
import threading
DEFAULT_WORKSPACE = os.getcwd()+ '/resources/'
DEFAULT_SAVE_DIR = os.getcwd()+'/img/'

MIN_HEIGHT = 460
MIN_WIDTH = 100

MAX_HEIGHT = 800
MAX_WIDTH = 150


lstRFID = [str(rfid) for rfid in range(1, 1000)]
def getRFID():
    return lstRFID.pop(-1)
def getParkingLotID():
    return 'PKL001'

def imshow(im):
    imsize = im.shape
    w = imsize[1]
    h = imsize[0]
    if w < MIN_WIDTH or h < MIN_HEIGHT:
        w_scale = math.ceil(MIN_WIDTH / w)
        h_scale = math.ceil(MIN_HEIGHT / h)
        scale = max(w_scale, h_scale)
        w = w * scale
        h = h * scale
    if w > MAX_WIDTH or h > MAX_HEIGHT:
        w_scale = math.ceil(w / MAX_WIDTH)
        h_scale = math.ceil(h / MAX_HEIGHT)
        scale = min(w_scale, h_scale)
        w = math.floor(w / scale)
        h = math.floor(h / scale)
    tmp = cv2.resize(im, (w, h), interpolation=cv2.INTER_CUBIC)
    cv2.imshow('Plate in', tmp)
    cv2.waitKey(0)
def getImg(imgName, show=True):
    im = cv2.imread(imgName)
    if show == True:
        t = threading.Thread(target=imshow, args=(im,))
        t.start()
        # imshow(im)
    saveName = DEFAULT_SAVE_DIR +'in_'+ imgName
    if not os.path.isdir(DEFAULT_SAVE_DIR):
        os.mkdir(DEFAULT_SAVE_DIR)
    cv2.imwrite(saveName, im)
    return saveName

def sysLogin():
    #Simulate loging process
    print('> Logged in!')
    return True
def getStaffID():
    return 'STF001'
def getCameraID():
    return 'CM0001'

def main():
    #Init the system:
    res = sysLogin()
    if res == False:
        print('> Login failed!')
        return False
    
    #Connect to database:
    res, conn, cur= psq.login_database_Default()
    if res == False:
        print('> Connect database failed!')
        return False

    #Load model for AI modules:
    yoloPlate, characterRecognition = pr.sysInit_Default()
    
    os.chdir(DEFAULT_WORKSPACE)
    lstImg = [name for name in os.listdir() if name.endswith('.jpg') 
                                            or name.endswith('.jpeg')
                                            or name.endswith('.png')
                                            or name.endswith('.raw')]
    
    parking = ParkingTable(conn, cur)
    history = HistoryTable(conn,cur)
    for imgName in lstImg:
        # Load image, recognize the plate number:
        choice = input('> Press [ENTER] to load img:')
        if choice == '0':
            print('> Exiting...')
            break
        RFID = getRFID()
        PlateImgURL = getImg(imgName, show=True)
        _,PlateNumber = pr.plateRecog(PlateImgURL, yoloPlate, characterRecognition, show=False)
        ParkingLotID = getParkingLotID()
        CheckInTime = DT.now()
        StaffID = getStaffID()
        print(StaffID)
        CameraID = getCameraID()
        # cv2.waitKey(0)
        choice = input('> Press [ENTER] to allow vehicles in:')
        cv2.destroyAllWindows()
        if choice == '0':
            print('> Canceled!')
            continue
        # Insert to ParkingTable:
        res = parking.insert(RFID, ParkingLotID, PlateNumber, PlateImgURL, CheckInTime)
        if res != True:
            print('> Cannot allow vehicles to come in <%s> parking lot'%(ParkingLotID))    
        else:
            print('> Inserted parking')
            # Insert to HistoryTable: 
            res = history.insert(RFID, ParkingLotID, PlateNumber, PlateImgURL, StaffID, CameraID, True, CheckInTime)
            if res != True:
                print('> Cannot add history')
            else:
                print('> Inserted History')

    # print(yoloPlate)
    # print(characterRecognition)


if __name__ == '__main__':
    main()