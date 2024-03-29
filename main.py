from curses import window
from operator import imod
from pickletools import pytuple
from tkinter import ROUND
from black import main
from cv2 import polylines
import pyglet
import random
from pyglet import resource
from pyglet.window import mouse
import math
from pyglet import clock
from enum import Enum, auto

# ウィンドウの描画
window = pyglet.window.Window(640, 480, "KurikinTest")

# キンの画像ロード
player_kins_image = pyglet.image.load("images/a0.png")
enemy_kins_image = pyglet.image.load("images/b0.png")
error_image = pyglet.image.load("images/a1.png")

class State(Enum):
    STOP = auto()
    MOVE = auto()
    ROUNDED = auto()  

class Kin():

    def __init__(self,point=[0,0],size=8,speed=2.0,point_purpose=[0,0],stop_time=1024,color=(255,255,255),batch=None):
        self.speed = speed
        self.point_purpose = point_purpose
        self.state = State.STOP
        self.stop_time = stop_time
        self.dt = 1/24
        self.distance_min = 6
        self.kin = pyglet.shapes.Circle(point[0],point[1],size,color=color,batch=batch)
        self.event = pyglet.clock.schedule_interval(self.callback, self.dt)
    
    def callback(self, dt):
        distance = math.sqrt((self.point_purpose[0]-self.kin.x)**2 + (self.point_purpose[1]-self.kin.y)**2)
        if self.state == State.STOP:
            self.stop_time += 1
            if distance >= self.distance_min:
                self.state = State.MOVE
        if self.state == State.MOVE:
            self.stop_time = 0
            if distance <= self.distance_min:
                self.state = State.STOP
            else:
                self.kin.x += self.speed * ((self.point_purpose[0]-self.kin.x)/distance) * dt
                self.kin.y += self.speed * ((self.point_purpose[1]-self.kin.y)/distance) * dt
        if self.state == State.ROUNDED:
            self.stop_time = 0
        

# 自分または相手のキンの描画
def kins_maker(num_kins, batch=None, img=error_image, x0=0, y0=0, x1=640, y1=480, color=(255,255,255)):
    kins = []
    for i in range(num_kins):
        kin_x = random.randint(x0,x1)
        kin_y = random.randint(y0,y1)
        # kin_new = pyglet.shapes.Circle(kin_x,kin_y,8,color=color,batch=main_batch)
        kin_new = Kin(point=(kin_x,kin_y),color=color,batch=batch)
        kin_new.point_purpose = [kin_x,kin_y]
        kins.append(kin_new)
    return kins

# タッチペンで描く円(曲線)を描画するためのプログラム
def polygon_node_add(x,y,tp=(0,0),batch=None):
    edge = pyglet.shapes.Line(x,y,tp[0],tp[1],width=5,batch=batch)
    return edge

# バッチの用意, 自分のキンと相手のキンを描画
main_batch = pyglet.graphics.Batch()
circle_batch = pyglet.graphics.Batch()
kins_p = kins_maker(num_kins=10, batch=main_batch, img=player_kins_image, x0=0, y0=240, x1=240, y1=480, color=(100,100,255)) # 自分のキンの描画
kins_e = kins_maker(num_kins=10, batch=main_batch, img=enemy_kins_image, x0=400, y0=0, x1=640, y1=240, color=(255,100,100)) # 自分のキンの描画
kins_leader_line = pyglet.shapes.Line(0,0,0,0,width=5,batch=main_batch)
circle_point_tmp = [0,0]
circle_point_center = [0,0]
circle_point_purpose = [0,0]
circle_polygon = []
circle_polygon_edge = []
rounded_mode = False
radian_total = 0.0
# polyline = polyline_maker(edges, batch=main_batch) # 多角形描画

@window.event
def on_draw():
    window.clear()
    main_batch.draw() # kins_pのオブジェクトリストもバッチで一括描画！
    circle_batch.draw()

@window.event
def on_mouse_press(x,y,button,modifiers):
    global circle_point_tmp
    global circle_point_center
    global circle_point_purpose
    global circle_polygon
    global circle_polygon_edge
    global kins_p
    global kins_leader_line
    global radian_total
    global rounded_mode
    
    circle_point_tmp = x,y
    circle_polygon.append(circle_point_tmp)
    # print(circle_point_tmp,"pressed") # debug
    
    if not rounded_mode:
        # 多角形が描画されてる場合にその描画を消す
        circle_polygon = []
        circle_polygon_edge = []
        radian_total = 0.0
        # ついでにキンの色も元に戻す
        for kin in kins_p:
            kin.kin.color = 100,100,255
    
    # if rounded mode
    else:
        # WindingNumberAlgorithm
        for edge in circle_polygon_edge:
            x0,y0,x1,y1 = edge.position
            vec0 = x0-x, y0-y
            vec1 = x1-x, y1-y
            radian = math.acos(((vec0[0]*vec1[0])+(vec0[1]*vec1[1]))/((math.sqrt((vec0[0]**2)+(vec0[1]**2)))*(math.sqrt((vec1[0]**2)+(vec1[1]**2)))))
            # print(radian) # debug
            radian_total += radian
            
        # WindingNumberAlgorithmによる多角形内外判定の結果出力
        # print(radian_total) # debug
        if radian_total >= 1.999 * math.pi:
            # 多角形の内側なら円の中心点と目的点を定める
            # 円の中心点は、多角形の座標の平均を取る
            cx,cy = 0,0
            for point in circle_polygon:
                cx += point[0]
                cy += point[1]
            cx /= len(circle_polygon)
            cy /= len(circle_polygon)
            circle_point_center = [cx,cy]
            # 円の目的点は、現在のマウスポインタとし、直線を引く
            kins_leader_line.x = cx
            kins_leader_line.y = cy
            kins_leader_line.x2 = x
            kins_leader_line.y2 = y
        else:
            # 多角形の外側なら円を外す
            circle_polygon = []
            circle_polygon_edge = []
            # ついでにキンの色も戻す
            for kin in kins_p:
                kin.kin.color = 100,100,255
        radian_total = 0.0
    
