import os
import time

import datetime
import videosplit_sklearn as videosplit
import cv2
#import pymongo
import Launch
import pathlib



def mongo_connection():
    con = pymongo.MongoClient(host,27017)
    col = con[database][collection]
    return col


if __name__ == '__main__':
    name = str(input('Enter the name of the video: '))
    print("name_1: ", name)
    (vdolength,totalFrames) = videosplit.Launch(name)
    print("name_2: ", name)
    
    	
    os.chdir('data')
    path = pathlib.Path(__file__).parent.absolute()
    addition = "\\"
    path = str(path) + addition
    print("path: ", path) 
    

    result = {}
    result_imag = {}
    startTime = time.time()
    print("=======starttime: ", startTime)
    for f in os.listdir():
        print("dir: ",os.listdir()) 
        print("HHHHHHHHHHHHTest: ", path+f)
        pred, img = Launch.main(path+f)
        if pred in result.keys():
            result[pred] = result[pred] + 1
        elif pred != ' ':
            result[pred] = 1
            result_imag[pred] = img
           

    endTime = time.time()
    print("==================>endTime: ", endTime)
    l = {x: y for y, x in result.items()}
    r = list(sorted(l.keys()))
    index = r[len(r) - 1]
    plate = l[index]
    img = result_imag[plate]
    executionTime = "{0:.2f}".format(endTime - startTime)
    print('The name plate is :', plate, ' frequency is: ', result[plate])
    try:
        cv2.imshow('The plate', img)
    except:
        print("Problem in displaying license plate")
    print('execution time is : ' + executionTime)
    
    os.chdir('..')
    licensePlatePath = './LicensePlates/'+name.split('.')[0]+'.jpg'
    try:
        cv2.imwrite(licensePlatePath,img)
    except:
        print("Problem in writing license plate image")
    cv2.waitKey(0)
    for i in result.keys():
        print(i, ' : ', result[i])
        
    #storing data in database
    
    """
    host = 'localhost'
    database = 'ALPR'
    collection = 'videosTest'
    try:
        col = mongo_connection()
        dict = {}
        dict['date and time'] = time.ctime()
        dict['video'] = name
        dict['video length'] = vdolength
        dict['image'] = plate
        dict['Total Frames in video'] = totalFrames
        dict['execution_time'] = executionTime
        dict['frequency ratio'] = "{0:.2f}".format(result[plate] / len(result))
        
        col.insert(dict)
    except:
        print("error in mongodb connection or insertion")
        
    """
