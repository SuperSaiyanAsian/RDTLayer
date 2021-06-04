import random
from functools import reduce


# #################################################################################################################### #
# Segment                                                                                                              #
#                                                                                                                      #
# Description:                                                                                                         #
# The segment is a segment of data to be transferred on a communication channel.                                       #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is not to be changed.                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class Segment():

    def __init__(self):
        self.seqnum = -1
        self.acknum = -1
        self.payload = ''
        self.checksum = 0
        self.startIteration = 0
        self.startDelayIteration = 0

    def setData(self,seq,data):
        self.seqnum = seq
        self.acknum = -1
        self.payload = data
        self.checksum = 0
        str = self.to_string()
        self.checksum = self.calc_checksum(str)

    def setAck(self,ack):
        self.seqnum = -1
        self.acknum = ack
        self.payload = ''
        self.checksum = 0
        str = self.to_string()
        self.checksum = self.calc_checksum(str)

    def setStartIteration(self,iteration):
        self.startIteration = iteration

    def getStartIteration(self):
        return self.startIteration

    def setStartDelayIteration(self,iteration):
        self.startDelayIteration = iteration

    def getStartDelayIteration(self):
        return self.startDelayIteration

    def to_string(self):
        return "seq: {0}, ack: {1}, data: {2}"\
        .format(self.seqnum,self.acknum,self.payload)

    def checkChecksum(self):
        cs = self.calc_checksum(self.to_string())
        return cs == self.checksum

    def calc_checksum(self,str):
        return reduce(lambda x,y:x+y, map(ord, str))

    def printToConsole(self):
        print(self.to_string())

    # Function to cause an error - Do not modify
    def createChecksumError(self):
        if not self.payload:
            return
        char = random.choice(self.payload)
        self.payload = self.payload.replace(char, 'X', 1)