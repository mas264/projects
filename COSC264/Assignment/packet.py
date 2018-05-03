PTYPE_DATA = 0
PTYPE_ACK = 1

class Packet:

    def __init__(self, magicno, data_type, seqno, data_len, data):
        self.magicno = magicno
        self.data_type = data_type
        self.seqno = seqno
        self.data_len = data_len
        self.data = data
        
    def check_magicno(self):
        
        return self.magicno == 0x497E
    
    
        
        
    
        
    