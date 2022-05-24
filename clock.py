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

from pyglet import clock


class Kin:
    kin = pyglet.shapes.Circle(self.point[0],self.point[1],self.size,color=self.color,batch=self.batch)


pyglet.app.run()