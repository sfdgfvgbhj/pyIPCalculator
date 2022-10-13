# !/usr/bin/python3
# IPV4Calculator

def bin_todec(bit):
    x = list(bit)
    x.reverse()
    result = 0
    for i in range(len(bit)):
      if x[i] == '1':
        result += 2 ** i
    return result

def dec_tobin(num):
    result = ''
    while num > 0:
        x = num%2
        result += str(x)
        num //= 2
    a = list(result)
    a.reverse()
    result = ''.join(a)
    return result.zfill(8)

def get_bitmask(cidr):
    bit = ''
    for i in range(32):
      x = '1'
      if i >= int(cidr):
        x = '0'
      bit += x
    result = [''] * 4
    x = 0
    for i in bit:
        result[x] += i
        if len(result[x]) == 8:
           x += 1
    return result

class IPAddress:

    def __init__(self, ip):
        self.ip, self.cidr = ip.split('/')
        self.ip = self.ip.split('.')
        self.bitmask = get_bitmask(self.cidr)
        self.netmask = [bin_todec(x) for x in self.bitmask]
        self.rawip = [dec_tobin(int(x)) for x in self.ip]
        self.host = (2**(32 - int(self.cidr))) - 2
        self.netid = [self.netmask[i] and int(self.ip[i])  for i in range(len(self.netmask))]
        self.rawnetid = [dec_tobin(self.netid[i]) for i in range(len(self.netid))]

    def ip_clases(self):
        octet = int(self.ip[0])
        classes = ''
        if octet >= 1 and octet <= 127:
           classes = 'A'
        elif octet >= 128 and octet <= 191:
           classes = 'B'
        elif octet >= 192 and octet <= 223:
           classes = 'C'
        else:
           print('Error : class not found')
        return classes


    def get_subnet(self):
        subnet = 0
        if self.ip_clases() == 'A':
           for a in self.bitmask[1:]:
             for bit in a:
               if bit == '1':
                 subnet += 1
        elif self.ip_clases() == 'B':
           for b in self.bitmask[2:]:
             for bit in b:
               if bit == '1':
                 subnet += 1

        return 2**subnet

ip = IPAddress('10.10.0.1/24')
print(ip.bitmask)
print(ip.netmask)
print(ip.rawip)
print(ip.get_subnet())
print(ip.netid, '\t',  ip.rawnetid)
print(ip.host)
