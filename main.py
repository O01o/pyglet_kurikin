from curses import window
from operator import imod
from pickletools import pytuple
from black import main
import pyglet
import random
from pyglet import resource

window = pyglet.window.Window(640, 480, "KurikinTest")

player_kins_image = pyglet.image.load("images/a0.png")

def kins_maker(num_kins, batch=None):
    kins = []
    for i in range(num_kins):
        kin_x = random.randint(0,240)
        kin_y = random.randint(240,480)
        kin_new = pyglet.sprite.Sprite(img=player_kins_image, x=kin_x, y=kin_y, batch=batch)
        kins.append(kin_new)
    return kins



main_batch = pyglet.graphics.Batch()
kins_p = kins_maker(num_kins=10, batch=main_batch)    

@window.event
def on_draw():
    window.clear()
    main_batch.draw() # kins_pのオブジェクトリストもバッチで一括描画！

def update():
    pass

pyglet.app.run()
pyglet.clock.schedule_interval(update, 1/30)