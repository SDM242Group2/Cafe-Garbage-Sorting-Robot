# -*- coding:utf-8 -*-
import time
import socket
import numpy as np
 
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.31.17.190', 6666))  #绑定ip和端口号（IP为发送数据的树莓派ip，端口号自己指定）
s.listen(5)
c, address = s.accept()      #等待别的树莓派接入
 
start_time = time.time()
 
while(True):
 
    if(time.time() - start_time < 5):
        msg = '1'
    else:
        msg = '2'
 
    print(msg)
 
    c.send(msg.encode('utf-8'))   #编码
 
    if(msg == '2'):
        break
 
s.close()