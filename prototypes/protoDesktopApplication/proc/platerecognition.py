
from darkflow.net.build import TFNet
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import cv2
import imutils
import argparse
import math
import recognitionmodules as rm
import timeit
import time
import os
import datetime

from progress.bar import IncrementalBar

# #Old database
# MIN_WIDTH = 400
# MIN_HEIGHT = 220

# MAX_WIDTH = 2100
# MAX_HEIGHT = 1000


#New Database
MIN_WIDTH = 460
MIN_HEIGHT = 100

MAX_WIDTH = 1200
MAX_HEIGHT = 290

# #New Database
# MIN_WIDTH = 230
# MIN_HEIGHT = 50

# MAX_WIDTH = 600
# MAX_HEIGHT = 145
# dir = '/home/khoa/AI_DeepLearning/LicensePlateRecognition/LicensePlateRecognition/'
dir = os.getcwd()+'/'
workspace = dir+'resources/'

platePbDir = dir +'database/protobuf/yolo-plate.pb'
plateMetaDir = dir+'database/meta/yolo-plate.meta'

charCnnDir = dir+'database/character_recognition.h5'
testmode = 'test'
gpuMode = 0.1
testfile = dir+'resources/data'

def sysInit_Default():
    try:
        plateOptions = {"pbLoad": platePbDir, "metaLoad": plateMetaDir, "gpu": gpuMode}
        yoloPlate = TFNet(plateOptions)
        characterRecognition = tf.keras.models.load_model(charCnnDir)
    except Exception as e:
        return False, e
    return yoloPlate, characterRecognition

def sysInit(platePb, plateMeta, charCnn, gpu):
    try:
        plateOptions = {"pbLoad": platePb, "metaLoad": plateMeta, "gpu": gpu}
        yoloPlate = TFNet(plateOptions)
        characterRecognition = tf.keras.models.load_model(charCnn)
    except Exception as e:
        print('>Error...')
        return False, e
    return yoloPlate, characterRecognition

def plateRecogTest(yoloPlate, characterRecognition, testfile):
    print(">> Testing mode:")

    testList = {}
    file = open(testfile, 'r')
    line =file.readline()
    while line and line != '\n':
        entry = line.split(" ")
        tmp = {entry[0]: entry[1].strip('\n')}
        testList.update(tmp)
        line =file.readline()
    # print(testList)
    total = len(testList)
    resManLen = [len(testList[key]) for key in testList]
    totalLen = sum(resManLen)
    #Stat for overall:
    countOpenCV = 0
    #Stat for character recognition:
    countSegmentedOpenCV = 0
    countSuccessCharOpenCV = 0
    #Stat for character segmentation:
    countSegOpenCV = 0

    bar = IncrementalBar('Tesing', max=total)
    t = datetime.datetime.now()
    logname = 'log'+t.strftime("%y_%m_%d_%H%M%S")
    logfile = open(logname, 'w')

    for key in testList.keys():
        resMan = testList[key]
        _, resOpenCV = plateRecog(key,yoloPlate, characterRecognition, show=False)

        if resOpenCV == resMan:
            countOpenCV += 1
        if(len(resOpenCV) == len(resMan)):
            countSegOpenCV += 1
            countSegmentedOpenCV += len(resMan)
            for i in range(0,len(resOpenCV)):
                if resOpenCV[i] == resMan[i]:
                    countSuccessCharOpenCV += 1
        tmp = key+' man:'+resMan+' opencv:'+resOpenCV+'\n'
        logfile.write(tmp)
        bar.next()
    bar.finish()
    logfile.close()
    print(">> Testing Finished!")
    print(">> Statistic: ")
    print("> Overall:")
    print("OpenCV: %.2f %%"%(countOpenCV*100/total))
    print("> Character segmentation: ")
    print("OpenCV:%.2f %%"%(countSegOpenCV*100/total))
    print("> Character recognition: ")
    if countSegmentedOpenCV !=0 :
        print("OpenCV:%.2f %%"%(countSuccessCharOpenCV*100/countSegmentedOpenCV))
    else:
        print("OpenCV:0%")

def plateRecog(image, yoloPlate, characterRecognition, show=True):
    #Init the recognition configuration:
    
    #Start:
    im = cv2.imread(image)
    if type(im) == type(None):
        print("> Error: Cannot read/find image ", image)
        return False
    
    #Plate detection by YOLO:
    platePrediction = yoloPlate.return_predict(im)
    # print(len(platePrediction))
    #Crop the plate out and second crop to reduce some background:
    resultOpenCV = ""
    if len(platePrediction) > 0:
        im = rm.firstCrop(im, platePrediction, show=show)
        if show == True:
            cv2.imshow('firstCrop', im)
        # cv2.imwrite('test.jpg', im)
    im = rm.secondCrop(im, show=show)
    # cv2.imwrite('test2.jpg', im)


#resize the capture of plate before we detect the character:
    imsize = im.shape
    w = imsize[1]
    h = imsize[0]
    if(show== True):
        print(">>Origin: Width: ", w, ", Height: ", h)
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
    if show == True:
        print(">>Scale up: Width: ", w, ", Height: ", h)
    im = cv2.resize(im, (w, h), interpolation=cv2.INTER_CUBIC)
    
    resultOpenCV = rm.opencvReadPlate(im, characterRecognition, show=show)
    if show == True:
        print(">>Plate number OpenCV: ", resultOpenCV)
    
    return True, resultOpenCV


def main():
    #arguments parser:
    # parser = argparse.ArgumentParser()
    # parser.add_argument("workspace")
    # parser.add_argument("platePb")
    # parser.add_argument("plateMeta")
    # parser.add_argument("charCnn")
    # parser.add_argument("gpuMode")
    # parser.add_argument("testmode")
    # parser.add_argument("testfile")
    # args = parser.parse_args()
    # workspace = args.workspace
    os.chdir(workspace)
    
    # platePbDir = args.platePb
    # plateMetaDir = args.plateMeta

    # charPbDir = args.charPb
    # charMetaDir = args.charMeta

    # charCnnDir = args.charCnn

    # gpuMode = float(args.gpuMode)

    # testmode = args.testmode
    # testfile =args.testfile
    #Start to run the program:
    yoloPlate, characterRecognition = sysInit(platePbDir, plateMetaDir,
                charCnnDir, gpuMode)
    # yoloPlate, characterRecognition = sysInit_Default()
    for i in range(0,5):    
        print(".")
    time.sleep(0.5)
    print(">>> Init Completed.")
    time.sleep(0.5)
    print(">>> Ready!")
    time.sleep(1)
    os.system('clear')
    print("*****PLATE RECOGNITION*****")
    print("> Workspace: ",workspace)
    print("> GPU mode: ", gpuMode * 100,"%")
    if(testmode == 'normal'):
        while(True):
            print("Please enter the image (0 or q to exit)")
            image = input("> Input image: ")
            if(image == '0' or image == 'q'):
                break 
            # image = workspace + image 
            start = timeit.default_timer()
            res, _ = plateRecog(image, yoloPlate, characterRecognition)
            stop = timeit.default_timer()
            print("Runtime: ", stop - start)
            if(res == True):
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print("******************************") 
        print(">>> Exiting...")
    elif testmode == 'test':
        if(testfile != ''):
            if(os.path.isfile(testfile) == False):
                print("Error: no such file or directory!")
            else:
                start = timeit.default_timer()
                plateRecogTest(yoloPlate, characterRecognition, testfile)
                stop = timeit.default_timer()
                print("Runtime: ", stop - start)
    else:
        print("Error: Wrong operation mode!")
    
    
# main()

