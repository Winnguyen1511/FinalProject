import platerecognition as pr
import recognitionmodules as rm
import PostgreSQLQuery as psq
from Tables.Table import *
import os
import cv2
import math
from datetime import datetime as DT
import threading
import time
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

show_flag = False
show_ret = False
img_to_show = []
def imshow():
    global show_flag
    while True:
        if show_ret == True:
            return show_ret
        if show_flag == True:
            if len(img_to_show) > 0:
                obj = img_to_show.pop()
                im = obj[0]
                cmd = obj[1]
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
                cv2.imshow('Plate '+cmd, tmp)
            else:
                show_flag = False  
                cv2.waitKey(0)
             

def getImg(imgName, show=True):
    im = cv2.imread(imgName)
    # if show == True:
    #     t = threading.Thread(target=imshow, args=(im,))
    #     t.start()
    saveName = DEFAULT_SAVE_DIR +'out_'+ imgName
    if not os.path.isdir(DEFAULT_SAVE_DIR):
        os.mkdir(DEFAULT_SAVE_DIR)
    cv2.imwrite(saveName, im)
    return saveName

def sysLogin():
    #Simulate loging process
    print('> Logged in!')
    return True
def getStaffID():
    return 'STF002'
def getCameraID():
    return 'CM0002'

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
    yoloPlate, characterRecognition = pr.sysInit_Default()
    
    os.chdir(DEFAULT_WORKSPACE)
    lstImg = [name for name in os.listdir() if name.endswith('.jpg') 
                                            or name.endswith('.jpeg')
                                            or name.endswith('.png')
                                            or name.endswith('.raw')]
    parking = ParkingTable(conn, cur)
    history = HistoryTable(conn,cur)
    tshow = threading.Thread(target=imshow)
    tshow.start()
    for imgName in lstImg:
        choice = input('> Press [ENTER] to load img:')
        if choice == '0':
            print('> Exiting...')
            break
    
        RFID = getRFID()
        ParkingLotID = getParkingLotID()
        columns= 'platenumber, plateimgurl'
        conditions = "rfid='"+RFID+"' and parkinglotid='"+ParkingLotID+"'"
        records = parking.select(columns,conditions)
        if len(records) == 0:
            print('> Cannot find any match <rfid:%s> in <%s>'%(RFID,ParkingLotID))
            continue
        # record = records[0]
        inPlateNumber = records[0][0]
        print('in:'+inPlateNumber)
        inPlateImgURL = records[0][1]

        inImg = cv2.imread(inPlateImgURL)
        outImg = cv2.imread(imgName)
        _,outPlateNumber = pr.plateRecog(imgName, yoloPlate, characterRecognition, show=False)
        print('out:',outPlateNumber)
        
        img_to_show.append([inImg, 'in'])
        img_to_show.append([outImg, 'out'])
        global show_flag
        show_flag = True
        # cv2.waitKey(0)
        if inPlateNumber == outPlateNumber:
            print('> Plate Number matched!')
        else:
            print('> Plate Number not matched!')
            choice = input('> Press [ENTER] to cancel')
            if choice != '0':
                cv2.destroyAllWindows()
                print('> Cancelled!')
                continue
        choice = input('> Press [ENTER] ')
        cv2.destroyAllWindows()
        res = parking.delete(RFID, ParkingLotID)
        if res != True:
            print('> Cannot allow vehicles to come out <%s> parking lot'%(ParkingLotID))    
        else:
            print('> Delete parking')
        outPlateImgURL =getImg(imgName, show=False)
        StaffID =getStaffID()
        CameraID = getCameraID()
        CheckInTime = DT.now()
        res = history.insert(RFID, ParkingLotID,outPlateNumber,outPlateImgURL, StaffID,CameraID, False, CheckInTime)
        if res != True:
                print('> Cannot add history')
        else:
            print('> Inserted History')
    global show_ret
    show_ret = True
    
if __name__ == '__main__':
    main()