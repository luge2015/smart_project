#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
    Read.py
    ~~~~~~~~~~~~~~~~
    Rfid read ic module.
    :copyright: (c) 2017 by jxg.
'''

import signal
import logging
import os

from pymongo import MongoClient

import RPi.GPIO as GPIO
from vender import MFRC522
import errors

logger = logging.getLogger(__name__)

client = MongoClient('0.0.0.0',27017)
db_name = 'RFID_card'
db = client[db_name]
collection_card_num = db['card_num']

da = []
de = []

start_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame,continue_reading):
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."


# This loop keeps checking for chips. If one is near it will get the UID and authenticate

"""
读第二块数据，对应存储在s50卡的第12个数据区
"""

def read_second_block(start_reading):
    global  result
    while start_reading:

        # Scan for cards
        status,TagType = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"

        # Get the UID of the card
        status,uid = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            da = []
            de = []
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 12, key, uid)
            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                try:
                    data = MIFAREReader.MFRC522_Read(12)
                    logger.info('===== log-MFRC522_Read: ===== %s', data)
                except IOError:
                    print 'Can not find card or your card is damaged.'
                    result = errors.ErrorReadNotFind()
                    logger.error('===== log-error: ===== %s', result)
                except Exception as e:
                    print 'Exception :',e
                    result = errors.ErrorReadFailedUnknow()
                    logger.error('===== log-error: ===== %s', result)
                print 'The data after change:'
                asci = set([i for i in range(127)])
                ddata = set(data)
                if ddata.issubset(asci):
                    for i in range(len(data)):
                        de.append(chr(data[i]))
                        #da.append(data[i].decode('utf-8'))
                        #print data[i].decode('utf-8')
                    print de
                else:
                    for i in range(len(data)-2):
                        if i%3==0:
                            #da.append((chr(data[i])+chr(data[i+1])+chr(data[i+2])).decode('utf-8'))
                            print (chr(data[i])+chr(data[i+1])+chr(data[i+2])).decode('utf-8')
                        #print da
                MIFAREReader.MFRC522_StopCrypto1()
            else:
                print "Authentication error"
                result = errors.ErrorAuthenticationErr()
                logger.error('===== mss-not-found: ===== %s',result)

            #db.collection_card_num.drop()
            # u = dict(name=uid,chunk=2,num = de)
            # db.collection_card_num.insert(u)
            l = db.card_s.find_one({'uid':uid,'chunk':2},{'num':1,'_id':0})
            nnum = l.get('num',0)
			
            '''file_object = open('file.txt','a+')
            try:
                file_object.write(str(nnum))
            finally:
                file_object.close()
            '''
            return nnum
            start_reading = False


