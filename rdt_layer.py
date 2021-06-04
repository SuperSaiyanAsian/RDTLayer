from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None                                  # Channel to send data through
    receiveChannel = None                               # Channel to receive data through
    dataToSend = ''                                     # The data to send
    countSegmentTimeouts = 0                            # Total segment timeouts
    # Add items as needed
    currentTimeouts = 0                                 # Current segment timeout iteration
    sentData = 0                                        # Number of characters sent
    seqCount = 1                                        # Keeps track of current sequence number
    ackCount = 1                                        # Keeps track of current acknowledgement number
    cumulativeAck = 1                                   # Used to implement cumulative ack
    flowCheck = 0                                       # Ensures that pipeline segments fit the flow-control window
    packetNum = 0                                       # Keeps track of the number of the current packet in the pipeline
    isServer = False                                    # Used to differentiate between client and server
    payloadList = []                                    # List of uncorrupted payloads
    successPackets = []                                 # List of packets successfully received by the server
    cachedSeqs = []                                     # List of sequence numbers successfully received by the server
    cachedSeqNums = []                                  # Temporary list of sequence numbers successfully received by the server (Used to prevent duplicates from being added to payloadList)
    uncorruptedSegs = []                                # Temporary list of segments received by the server that have not been corrupted
    

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.countSegmentTimeouts = 0
        # Add items as needed
        self.currentTimeouts = 0
        self.sentData = 0
        self.seqCount = 1
        self.ackCount = 1
        self.cumulativeAck = 1
        self.flowCheck = 0
        self.packetNum = 0
        self.isServer = False
        self.payloadList = []
        self.successPackets = []
        self.cachedSeqs = []
        self.cachedSeqNums = []
        self.uncorruptedSegs = []

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        # print('getDataReceived(): ' + self.dataToSend)

        # ############################################################################################################ #
        return self.dataToSend

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):

        # ############################################################################################################ #

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        # If no data to send at first, then this must be the server
        if(self.dataToSend == ''):
            self.isServer = True

        else:  
            if(self.isServer is False):

                # Ensure that only 15 characters of data are sent in one pipeline
                while(self.flowCheck < self.FLOW_CONTROL_WIN_SIZE):
                    segmentSend = Segment()                         # Moved inside while loop to prevent segments from being overwritten
                                                                    # Reference: https://edstem.org/us/courses/5258/discussion/412270
        
                    data = ""                                       # 3 or 4 characters to be sent
                    sentChars = 0                                   # Number of characters sent
                    
                    # Check if a segment has timed out so it can be selectively retransmitted
                    if(self.currentTimeouts > 0):
                        
                        x = 1
                        isComplete = False                          # Checks whether to send a full packet of 4 characters or just 3
                        seqnum = self.ackCount
                        
                        # Use the seqnum to decide whether to send complete packets or not
                        while(x < len(self.dataToSend) + 1):
                            if(x == seqnum):
                                isComplete = True
                                break
                            
                            x += self.DATA_LENGTH
                            if(x == seqnum):
                                isComplete = True
                                break

                            x += self.DATA_LENGTH
                            if(x == seqnum):
                                isComplete = True
                                break

                            x += self.DATA_LENGTH
                            if(x == seqnum):
                                break
                            
                            x += self.DATA_LENGTH - 1

                        if(isComplete):
                            lowerBound = seqnum - 1
                            upperBound = seqnum + 3

                            # Increment flow-control checker
                            self.flowCheck += 4
                        
                        else:
                            lowerBound = seqnum - 1
                            upperBound = seqnum + 2

                            # Increment flow-control checker
                            self.flowCheck += 3

                        # Ensure that the string index will not be out of range
                        while(upperBound > len(self.dataToSend)):
                            upperBound -= 1
                        
                        # Take 3 or 4 chars to send
                        for i in range(lowerBound, upperBound):
                            data += self.dataToSend[i]
                        
                        # Reset timeout timer
                        self.currentTimeouts = 0
            
                        # ############################################################################################################ #
                        # Display sending segment
                        segmentSend.setData(seqnum,data)
                        print("Retransmitting segment: ", segmentSend.to_string())
            
                        # Use the unreliable sendChannel to send the segment
                        self.sendChannel.send(segmentSend)

                    # Send new segments
                    elif(self.sentData < len(self.dataToSend)):
                        seqnum = self.seqCount
                        lowerBound = self.sentData

                        self.packetNum += 1
                          
                        # Send 3 characters of data for every 4th new packet
                        if(self.packetNum == 4):
                            self.seqCount += self.DATA_LENGTH - 1
                            upperBound = self.sentData + self.DATA_LENGTH - 1
                            self.packetNum = 0
                        
                        # Otherwise, send the complete 4 characters
                        else:
                            self.seqCount += self.DATA_LENGTH
                            upperBound = self.sentData + self.DATA_LENGTH

                        # Prevent index errors
                        while(upperBound > len(self.dataToSend)):
                            upperBound -= 1

                        # Take 3 or 4 characters to send
                        for i in range(lowerBound, upperBound):
                            data += self.dataToSend[i]
                            sentChars += 1
            
                        # Increment total data sent with the amount that was just sent
                        self.sentData += sentChars

                        # Increment flow-control checker
                        self.flowCheck += sentChars
            
                        # ############################################################################################################ #
                        # Display sending segment
                        segmentSend.setData(seqnum,data)
                        print("Sending segment: ", segmentSend.to_string())
            
                        # Use the unreliable sendChannel to send the segment
                        self.sendChannel.send(segmentSend)
                    
                    # If nothing to send, close flow-control window
                    else:
                        self.flowCheck = 15

                # Reset flow-control checker
                self.flowCheck = 0

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        
        acknum = -1

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented

        # Check if server
        if(self.isServer):
            listIncomingSegments.sort(key=lambda x: x.seqnum)           # Sort segments based on sequence number
                                                                        # Reference: https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
            
            self.uncorruptedSegs.clear()                                # Clear list

            for i in listIncomingSegments:
                if(i.payload.find('X') == -1):                          # Check if data contains an 'X'
                                                                        # If so, then data is corrupted and should be discarded
                                                                        # Reference: https://www.w3schools.com/python/ref_string_find.asp
                    if(i not in self.successPackets):
                        self.successPackets.append(i)
                
                    self.uncorruptedSegs.append(i)

            listIncomingSegments.clear()                                # Clear list

            # Make list of received segments have only uncorrupted segments
            for i in self.uncorruptedSegs:
                listIncomingSegments.append(i)

            self.successPackets.sort(key=lambda x: x.seqnum)            # Sort segments based on sequence number
            self.cachedSeqNums.clear()                                  # Clear list
            self.payloadList.clear()                                    # Clear list

            # Transfer only unique payloads to list of payloads
            for i in self.successPackets:
                if(i.seqnum not in self.cachedSeqNums):
                    self.cachedSeqNums.append(i.seqnum)
                    self.payloadList.append(i.payload)
                        
            self.dataToSend = ""                                        # Empty current data to send

            # Finalize data to send
            for i in self.payloadList:
                self.dataToSend += i
        
        # Client
        else:
            listIncomingSegments.sort(key=lambda x: x.startIteration)   # Sort received packets from server

            # Process received packets and find out current ack number and if a segment needs to be resent
            for i in listIncomingSegments:
                self.ackCount = i.acknum
                self.currentTimeouts += i.startIteration
                self.countSegmentTimeouts += i.startIteration
                if(self.ackCount < len(self.dataToSend) and self.sentData == len(self.dataToSend)):
                    self.currentTimeouts += 1
                    self.countSegmentTimeouts += 1

        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segments?

        ### My implementation has the client only sending data and the server mainly sending acks
        ### so the type of segment depends whether the recipient is the client or the server
        ### The isServer boolean determines this
        
        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        
        if(self.isServer):
            for i in listIncomingSegments:
                segmentAck = Segment()                              # Segment acknowledging packet(s) received
                                                                    # Moved inside while loop to prevent segments from being overwritten
                                                                    # Reference: https://edstem.org/us/courses/5258/discussion/412270
                
                acknum = self.ackCount

                # If expected segment, then cache its sequence number and increment ack number accordingly.
                if(i.seqnum == acknum):
                    self.cachedSeqs.append(i.seqnum)
                    self.ackCount += len(i.payload)
                    acknum = self.ackCount
                
                # If unexpected segment, then start timeout timer
                else:
                    segmentAck.startIteration = 1

                # If next expected segment has already been received, then set ack to next expected unreceived segment
                if(acknum in self.cachedSeqs):
                    x = 1
                    uncachedSeq = 0
                    self.cachedSeqs.sort()
                    while(x != self.cachedSeqs[-1]):

                        x += self.DATA_LENGTH

                        if(x not in self.cachedSeqs):
                            uncachedSeq = 1  
                            break 

                        x += self.DATA_LENGTH

                        if(x not in self.cachedSeqs):
                            uncachedSeq = 1  
                            break 

                        x += self.DATA_LENGTH

                        if(x not in self.cachedSeqs):
                            uncachedSeq = 1  
                            break

                        x += self.DATA_LENGTH - 1

                        if(x not in self.cachedSeqs):
                            uncachedSeq = 1  
                            break                          

                    # Set ack to cumulative ack if all previous data have been received
                    if(uncachedSeq == 0):
                        self.ackCount = self.cumulativeAck
                        acknum = self.cumulativeAck
                    
                    else:
                        self.ackCount = x
                        acknum = x
                
                # Increment cumulative ack
                if(i.seqnum >= self.cumulativeAck):
                    if(i.seqnum not in self.cachedSeqs):
                        self.cachedSeqs.append(i.seqnum)                        
                    self.cumulativeAck = i.seqnum + len(i.payload)       

                # ############################################################################################################ #
                # Display response segment
                segmentAck.setAck(acknum)
                print("Sending ack: ", segmentAck.to_string())
        
                # Use the unreliable sendChannel to send the ack packet
                self.sendChannel.send(segmentAck)
            
            # Ensure that client knows current ack number even if client stops sending segments
            if(len(listIncomingSegments) == 0):
                segmentAck = Segment()

                segmentAck.startIteration = 1
                acknum = self.ackCount

                # ############################################################################################################ #
                # Display response segment
                segmentAck.setAck(acknum)
                print("Sending ack: ", segmentAck.to_string())
        
                # Use the unreliable sendChannel to send the ack packet
                self.sendChannel.send(segmentAck)