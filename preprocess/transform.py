# -*- encoding:utf8 -*-
'''
全角转半角
'''
def SBC2DBC(content):
    assert type(content)==str
    res=''
    for c in content:
        unicode=ord(c)
        if unicode==0x3000:
            res+=chr(0x20)
        elif unicode>=0xff01 and unicode<=0xff5e:
            res+=chr(unicode-0xfee0)
        else:
            res+=c
    return res
'''
半角转全角
'''
def DBC2SBC(content):
    assert type(content)==str
    res=''
    for c in content:
        unicode=ord(c)
        if unicode==0x20:
            res+=chr(0x3000)
        elif unicode>=0x21 and unicode<=0x7e:
            res+=chr(unicode+0xfee0)
        else:
            res+=c
    return res

if __name__=='__main__':
    pass
