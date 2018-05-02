import socket
import sys
import select
import packet
import random
import numbers
import pickle

cport_num_sin = int(sys.argv[1])
cport_num_sout = int(sys.argv[2])
cport_num_rin = int(sys.argv[3])
cport_num_rout = int(sys.argv[4])
sport_num_in = int(sys.argv[5])
rport_num_in = int(sys.argv[6])
ploss_rate = float(sys.argv[7])

HOST = '127.0.0.1'

def check_port_num(port_num):
    "Returns boolean value to check whether the port number is valid."
    
    return (1024 < port_num < 64000) and \
           (isinstance(port_num, numbers.Integral))

def check_ploss_rate(ploss_rate):
    "Returns boolean value to check whether the packet loss rate is valid."
    
    return (0.0 <= ploss_rate < 1) \
           and (isinstance(ploss_rate, numbers.Real))

port_nums = [cport_num_sin, cport_num_sout, cport_num_rin, cport_num_rout, sport_num_in, rport_num_in]
socket_names = ['cs_in', 'cs_out', 'cr_in', 'cr_out', 's_in', 'r_in']
if len(set(port_nums)) != len(port_nums):
    print('port numbers are not unique, try again')
    sys.exit()


counter = 0
for i in port_nums:
    if check_port_num(i) == True:
        print('port number for ' + socket_names[counter]+ ': ' + str(i))
    else:
        print('error, check the port number for ' + socket_names[counter])
        sys.exit(1)
    counter += 1

if check_ploss_rate(ploss_rate) == True:
    print('packet loss rate is: ' + str(ploss_rate))
else:
    print('error packet loss rate is invalid')

try:
    #create and bind the channel sockets
    sock_sin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_sout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_rin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_rout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock_sin.bind((HOST, cport_num_sin))
    sock_sout.bind((HOST, cport_num_sout))
    sock_rin.bind((HOST, cport_num_rin))
    sock_rout.bind((HOST, cport_num_rout))
    
    #connects the channel s_out and r_out to sender and receivers s_in, r_in
    sock_sout.connect((HOST, sport_num_in))
    sock_rout.connect((HOST, rport_num_in))
    
except socket.error as message:
    sock_sin.close()
    sock_sout.close()
    sock_rin.close()
    sock_rout.close()
    print("Could not open socket: " + message)
    sys.exit(1)

inputs = [sock_sin, sock_rin]
outputs = []


while True:
    
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    
    for s in readable:
        
        if s is sock_sin or s is sock_rin:
            
            d, addr = s.recvfrom(1024)
            data = pickle.loads(d)
            
            if data.check_magicno() == True:
                #random.seed(10) #seed value
                u = random.random()
                print('random variate is ' + str(u))
                if u >= ploss_rate:
                    
                    if s is sock_sin:
                        print("sending '" + data.data + "' to " + str(rport_num_in))
                        sock_rout.sendto(pickle.dumps(data), (HOST, rport_num_in))
                    if s is sock_rin:
                        print("sending '" + data.data + "' to " + str(sport_num_in))
                        sock_sout.sendto(pickle.dumps(data), (HOST, sport_num_in))                    
                    
                
                
                