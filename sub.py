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

polygon = [(200,100),(400,100),(500,250),(300,400),(100,250),(200,100)]
polygon_edge = []
tmp_point = 0,0
for point in polygon:
    if not tmp_point == (0,0):
        polygon_edge.append(polygon_edge_add(point,tmp_point,batch=main_batch))

@window.event
def on_draw():
    window.clear()
    main_batch.draw()

pyglet.app.run()