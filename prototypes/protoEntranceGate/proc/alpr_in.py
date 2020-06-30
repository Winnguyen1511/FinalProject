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
import argparse


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
    #Simulate the image read from camera,
    #Here we just get img from a directory:
    im = cv2.imread(imgName)
    if show == True:
        w = im.shape[1]
        h = im.shape[0]
        im_tmp = QImage(im.data, w,h, QImage.Format_RGB888).rgbSwapped()
        UI.lbEntranceImg.setPixmap(QPixmap.fromImage(im_tmp))
        # imshow(im)

    #Save image to the image location:
    #This can be saved as AWS W3 service later:
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
    print('> Skip...')
    global state, skip_plate
    if state == DATABASE_STATE:
        skip_plate = True

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='Enter database!')
    parser.add_argument('-U', '--username', help='Enter username!')
    parser.add_argument('-W', '--password', help='Enter password!')
    parser.add_argument('-p', '--port', help='Enter port!')
    parser.add_argument('-H', '--host', help='Enter hostname!')
    args = parser.parse_args()
    if args.database:
        database = args.database
    else:
        database = psq.DEFAULT_DATABASE
    
    if args.username:
        username = args.username
    else:
        username = psq.DEFAULT_USERNAME

    if args.password:
        password = args.password
    else:
        password = psq.DEFAULT_PASSWORD
    
    if args.port:
        port = args.port
    else:
        port = psq.DEFAULT_PORT
    
    if args.host:
        host = args.host
    else:
        host = psq.DEFAULT_HOST

    #Init GUI: 
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AE.Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.btnEnter.clicked.connect(btnEnterCallback)
    ui.btnSkip.clicked.connect(btnSkipCallback)
    
    MainWindow.show()
    # global exit_status
    exit_status = False
    # error_status = False
    # The AI Core Thread:
    ui.setNotifications('Initializing. Please wait...')
    def running_thread_func():
        if exit_status == True:
            return True
        ###########################################################################
        #Init the AI Core system:
        
        ## 1) Connect to database:
        ret, conn, cur = psq.login_database(database, username, password, host, port)
        if ret == True:
            print('> Logged in successful to <%s>'%(username))
        else:
            print('> Error: Log in error to <%s>'%(username))
            # ui.msg_box('Error: Log in error to <'+username+'>', detail=str(ret))
            print('>Exit...')
            # error_status = True
            ## Quit the app immediately.
            # MainWindow.close()
            return False
        parking = ParkingTable(conn, cur)
        history = HistoryTable(conn,cur)


        ## 2) Load model for AI modules:
        yoloPlate, characterRecognition = pr.sysInit_Default()
        if yoloPlate == False:
            print('> Error: loading database for AI Core')
            # ui.msg_box('> Error: loading database for AI Core', detail=str(characterRecognition))
            # app.quit()
            # MainWindow.close()
            # error_status = True
            return False

        os.chdir(DEFAULT_WORKSPACE)
        ## 3) Simulate the data for recognition:
        lstImg = [name for name in os.listdir() if name.endswith('.jpg') 
                                                or name.endswith('.jpeg')
                                                or name.endswith('.png')
                                                or name.endswith('.raw')]
        

        ## 4) Get Information of the working session:
        StaffID = getStaffID()
        ui.lbStaffDesc.setText(StaffID)
        ParkingLotID = getParkingLotID()
        ui.lbParkingLotDesc.setText(ParkingLotID)
        CameraID = getCameraID()
        ui.lbCameraDesc.setText(CameraID)


        for imgName in lstImg:
            global semaphore, skip_plate, state
            # Load image, recognize the plate number:
            ui.lbEntranceImg.setPixmap(QtGui.QPixmap(""))
            ui.lbRFIDDesc.setText("")

            ui.lbPlateNumberDesc.setText('Press [Enter]')
            print('> Press [ENTER] to load img:')
            ui.setNotifications('Press [ENTER] to get new car.')
            state = SCAN_STATE
            semaphore = 0
            while semaphore == 0:
                if exit_status == True:
                    return True
                # print('.')
                # time.sleep(3)
            ui.setNotifications('Please wait...')
            RFID = getRFID()
            ui.lbRFIDDesc.setText(RFID)
            PlateImgURL = getImg(imgName,ui,  show=True)
            _,PlateNumber = pr.plateRecog(PlateImgURL, yoloPlate, characterRecognition, show=False)
            ui.lbPlateNumberDesc.setText(PlateNumber)
            
            print('Plate number:', PlateNumber)
            
            CheckInTime = DT.now()
            
            state = DATABASE_STATE
            # choice = input('> Press [ENTER] to allow vehicles in:')
            print('> Press [ENTER] to allow vehicles in:')
            ui.setNotifications('Please Check the plate number again\n'
            'Press [ENTER] to allow vehicles in\n'
            'Press [SKIP] to reject vehicles')
            semaphore = 0
            while semaphore == 0:
                if skip_plate == True:
                    # skip_plate = False
                    break
                if exit_status == True:
                    return True
                # print('.')
                # time.sleep(3)
            if skip_plate == True:
                print('> Skipping plate <%s>'%(PlateNumber))
                ui.setNotifications('Skipped plate <'+PlateNumber+'>')
                skip_plate = False
                continue
            ui.setNotifications('Please wait...')
            # Insert to ParkingTable:
            PlateNumber = ui.lbPlateNumberDesc.text()

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
            
            ui.lbPlateNumberDesc.setText('Press [Enter]')
            
    t = threading.Thread(target=running_thread_func)
    t.start()
    app.exec_()
    exit_status = True


if __name__ == '__main__':
    main()
    
    