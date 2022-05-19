from curses import window
from operator import imod
from pickletools import pytuple
from black import main
from cv2 import polylines
import pyglet
import random
from pyglet import resource

window = pyglet.window.Window(640, 480, "KurikinTest")

player_kins_image = pyglet.image.load("images/a0.png")
enemy_kins_image = pyglet.image.load("images/b0.png")
error_image = pyglet.image.load("images/a1.png")

def kins_maker(num_kins, batch=None, img=error_image, x0=0, y0=0, x1=640, y1=480):
    kins = []
    for i in range(num_kins):
        kin_x = random.randint(x0,x1)
        kin_y = random.randint(y0,y1)
        kin_new = pyglet.sprite.Sprite(img=img, x=kin_x, y=kin_y, batch=batch)
        kins.append(kin_new)
    return kins

# タッチペンで描く円(曲線)を描画するためのプログラム
'''
nodes = [[0,0],[50,50],[20,80]]
edges = []
for node_num in range(nodes)-1:
    edge = [nodes[node_num][0],nodes[node_num][1], nodes[node_num+1][0]-nodes[node_num+1][1]]
    edges.append = edge
    
def polyline_maker(edges, batch=None):
    polyline = []
    for edge in edges:
        element = pyglet.shapes.Line(edge[0],edge[1],edge[2],edge[3],width=3,batch=batch)
        polyline.append(element)
    return polyline
'''

main_batch = pyglet.graphics.Batch()
kins_p = kins_maker(num_kins=10, batch=main_batch, img=player_kins_image, x0=0, y0=240, x1=240, y1=480) # 自分のキンの描画
kins_e = kins_maker(num_kins=10, batch=main_batch, img=enemy_kins_image, x0=480, y0=0, x1=640, y1=240) # 自分のキンの描画
# polyline = polyline_maker(edges, batch=main_batch) # 多角形描画

@window.event
def on_draw():
    window.clear()
    main_batch.draw() # kins_pのオブジェクトリストもバッチで一括描画！

def update():
    pass

pyglet.app.run()
pyglet.clock.schedule_interval(update, 1/30)