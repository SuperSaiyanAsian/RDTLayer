import random


# #################################################################################################################### #
# UnreliableChannel                                                                                                    #
#                                                                                                                      #
# Description:                                                                                                         #
# This class is meant to be more of a blackbox but you are allowed to see the implementation. You are not allowed to   #
# change anything in this file. There is also no need to base your algorithms on this particular implementation.       #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is not to be changed.                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class UnreliableChannel():
    RATIO_DROPPED_PACKETS = 0.1
    RATIO_DELAYED_PACKETS = 0.1
    RATIO_DATA_ERROR_PACKETS = 0.1
    RATIO_OUT_OF_ORDER_PACKETS = 0.1
    ITERATIONS_TO_DELAY_PACKETS = 5

    def __init__(self, canDeliverOutOfOrder_, canDropPackets_, canDelayPackets_, canHaveChecksumErrors_):
        self.sendQueue = []
        self.receiveQueue = []
        self.delayedPackets = []
        self.canDeliverOutOfOrder = canDeliverOutOfOrder_
        self.canDropPackets = canDropPackets_
        self.canDelayPackets = canDelayPackets_
        self.canHaveChecksumErrors = canHaveChecksumErrors_
        # stats
        self.countTotalDataPackets = 0
        self.countSentPackets = 0
        self.countChecksumErrorPackets = 0
        self.countDroppedPackets = 0
        self.countDelayedPackets = 0
        self.countOutOfOrderPackets = 0
        self.countAckPackets = 0
        self.currentIteration = 0

    def send(self,seg):
        self.sendQueue.append(seg)

    def receive(self):
        new_list = list(self.receiveQueue)
        self.receiveQueue.clear()
        #print("UnreliableChannel len receiveQueue: {0}".format(len(self.receiveQueue)))
        return new_list

    def processData(self):
        #print("UnreliableChannel manage - len sendQueue: {0}".format(len(self.sendQueue)))
        self.currentIteration += 1

        if len(self.sendQueue) == 0:
            return

        if self.canDeliverOutOfOrder:
            val = random.random()
            if val <= UnreliableChannel.RATIO_OUT_OF_ORDER_PACKETS:
                self.countOutOfOrderPackets += 1
                self.sendQueue.reverse()

        # add in delayed packets
        noLongerDelayed = []
        for seg in self.delayedPackets:
            numIterDelayed = self.currentIteration - seg.getStartDelayIteration()
            if (numIterDelayed) >= UnreliableChannel.ITERATIONS_TO_DELAY_PACKETS:
                noLongerDelayed.append(seg)

        for seg in noLongerDelayed:
            self.countSentPackets += 1
            self.delayedPackets.remove(seg)
            self.receiveQueue.append(seg)

        for seg in self.sendQueue:
            #self.receiveQueue.append(seg)

            addToReceiveQueue = False
            if self.canDelayPackets:
                val = random.random()
                if val <= UnreliableChannel.RATIO_DELAYED_PACKETS:
                    self.countDelayedPackets += 1
                    seg.setStartDelayIteration(self.currentIteration)
                    self.delayedPackets.append(seg)
                    continue

            if self.canDropPackets:
                val = random.random()
                if val <= UnreliableChannel.RATIO_DROPPED_PACKETS:
                    self.countDroppedPackets += 1
                else:
                    addToReceiveQueue = True
            else:
                addToReceiveQueue = True

            if addToReceiveQueue:
                self.receiveQueue.append(seg)
                self.countSentPackets += 1

            if seg.acknum == -1:
                self.countTotalDataPackets += 1

                # only data packets can have checksum errors...
                if self.canHaveChecksumErrors:
                    val = random.random()
                    if val <= UnreliableChannel.RATIO_DATA_ERROR_PACKETS:
                        seg.createChecksumError()
                        self.countChecksumErrorPackets += 1

            else:
                # count ack packets...
                self.countAckPackets += 1

            #print("UnreliableChannel len receiveQueue: {0}".format(len(self.receiveQueue)))

        self.sendQueue.clear()
        #print("UnreliableChannel manage - len receiveQueue: {0}".format(len(self.receiveQueue)))
