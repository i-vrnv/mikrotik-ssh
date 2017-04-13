#!/usr/bin/python
# get from https://wiki.mikrotik.com/wiki/Manual:API

import sys, posix, time, md5, binascii, socket, select


class ApiRos:
    "Routeros api"
    def __init__(self, sk):
        self.sk = sk
        self.current_tag = 0
        
    def login(self, username, pwd):
        chal = None

        for repl, attrs in self.talk(["/login"]):
            chal = binascii.unhexlify(attrs['=ret'])
        md = md5.new()
        md.update('\x00')
        md.update(pwd)
        md.update(chal)
        self.talk(["/login", "=name=" + username,
                   "=response=00" + binascii.hexlify(md.digest())])

    def talk(self, words):
        if self.write_sentence(words) == 0:
            return
        r = []
        while 1:
            i = self.read_sentence()
            if len(i) == 0:
                continue
            reply = i[0]
            attrs = {}
            for w in i[1:]:
                j = w.find('=', 1)
                if j == -1:
                    attrs[w] = ''
                else:
                    attrs[w[:j]] = w[j+1:]
            r.append((reply, attrs))
            if reply == '!done':
                return r

    def write_sentence(self, words):
        ret = 0
        for w in words:
            self.write_word(w)
            ret += 1
        self.write_word('')
        return ret

    def read_sentence(self):
        r = []
        while 1:
            w = self.read_word()
            if w == '':
                return r
            r.append(w)
            
    def write_word(self, w):
        print "<<< " + w
        self.write_len(len(w))
        self.write_str(w)

    def read_word(self):
        ret = self.read_str(self.read_len())
        print ">>> " + ret
        return ret

    def write_len(self, l):
        if l < 0x80:
            self.write_str(chr(l))
        elif l < 0x4000:
            l |= 0x8000
            self.write_str(chr((l >> 8) & 0xFF))
            self.write_str(chr(l & 0xFF))
        elif l < 0x200000:
            l |= 0xC00000
            self.write_str(chr((l >> 16) & 0xFF))
            self.write_str(chr((l >> 8) & 0xFF))
            self.write_str(chr(l & 0xFF))
        elif l < 0x10000000:        
            l |= 0xE0000000         
            self.write_str(chr((l >> 24) & 0xFF))
            self.write_str(chr((l >> 16) & 0xFF))
            self.write_str(chr((l >> 8) & 0xFF))
            self.write_str(chr(l & 0xFF))
        else:                       
            self.write_str(chr(0xF0))
            self.write_str(chr((l >> 24) & 0xFF))
            self.write_str(chr((l >> 16) & 0xFF))
            self.write_str(chr((l >> 8) & 0xFF))
            self.write_str(chr(l & 0xFF))

    def read_len(self):
        c = ord(self.read_str(1))
        if (c & 0x80) == 0x00:      
            pass                    
        elif (c & 0xC0) == 0x80:    
            c &= ~0xC0              
            c <<= 8                 
            c += ord(self.read_str(1))
        elif (c & 0xE0) == 0xC0:    
            c &= ~0xE0              
            c <<= 8                 
            c += ord(self.read_str(1))
            c <<= 8                 
            c += ord(self.read_str(1))
        elif (c & 0xF0) == 0xE0:    
            c &= ~0xF0              
            c <<= 8                 
            c += ord(self.read_str(1))
            c <<= 8                 
            c += ord(self.read_str(1))
            c <<= 8                 
            c += ord(self.read_str(1))
        elif (c & 0xF8) == 0xF0:    
            c = ord(self.read_str(1))
            c <<= 8                 
            c += ord(self.read_str(1))
            c <<= 8                 
            c += ord(self.read_str(1))
            c <<= 8                 
            c += ord(self.read_str(1))
        return c                    

    def write_str(self, str):
        n = 0
        while n < len(str):         
            r = self.sk.send(str[n:])
            if r == 0:
                raise RuntimeError("connection closed by remote end")
            n += r                  

    def read_str(self, length):
        ret = ''                    
        while len(ret) < length:    
            s = self.sk.recv(length - len(ret))
            if s == '':
                raise RuntimeError("connection closed by remote end")
            ret += s
        return ret


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], 8728))  
    apiros = ApiRos(s)
    apiros.login(sys.argv[2], sys.argv[3])

    input_sentence = []

    while 1:
        r = select.select([s, sys.stdin], [], [], None)
        if s in r[0]:
            # something to read in socket, read sentence
            x = apiros.read_sentence()

        if sys.stdin in r[0]:
            # read line from input and strip off newline
            l = sys.stdin.readline()
            l = l[:-1]

            # if empty line, send sentence and start with new
            # otherwise append to input sentence
            if l == '':
                apiros.write_sentence(input_sentence)
                input_sentence = []
            else:
                input_sentence.append(l)


if __name__ == '__main__':
    main()
