import socket
import sys
import numbers
import packet
import os
import pickle

sport_num_in = int(sys.argv[1])
sport_num_out = int(sys.argv[2])
cport_num_sin = int(sys.argv[3])
file_name = sys.argv[4]

HOST = '127.0.0.1'

def check_port_num(port_num):
    "Returns boolean value to check whether the port number is valid."
    
    return  (1024 < port_num < 64000) \
            and (isinstance(port_num, numbers.Integral))

port_nums = [sport_num_in, sport_num_out, cport_num_sin]
socket_names = ['s_in', 's_out', 'cs_in']
if len(set(port_nums)) != len(port_nums):
    print('port numbers are not unique, try again')
    sys.exit(1)

counter = 0
for i in port_nums:
    if check_port_num(i) == True:
        print('port number for ' +  socket_names[counter] + ': ' + str(i))
    else:
        print('error, check the port number for ' + socket_names[counter])
        sys.exit(1)
    counter += 1
try:
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock_in.bind((HOST, sport_num_in))
    sock_out.bind((HOST, sport_num_out))

    sock_out.connect((HOST, cport_num_sin))
except socket.error as message:
    sock_in.close()
    sock_out.close()
    print("Could not open socket: " + message)
    sys.exit(1)
    
if os.path.isfile(file_name) == False:
    print("error file with the name " + "'" + file_name +  "' doesn't exist")
    sys.exit(1)
else:
    print('file is ' + file_name)
    file = open(file_name, 'r')
    
next_value = 0
exitFlag = False
buffer = ""
sock_in.settimeout(1)
p_counter = 0

while True:
    buffer = file.read(512)
    n = len(buffer)
    
    if n == 0:
        d_packet = packet.Packet(0x497E, 0, next_value, 0, "")
        exitFlag = True
            
    if n > 0:
        d_packet = packet.Packet(0x497E, 0, next_value, n, buffer)
        
    packetBuffer = pickle.dumps(d_packet)
    while True:
        print("sending '" + d_packet.data + "' to " + str(cport_num_sin) + ", packet counter is " + str(p_counter)) 
        sock_out.sendto(packetBuffer, (HOST, cport_num_sin))
        p_counter += 1
        try:
            rcvd, addr = sock_in.recvfrom(512)
            rcvd = pickle.loads(rcvd)
        except socket.timeout:
            continue
        if not (rcvd.check_magicno() == True and rcvd.data_type == 1 \
                and rcvd.data_len == 0):
            continue
        else:
            if rcvd.seqno != next_value:
                continue
            else:
                next_value = 1 - next_value
                if exitFlag == True:
                    file.close()
                    sock_in.close()
                    sock_out.close()
                    
                    print('count of packet sent ' + str(p_counter))
                    sys.exit()
                else:
                    break    

    
    