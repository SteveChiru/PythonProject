import pycurl
from io import StringIO
import random

class Tools :
    def __init__(self):
        pass

    def getPage(self,url,requestHeader = []):
        fakeIp = self.fakeIp()
        requestHeader.append('CLIENT-IP:' + fakeIp)
        requestHeader.append('X-FORWARDED-FOR:' + fakeIp)
        try:
            curl = pycurl.Curl()
        except Exception as e:
            header = ''
            body = ''
        return header,body

    def fakeIp(self):
        fakeIpList = []
        for x in range(0,4):
            fakeIpList.append(str(int(random.uniform(0,255))))
        fakeIp = '.'.join(fakeIpList)
        return fakeIp

    def xor(self,x,y,base=32):
        stat = True
        if x >= 0 :
            x = str(bin(int(str(x), 10)))[2:]
            for i in range(0, base - len(x)):
                x = '0' + x
        else :
            x = str(bin(int(str(x + 1), 10)))[3:]
            for i in range(0, base - len(x)):
                x = '0' + x
            t = ''
            for i in range(0,len(x)):
                if x[i] == '1' :
                    t = t + '0'
                else :
                    t = t + '1'
            x = t
        if y >= 0 :
            y = str(bin(int(str(y), 10)))[2:]
            for i in range(0, base - len(y)):
                y = '0' + y
        else :
            y = str(bin(int(str(y + 1), 10)))[3:]
            for i in range(0, base - len(y)):
                y = '0' + y
            t = ''
            for i in range(0,len(y)):
                if y[i] == '1' :
                    t = t + '0'
                else :
                    t = t + '1'
            y = t
        t = ''
        for i in range(0, base):
            if x[i] == y[i] :
                t = t + '0'
            else :
                t = t + '1'
        x = t
        if x[0] == '1' :
            stat = False
            t = ''
            for i in range(0,len(x)):
                if x[i] == '1' :
                    t = t + '0'
                else :
                    t = t + '1'
            x = t
        r = int(str(x), 2)
        if stat == False :
            r = 0 - r - 1

        return r

    def rotate(self,x,y,w,base=32):
        stat = True
        if x >= 0 :
            x = str(bin(int(str(x), 10)))[2:]
            for i in range(0, base - len(x)):
                x = '0' + x
        else :
            x = str(bin(int(str(x + 1), 10)))[3:]
            for i in range(0, base - len(x)):
                x = '0' + x
            t = ''
            for i in range(0,len(x)):
                if x[i] == '1' :
                    t = t + '0'
                else :
                    t = t + '1'
            x = t
        if y >= base :
            y = y % base
        for i in range (0, y) :
            if w != 'r+' :
                x = x[0] + x + '0'
            else :
                x = '0' + x + '0'
        if w == 'r' or w == 'r+' :
            x = x[0 : base]
        else :
            x = x[(len(x) - base) : ]
        if x[0] == '1' :
            stat = False
            t = ''
            for i in range(0,len(x)):
                if x[i] == '1' :
                    t = t + '0'
                else :
                    t = t + '1'
            x = t
        r = int(str(x), 2)
        if stat == False :
            r = 0 - r - 1

        return r