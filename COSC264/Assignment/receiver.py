import socket
import sys
import numbers
import os
import packet
import pickle

rport_num_in = int(sys.argv[1])
rport_num_out = int(sys.argv[2])
cport_num_rin = int(sys.argv[3])
file_name = sys.argv[4]

HOST = '127.0.0.1'

def check_port_num(port_num):
    "Returns boolean value to check whether the port number is valid."
    
    return  (1024 < port_num < 64000) \
            and (isinstance(port_num, numbers.Integral))
    
    
port_nums = [rport_num_in, rport_num_out, cport_num_rin]
socket_names = ['r_in', 'r_out', 'cr_in']
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
    
    sock_in.bind((HOST, rport_num_in))
    sock_out.bind((HOST, rport_num_out))
    
    sock_out.connect((HOST, cport_num_rin))
except socket.error as message:
    sock_in.close()
    sock_out.close()
    print("Could not open socket: " + message)
    sys.exit(1)
    
if os.path.isfile(file_name) == False:
    file = open(file_name, 'w+')
else:
    print("error file with the name " + "'" + file_name +  "' already exist")
    sys.exit(1)
    
expected = 0

while True:
    
    rcv, addr = sock_in.recvfrom(1024)
    rcvd = pickle.loads(rcv)
    
    if rcvd.check_magicno() == True and rcvd.data_type == 0:
        if rcvd.seqno != expected:
            a_packet = packet.Packet(0x497E, 1, rcvd.seqno, 0, "")
            sock_out.sendto(pickle.dumps(a_packet), (HOST, cport_num_rin))
            continue
        if rcvd.seqno == expected:
            a_packet = packet.Packet(0x497E, 1, rcvd.seqno, 0, "")
            sock_out.sendto(pickle.dumps(a_packet), (HOST, cport_num_rin))
            expected = 1 - expected
            if rcvd.data_len > 0:
                print('writing ' + rcvd.data + 'to ' + file_name)
                file.write(rcvd.data)
                continue
            if rcvd.data_len == 0:
                print('received all packets needed and data is written to file')
                file.close()
                sock_in.close()
                sock_out.close()
                sys.exit()
                
    else:
        continue
    
    

                