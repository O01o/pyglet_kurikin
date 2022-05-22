from curses import window
from operator import imod
from pickletools import pytuple
from black import main
from cv2 import polylines
import pyglet
import random
from pyglet import resource
from pyglet.window import mouse
import math

# ウィンドウの描画
window = pyglet.window.Window(640, 480, "KurikinTest")

# キンの画像ロード
player_kins_image = pyglet.image.load("images/a0.png")
enemy_kins_image = pyglet.image.load("images/b0.png")
error_image = pyglet.image.load("images/a1.png")

# 自分または相手のキンの描画
def kins_maker(num_kins, batch=None, img=error_image, x0=0, y0=0, x1=640, y1=480, color=(255,255,255)):
    kins = []
    for i in range(num_kins):
        kin_x = random.randint(x0,x1)
        kin_y = random.randint(y0,y1)
        # kin_new = pyglet.sprite.Sprite(img=img, x=kin_x, y=kin_y, batch=batch)
        kin_new = pyglet.shapes.Circle(kin_x,kin_y,8,color=color,batch=main_batch)
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
circle_point_tmp = 0,0
circle_polygon = []
circle_polygon_edge = []
kins_state = False
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
    global circle_polygon
    global circle_polygon_edge
    global kins_p
    global radian_total
    circle_point_tmp = x,y
    circle_polygon.append(circle_point_tmp)
    print(circle_point_tmp,"pressed")
    
    # 多角形が描画されてる場合にその描画を消す
    circle_polygon = []
    circle_polygon_edge = []
    radian_total = 0.0
    # ついでにキンの色も元に戻す
    for kin in kins_p:
        kin.color = 100,100,255
    
@window.event
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):
    global circle_point_tmp
    global circle_polygon
    global circle_polygon_edge
    min_distance = 20
    distance = math.sqrt((x-circle_point_tmp[0])**2 + (y-circle_point_tmp[1])**2)
    if distance >= min_distance:
        edge = polygon_node_add(x,y,tp=circle_point_tmp,batch=circle_batch)
        circle_point_tmp = x,y
        circle_polygon.append(circle_point_tmp)
        circle_polygon_edge.append(edge)
        print(circle_point_tmp,"drag")
    
@window.event
def on_mouse_release(x,y,button, modifiers):
    global circle_point_tmp
    global circle_polygon
    global circle_polygon_edge
    global kins_p
    global radian_total
    edge = polygon_node_add(x,y,tp=circle_point_tmp,batch=circle_batch)
    circle_point_tmp = x,y
    circle_polygon.append(circle_point_tmp)
    circle_polygon_edge.append(edge)
    x0,y0 = circle_polygon[0]
    edge = polygon_node_add(x0,y0,tp=circle_point_tmp,batch=circle_batch)
    circle_polygon.append(circle_polygon[0])
    circle_polygon_edge.append(edge)
    
    print(circle_point_tmp,"released")
    print("polygon", circle_polygon)
    print("polygon_edge", circle_polygon_edge)
    
    rounded_flag = False
    for kin in kins_p:
        for edge in circle_polygon_edge:
            x0,y0,x1,y1 = edge.position
            vec0 = x0-kin.x, y0-kin.y
            vec1 = x1-kin.x, y1-kin.y
            radian = math.acos(((vec0[0]*vec1[0])+(vec0[1]*vec1[1]))/((math.sqrt((vec0[0]**2)+(vec0[1]**2)))*(math.sqrt((vec1[0]**2)+(vec1[1]**2)))))
            # print(radian) # debug
            radian_total += radian
        
        # WindingNumberAlgorithmによる多角形内外判定の結果出力
        # print(radian_total) # debug
        if radian_total >= 1.999 * math.pi:
            kin.color = 255,255,100
            rounded_flag = True
        else:
            kin.color = 100,100,255
        radian_total = 0.0
    
    if not rounded_flag:
        circle_polygon = []
        circle_polygon_edge = []
    
pyglet.app.run()
# pyglet.clock.schedule_interval(callback, 1/30)