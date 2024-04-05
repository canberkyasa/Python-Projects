# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 16:00:07 2024

@author: canbo

Finding and moving desired file in desired path to destination path

"""
import datetime
import os

def findFilesAndMove(fName:str,downloadPath:str,destinationPath:str) -> bool:
    
    startingTime = datetime.datetime.now()
    terminationLength = datetime.timedelta(hours=1,minutes=30)
    terminationTime = startingTime + terminationLength
    
    while terminationTime > startingTime:
        for file in os.listdir(downloadPath):
            if file.startswith(fName):
                os.rename(downloadPath + "\\" + str(file), destinationPath + "\\" + str(file))
                return True

    return False