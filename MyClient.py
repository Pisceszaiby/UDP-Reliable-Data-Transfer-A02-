from socket import *
from BadNet5 import *
import hashlib
import pickle
import sys
#importing libraries
serverName= "127.0.0.1"
serverPort=int(sys.argv[1])
file = ''.join(sys.argv[2])
clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(0.001)
seqNum=1
fileOpen= open(file, 'rb')
data = fileOpen.read(1000)  #opening file to be sent
read = False
currentPkt=[]
exception=False

while not read: #while file is not completely read
    if not exception: # if ack of previous packet is rec 
      sendPacket=[] #packet in the form of array
      sendPacket.append(seqNum) #add sequence number
      sendPacket.append(data) #add content
      h=hashlib.md5() #encryption and calculating checksum
      h.update(pickle.dumps(sendPacket))
      sendPacket.append(h.digest())
      BadNet.transmit(clientSocket,pickle.dumps(sendPacket),serverName,serverPort)
      print("Sequence Number of Packet Sent by Client: ",seqNum)
      if(not data): #if no more data
        read=True #file completely read
      data=fileOpen.read(1000)
      currentPkt=sendPacket   
    try:
        #ACKNOWLEDGEMENT RECEIPT
      ack1=[]
      ack,sendAddress=clientSocket.recvfrom(4096)
      #if ack is received, before timeout try block will run otherwise except block will run
      ack1=pickle.loads(ack)
      seqNum+=1 #after succesful recceipt of ack
      currentPkt.clear() #clear the current packet
      exception=False    #as exception has not occured
    except:
      BadNet.transmit(clientSocket,pickle.dumps(currentPkt),serverName,serverPort) #transmit current packet again, as ack is not rec before timeout
      print("Sequence Number of Packet Sent by Client: ",seqNum)
      exception=True #as exception has occuured
      continue #continue to next iteration

fileOpen.close() #close file
print("Connection Closed")
clientSocket.close() #close connection
