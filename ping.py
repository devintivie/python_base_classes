# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:49:31 2018

@author: user
"""

import platform
import subprocess

def ping_check(ip_addr):
    startupinfo = None
    
    if platform.system()=='Windows':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    
    response = subprocess.Popen(['ping.exe','-n', '1', '-w', '50', ip_addr],
                                stdout = subprocess.PIPE, startupinfo= startupinfo).communicate()  
    
    try:
        temp = str(response[0], encoding = 'utf-8').split(',')[2]
        if not '1' in temp:
            return 1
        else:
            return 0
    except:
        return 0
    