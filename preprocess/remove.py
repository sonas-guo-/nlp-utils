# -*- encoding:utf8 -*-
import re
from string import punctuation
'''
移除特殊符号(全角ASCII、全角中英文标点、半宽片假名、半宽平假名、半宽韩文字母)
'''
def remove_cn_symbols(content):
    assert type(content)==str
    re.sub(r'[\uff00-\uffef]','',content)
'''
移除英文符号
'''
def remove_en_symbols(content):
    assert type(content)==str
    return re.sub(r'['+punctuation+']','',content)
'''
移除中文和英文标点符号
'''
def remove_cnen_symbols(content):
    assert type(content)==str
    return remove_cn_symbols(remove_en_symbols(content))
'''
保留中文汉字(基本汉字)
'''
def remain_cn_chars(content):
    assert type(content)==str
    return re.sub(r'[^\u4e00-\u9fa5]','',content)

if __name__=='__main__':
    pass
