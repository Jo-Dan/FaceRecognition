# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 17:34:59 2016
Draw Person of Interest Squares
@author: Jo-dan
"""

import cv2
import numpy as np



def drawline(img,pt1,pt2,color,thickness=1,style='dotted',gap=20):
    dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
    pts= []
    for i in  np.arange(0,dist,gap):
        r=i/dist
        x=int((pt1[0]*(1-r)+pt2[0]*r)+.5)
        y=int((pt1[1]*(1-r)+pt2[1]*r)+.5)
        p = (x,y)
        pts.append(p)

    if style=='dotted':
        for p in pts:
            cv2.circle(img,p,thickness,color,-1)
    elif style == 'dashed vertical':
        for p in pts:
            cv2.line(img, (p[0], p[1]-3), (p[0], p[1]+3), color, thickness)
    elif style == 'dashed horizontal':
        for p in pts:
            cv2.line(img, (p[0]-3, p[1]), (p[0]+3, p[1]), color, thickness)
    else:
        s=pts[0]
        e=pts[0]
        i=0
        for p in pts:
            s=e
            e=p
            if i%2==1:
                cv2.line(img,s,e,color,thickness)
            i+=1

def drawpoly(img,pts,color,thickness=1,style='dotted',):
    s=pts[0]
    e=pts[0]
    pts.append(pts.pop(0))
    for p in pts:
        s=e
        e=p
        drawline(img,s,e,color,thickness,style)

def drawrect(img,pt1,pt2,color,thickness=1,style='dotted'):
    pts = [pt1,(pt2[0],pt1[1]),pt2,(pt1[0],pt2[1])] 
    drawpoly(img,pts,color,thickness,style)



def poi_box(win, x,y,w,h, sub_type):
    if sub_type == 'ADMIN':
        box_col = (58, 238, 247)
        accent_col = (58, 238, 247)
    elif sub_type == 'ANALOG':
        box_col = (000, 000, 000)
        accent_col = (58, 238, 247)
    elif sub_type == 'USER':
        box_col = (243, 124, 13)
        accent_col = (243, 124, 13)
    elif sub_type == 'THREAT':
        box_col = (000, 000, 255)
        accent_col = (000, 000, 255)
    elif sub_type == 'UNKNOWN':
        box_col = (255, 255, 255)
        accent_col = (255, 255, 255)
    
    

#    if w >= 300:
#        corner_len = 0.05
#        corner_thick = 8
#        point_len = .04
#        point_thick = 2
#        rect_thick = 1
#        gap = 30
#    elif w >= 100:
#        corner_len = 0.05
#        corner_thick = 3
#        point_len = .04
#        point_thick = 1
#        rect_thick = 1
#        gap = 20
#    else:
#        corner_len = 0.05
#        corner_thick = 1
#        point_len = .04
#        point_thick = 1
#        rect_thick = 1
#        gap = 10
    corner_len = 0.1
    corner_thick = int(round(w/38))
    point_len = .06
    #point_thick = int(round(w/140))
    point_thick = 2
    rect_thick = 2
    gap = int(round(w/10))
    
    #cv2.rectangle(win, (x, y), (x+w, y+h), col, 1)
    #drawrect(win, (x, y), (x+w, y+h), col, 1)
    drawline(win, (x,y), (x+w,y), box_col, rect_thick, 'dashed horizontal', gap)
    drawline(win, (x,y+h), (x+w,y+h), box_col, rect_thick, 'dashed horizontal', gap)
    drawline(win, (x,y), (x,y+h), box_col, rect_thick, 'dashed vertical', gap)
    drawline(win, (x+w,y), (x+w,y+h), box_col, rect_thick, 'dashed vertical', gap)
    #top left
    cv2.line(win, (x, y), (x+int(round(corner_len*w)), y), accent_col, corner_thick)
    cv2.line(win, (x, y), (x, y+int(round(corner_len*h))), accent_col, corner_thick)
    #top right
    cv2.line(win, (x+w, y), (x+w-int(round(corner_len*w)), y), accent_col, corner_thick)
    cv2.line(win, (x+w, y), (x+w, y+int(round(corner_len*h))), accent_col, corner_thick)
    #bottom left
    cv2.line(win, (x, y+h), (x+int(round(corner_len*w)),y+h), accent_col, corner_thick)
    cv2.line(win, (x, y+h), (x, y+h-int(round(corner_len*h))), accent_col, corner_thick)
    #bottom right
    cv2.line(win, (x+w, y+h), (x+w-int(round(corner_len*w)),y+h), accent_col, corner_thick)
    cv2.line(win, (x+w, y+h), (x+w, y+h-int(round(corner_len*h))), accent_col, corner_thick)
    #target points
    cv2.line(win, (x+int(round(.5*w)), y), (x+int(round(.5*w)), y+int(round(point_len*h))), accent_col, point_thick)
    cv2.line(win, (x+int(round(.5*w)), y+h), (x+int(round(.5*w)), y+h-int(round(point_len*h))), accent_col, point_thick)
    cv2.line(win, (x, y+int(round(.5*h))), (x+int(round(point_len*w)), y+int(round(.5*h))), accent_col, point_thick)
    cv2.line(win, (x+w, y+int(round(.5*h))), (x+w-int(round(point_len*w)), y+int(round(.5*h))), accent_col, point_thick)
    
def sam_circle(win, x, y, w, h, sub_type):
    circle_col = (214,214,214)
    outercircle_col = (10,10,10)
    accentcircle_col = (200,200,200)
    triangle_colour = (000,000,255)
    if w > h:
        r = w
    else:
        r = h
    tran1 = win.copy()
    tran2 = win.copy()
    trant = win.copy()
    cv2.circle(tran1, (x+int(round(.5*w)), y+int(round(.5*h))), int(round(0.9*r)), circle_col, 40)
    cv2.circle(tran1, (x+int(round(.5*w)), y+int(round(.5*h))), int(round(1*r))+20, outercircle_col, 30)
    cv2.circle(tran2, (x+int(round(.5*w)), y+int(round(.5*h))), int(round(1*r))+20, accentcircle_col, 2)
    trant = cv2.addWeighted(tran1, .3, tran2, .7, 0, trant)
    win = cv2.addWeighted(trant, .7, win, .3, 0, win)
    
#    cv2.line(win, (x-int(round(.5*w)), y-int(round(.5*h))), (x+w+int(round(.5*w)), y-int(round(.5*h))), triangle_colour, 3)
#    cv2.line(win, (x-int(round(.5*w)), y-int(round(.5*h))), (x+int(round(.5*w)), y+h+int(round(.5*h))), triangle_colour, 3)
#    cv2.line(win, (x+w+int(round(.5*w)), y-int(round(.5*h))), (x+int(round(.5*w)), y+h+int(round(.5*h))), triangle_colour, 3)
    
    cv2.line(win, (x-int(round(.25*r)), y), (x+w+int(round(.25*r)), y), triangle_colour, 3)
    cv2.line(win, (x-int(round(.25*r)), y), (x+int(round(.5*r)), y+h+int(round(.4*r))), triangle_colour, 3)
    cv2.line(win, (x+w+int(round(.25*r)), y), (x+int(round(.5*r)), y+h+int(round(.4*r))), triangle_colour, 3)
    
    
def poi_image(win, x, y, w, h, sub_type):
    assets_path = "D:\\BackUp\\F\\Users\\Jordan\\Documents\\Python\\Face Rec\\gui\\machine\\"
    box_path = assets_path + sub_type.lower() + '_focus.jpg'
    box = cv2.imread(box_path, -1)
    print box_path
    foreground_mask = box[:,:,3]
    background_mask = cv2.bitwise_not(foreground_mask)
    foreground_image = box[:, :, 0:3]
    
    re_image = cv2.resize(image, (x+w, y+h), interpolation = cv2.INTER_AREA)
    win = cv2.addWeighted(re_image, .7, win, .3, 0, win)    
        
        