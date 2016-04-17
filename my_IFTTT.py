# -*- coding: utf-8 -*-
"""
Sent IFTTT notification
Created on Fri Apr 15 17:07:21 2016

@author: Jo-dan
"""
import requests

def IFTTT(event_name, first, second, third):
    report = {}
    report["value1"] = first
    report["value2"] = second
    report["value3"] = third
    requests.post("https://maker.ifttt.com/trigger/{}/with/key/d0reP2BKasF7WXr86DXIxq".format(event_name), data=report)