@window.event
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
    global circle_point_tmp
    global circle_point_center
    global circle_point_purpose
    global circle_polygon
    global circle_polygon_edge
    global kins_leader_line
    global rounded_mode
    
    distance_min = 10
    
    if not rounded_mode:
        distance_circle = math.sqrt((x-circle_point_tmp[0])**2 + (y-circle_point_tmp[1])**2)
        if distance_circle >= distance_min:
            edge = polygon_node_add(x,y,tp=circle_point_tmp,batch=circle_batch)
            circle_point_tmp = x,y
            circle_polygon.append(circle_point_tmp)
            circle_polygon_edge.append(edge)
            # print(circle_point_tmp,"drag") # debug
    
    # if rounded mode
    else:
        distance_line = math.sqrt((x-circle_point_center[0])**2 + (y-circle_point_center[1])**2)
        if distance_line >= distance_min:
            kins_leader_line.x2 = x
            kins_leader_line.y2 = y
    
@window.event
def on_mouse_release(x,y,button, modifiers):
    global circle_point_tmp
    global circle_point_center
    global circle_point_purpose
    global circle_polygon
    global circle_polygon_edge
    global kins_p
    global kins_leader_line
    global radian_total
    global rounded_mode
    
    if not rounded_mode:
        edge = polygon_node_add(x,y,tp=circle_point_tmp,batch=circle_batch)
        circle_point_tmp = x,y
        circle_polygon.append(circle_point_tmp)
        circle_polygon_edge.append(edge)
        x0,y0 = circle_polygon[0]
        edge = polygon_node_add(x0,y0,tp=circle_point_tmp,batch=circle_batch)
        circle_polygon.append(circle_polygon[0])
        circle_polygon_edge.append(edge)
        
        # print(circle_point_tmp,"released") # debug
        # print("polygon", circle_polygon) # debug
        # print("polygon_edge", circle_polygon_edge) # debug
        
        rounded_flag = False
        for kin in kins_p:
            # WindingNumberAlgorithm
            for edge in circle_polygon_edge:
                x0,y0,x1,y1 = edge.position
                vec0 = x0-kin.kin.x, y0-kin.kin.y
                vec1 = x1-kin.kin.x, y1-kin.kin.y
                radian = math.acos(((vec0[0]*vec1[0])+(vec0[1]*vec1[1]))/((math.sqrt((vec0[0]**2)+(vec0[1]**2)))*(math.sqrt((vec1[0]**2)+(vec1[1]**2)))))
                
                # print(radian) # debug
                radian_total += radian
            
            # WindingNumberAlgorithmによる多角形内外判定の結果出力
            # print(radian_total) # debug
            if radian_total >= 1.999 * math.pi:
                kin.kin.color = 255,255,100
                rounded_flag = True
                kin.state = State.ROUNDED
            else:
                kin.kin.color = 100,100,255
                kin.state = State.MOVE
            radian_total = 0.0
        
        if rounded_flag:
            rounded_mode = True
        else:
            rounded_mode = False
            circle_polygon = []
            circle_polygon_edge = []
    
    # if rounded mode (mouse release)
    else:
        kins_leader_line.x = 0
        kins_leader_line.y = 0
        kins_leader_line.x2 = 0
        kins_leader_line.y2 = 0
        rounded_mode = False
        circle_polygon = []
        circle_polygon_edge = []
        for kin in kins_p:
            if kin.state == State.ROUNDED:
                cpcx,cpcy = circle_point_center
                # TypeError: 'tuple' object does not support item assignment
                kin.point_purpose[0] += x-cpcx
                kin.point_purpose[1] += y-cpcy
                # debug (キンを動かす(無事成功))
                # kin.kin.x = x
                # kin.kin.y = y
                
            kin.kin.color = 100,100,255
    

def update(dt):
    # debug(動かない)
    # print('p')
    pass
    
pyglet.app.run()
# pyglet.clock.schedule_interval(update, 1/30)