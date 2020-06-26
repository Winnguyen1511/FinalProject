import platerecognition as pr
import recognitionmodules as rm
import PostgreSQLQuery as psq
from Tables.Table import *
import os
import cv2
import math
from datetime import datetime as DT
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import alpr_entrance as AE
from PyQt5.QtGui import QImage, QPixmap
from multiprocessing import Process
import time
INIT_STATE = 0
SCAN_STATE = 1
DATABASE_STATE = 2

semaphore = 0

state = INIT_STATE

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

def getImg(imgName,UI,  show=True):
    im = cv2.imread(imgName)
    if show == True:
        w = im.shape[1]
        h = im.shape[0]
        im_tmp = QImage(im.data, w,h, QImage.Format_RGB888).rgbSwapped()
        UI.lbEntranceImg.setPixmap(QPixmap.fromImage(im_tmp))
        # imshow(im)
    saveName = DEFAULT_SAVE_DIR +'in_'+ imgName
    if not os.path.isdir(DEFAULT_SAVE_DIR):
        os.mkdir(DEFAULT_SAVE_DIR)
    cv2.imwrite(saveName, im)
    return saveName

def btnEnterCallback():
    print('> Enter...')
    global semaphore
    semaphore = 1

skip_plate = False
def btnSkipCallback():
    pass

def sysLogin():
    #Simulate loging process
    print('> Logged in!')
    return True
def getStaffID():
    return 'STF001'
def getCameraID():
    return 'CM0001'

def main():
    #Init GUI: 
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AE.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.btnEnter.clicked.connect(btnEnterCallback)
    ui.btnSkip.clicked.connect(btnSkipCallback)
    # t = threading.Thread(target=MainWindow.show)
    # t.start()
    # p = Process(target=MainWindow.show, args=())
    # p.start()
    MainWindow.show()
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
    def running_thread_func():
        for imgName in lstImg:
            global semaphore
            # Load image, recognize the plate number:
            # choice = input('> Press [ENTER] to load img:')
            print('> Press [ENTER] to load img:')
            state = SCAN_STATE
            semaphore = 0
            while semaphore == 0:
                print('.')
                time.sleep(1)
            # if choice == '0':
            #     print('> Exiting...')
            #     break
            RFID = getRFID()
            PlateImgURL = getImg(imgName,ui,  show=True)
            _,PlateNumber = pr.plateRecog(PlateImgURL, yoloPlate, characterRecognition, show=False)
            ParkingLotID = getParkingLotID()
            CheckInTime = DT.now()
            StaffID = getStaffID()
            # print(StaffID)
            CameraID = getCameraID()
            # cv2.waitKey(0)
            state = DATABASE_STATE
            # choice = input('> Press [ENTER] to allow vehicles in:')
            print('> Press [ENTER] to allow vehicles in:')
            semaphore = 0
            while semaphore == 0:
                print('.')
                time.sleep(1)

            # cv2.destroyAllWindows()
            # if choice == '0':
            #     print('> Canceled!')
            #     continue
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
    t = threading.Thread(target=running_thread_func)
    t.start()
    sys.exit(app.exec_())
    # print(yoloPlate)
    # print(characterRecognition)


if __name__ == '__main__':
    
    main()
    
    