# -*- coding: utf-8 -*-
'''
将事件插入数据库的控制程序-控制1分钟可插入1次

用法：

'''

import time

seconds = 60
while True:
    f = open('allowinsertdatabase.txt','r')
    content = f.read()
    f.close()
    
    allow = content[11:12]
    
    if allow == '0':
        print('status: not allow')
        for i in range(seconds,0,-1):
            print('wait %d seconds...' %(i))
            time.sleep(1)
            
        f = open('allowinsertdatabase.txt','w')
        f.write('is_allowed=1')
        f.close()
        
    elif allow == '1':
        print('status: allow')
        time.sleep(1)
    else:
        pass