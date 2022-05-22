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
    edge = pyglet.shapes.Line(np[0],np[1],tp[0],tp[1],width=5,batch=batch)
    return edge

# p_node = 200,300
polygon = [(200,100),(400,100),(500,250),(300,400),(100,250),(200,100)]
polygon_edge = []
radian_total = 0.0
tmp_point = 0,0

# ポリゴンエッジの生成
for point in polygon:
    if not tmp_point == (0,0):
        # p_nodeとpoint、p_nodeとtmp_pointの
        # 残差ベクトルをそれぞれ作って、
        # 2直線のなす角を求め、合計角に追加する
        radian_total += 0
        polygon_edge.append(polygon_edge_add(point,tmp_point,batch=main_batch))
    tmp_point = point

# ポリゴンエッジの可視化
for edge in polygon_edge:
    edge.opacity = 255

# WindingNumberAlgorithmによる多角形内外判定の結果出力    
if radian_total >= 0.95:
    print("in the polygon is True")
else:
    print("in the polygon is False")

@window.event
def on_draw():
    window.clear()
    main_batch.draw()

pyglet.app.run()