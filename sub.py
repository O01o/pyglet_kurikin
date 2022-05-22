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
window = pyglet.window.Window(640, 480, "WindingNumberAlgorithm")
main_batch = pyglet.graphics.Batch()

# タッチペンで描く円(曲線)を描画するためのプログラム
def polygon_edge_add(np=(1,1),tp=(0,0),batch=None):
    edge = pyglet.shapes.Line(np[0],np[1],tp[0],tp[1],width=3,batch=batch)
    return edge

# inner mode
# p_node = pyglet.shapes.Circle(200,300,8,batch=main_batch)
# outer mode
# p_node = pyglet.shapes.Circle(100,400,8,batch=main_batch)
# random group mode
p_nodes = []
count = 1000
for i in range(count):
    x = random.randint(0,640)
    y = random.randint(0,480)
    p_nodes.append(pyglet.shapes.Circle(x,y,8,batch=main_batch))

# pentagon mode
# polygon = [(200,100),(400,100),(500,250),(300,400),(100,250),(200,100)]
# star mode
polygon = [(200,100),(500,250),(100,250),(400,100),(300,400),(200,100)]

polygon_edge = []
tmp_point = 0,0

# ポリゴンエッジの生成
for point in polygon:
    if not tmp_point == (0,0):
        polygon_edge.append(polygon_edge_add(point,tmp_point,batch=main_batch))
    tmp_point = point

radian_total = 0.0

# WindingNumberAlgorithm
for p_node in p_nodes:        
    for edge in polygon_edge:
        edge.opacity = 150
        # p_nodeとpoint、p_nodeとtmp_pointの
        # 残差ベクトルをそれぞれ作って、
        # 2直線のなす角を求め、合計角に追加する
        x0,y0,x1,y1 = edge.position
        vec0 = x0-p_node.x, y0-p_node.y
        vec1 = x1-p_node.x, y1-p_node.y
        radian = math.acos(((vec0[0]*vec1[0])+(vec0[1]*vec1[1]))/((math.sqrt((vec0[0]**2)+(vec0[1]**2)))*(math.sqrt((vec1[0]**2)+(vec1[1]**2)))))
        # print(radian) # debug
        radian_total += radian
        
    # WindingNumberAlgorithmによる多角形内外判定の結果出力
    # print(radian_total) # debug
    if radian_total >= 1.999 * math.pi:
        p_node.color = 100,100,255
    else:
        p_node.color = 255,100,100
    radian_total = 0


@window.event
def on_draw():
    window.clear()
    main_batch.draw()

pyglet.app.run()