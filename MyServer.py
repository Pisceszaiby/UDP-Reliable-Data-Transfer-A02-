from socket import *
import pickle
import hashlib
import time
import sys
serverIP="127.0.0.1"
serverPort=12000
serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((serverIP,serverPort))
#Settimeout serves as a timeout
serverSocket.settimeout(1)
print ("Ready to serve")

expectedSeqNum=1 #Expected sequence number of received Packet
f = open("cnout.pdf", "wb")
endOfFile = False #to check if the file is read completely or not
starttime = time.time() #Record time when connection is established

while not endOfFile: #while there is data to be received (client file has not been completely read)
    try:
        receivePacket=[] #received packet to be stored in array
        packet,clientAddress= serverSocket.recvfrom(4096) #packet reception
        receivePacket=pickle.loads(packet)        
        checksumRec=receivePacket[-1] #stores checksum (that was calculated at client side)
        del receivePacket[-1] #deletes attached checksum 
        hash = hashlib.md5() #encryption,calculates new checksum
        hash.update(pickle.dumps(receivePacket))
        print("Server Expected Number :",expectedSeqNum)
        if checksumRec==hash.digest(): #if both checksums match
            if(receivePacket[0]==expectedSeqNum): #if the recieved sequence number matches expected sequence number
                print("Received Inorder")               
                if receivePacket[1]: #if received packet still contains data
                    f.write(receivePacket[1]) #write onto output file
                    expectedSeqNum+=1
                else:
                    endOfFile=True
                ack=True
                ackSend=[]
                ackSend.append(ack) #send acknowledgement for recieved inorder packet
                serverSocket.sendto(pickle.dumps(ackSend),(clientAddress[0],clientAddress[1]))
            else:
                print("Received Out of Order") #if sequence numbers do not match
                if not receivePacket[1]: #if no data in packet
                    endOfFile=True
                ackSend.clear()
        else: #if checksums do not match (bit corruption)
            print("Error Detected")           
            
    except:  
         #packet not received before timeout
        if endOfFile:
                break
endtime=time.time()
f.close() #close output file
print("File Transferred Successfully")
print("Time Taken in seconds: ", str(endtime-starttime))

