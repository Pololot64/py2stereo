#Py2Stereo Copyright Paul-E 2020 (Opticos Studios)
import pygame, sys, random
from pygame.locals import *
import pygame.gfxdraw

version = "1.4.1"

def screensize():
    info = str(pygame.display.Info())
    w_index = info.index("current_w")
    c_index = info[w_index:].index(",")
    width = int(info[w_index + 12:c_index + w_index])
    h_index = info.index("current_h")
    height = int(info[h_index + 12:-3])
    return [width, height]

class layer:
    def __init__(self, size, distance, layer_depth=None):
        self.surface = pygame.Surface(size, SRCALPHA).convert_alpha()
        self.surface.fill([0, 0, 0, 0])
        self.distance = distance
        self.depth = layer_depth
        self.id = str(random.randrange(1000, 10000))
        if layer_depth == None:
            self.depth = 0
    def clear(self):
        self.surface.fill([0, 0, 0, 0])
    def blit(self, surface, pos, rect=None):
        if rect == None:
            self.surface.blit(surface, pos)
        else:
            self.surface.blit(surface, pos, rect)
            
pygame.init()
print("py2stereo " + version)
print("Hello from Opticos Studios. https://sites.google.com/bartimee.com/opticos-studios")
def init():
    pygame.init()

class display:
    def __init__(self, size):
        self.set_mode(size)
    def set_mode(self, size):
        #set the screen up
        self.window_size = screensize()
        self.unscaled_size = size
        self.size = size
        self.screen = pygame.display.set_mode(self.window_size, FULLSCREEN|HWSURFACE|DOUBLEBUF)
        self.screen.fill([0, 0, 0])
        self.clock = pygame.time.Clock()
        self.unit = 10#inches
        self.layers = []
        #the size of each virtual screen
        self.size = size
        self.auto_depth = False
        self.eye_distance = 10
        self.caption = ""
        self.font = pygame.font.Font("osl.ttf", 50)
        caption = self.font.render(self.caption + " py2stereo " + version, True, [255, 255, 255])
        self.screen.blit(caption, [10, 10])
        pygame.display.update()
        self.mode = "double"
        return self.screen
    
    def set_caption(self, caption):
        self.caption = caption
    def set_stereo_mode(self, mode):
        self.mode = mode
    def set_eye_distance(self, pixels_between_eyes):
        self.eye_distance = pixels_between_eyes
    def set_auto_depth(self, boolean):
        self.auto_depth = boolean
    def sort_layers(self):
        depth_in_order = []
        for layer_num in range(len(self.layers)):
            this_layer = self.layers[layer_num]
            depth_in_order.append(str(this_layer.depth) + "_" + str(this_layer.id))
            
        depth_in_order.sort()
        ids = []
        for i in depth_in_order:
            ind = i.index("_")
            ids.append(i[ind + 1:])
        layers = []
        for i in ids:
            for l in self.layers:
                if l.id == i:
                    layers.append(l)
        self.layers = layers
    def add_layer(self, depth):
        new_layer = layer(self.size, depth, len(self.layers))
        self.layers.append(new_layer)
        self.sort_layers()
    def set_unit(self, pixels_per_unit):
        self.unit = pixels_per_unit

    def update(self):
        window_size = pygame.display.get_window_size()
        self.screen.fill([0, 0, 0])
        self.clock.tick(90)
        canvas = self.screen
        aspect = "landscape"
        if self.unscaled_size[1] >= self.unscaled_size[0]:
            aspect = "portrait"
            
        if self.mode == "double":
            if aspect == "landscape":
                eye_size = [int(window_size[0] / 2), int((self.unscaled_size[1] / self.unscaled_size[0]) * int(window_size[0] / 2))]
            else:
                eye_size = [int((self.unscaled_size[0] / self.unscaled_size[1]) * int(window_size[1] / 1.5)), int(window_size[1] / 1.5)]
        else:
            if aspect == "landscape":
                eye_size = [int(window_size[0] / 1.3), int((self.unscaled_size[1] / self.unscaled_size[0]) * int(window_size[0] / 1.3))]
            else:
                eye_size = [int((self.unscaled_size[0] / self.unscaled_size[1]) * int(window_size[1] / 1.4)), int(window_size[1] / 1.4)]
        left_eye = pygame.Surface(eye_size)
        right_eye = pygame.Surface(eye_size)
        unit = self.unit
        if self.auto_depth == True:
            big_dist = unit * (1 + ((self.layers[0].distance) / 1.0)) * len(self.layers) - 1
        else:
            big_dist = unit * (1 + ((self.layers[0].distance) / 1.0))
        if self.mode == "double":
            #left eye
            left_pos = 0
            dep = len(self.layers) - 1
            for layer in self.layers:
                l = pygame.transform.scale(layer.surface, eye_size)
                if self.auto_depth == True:
                    offset = unit * (1 + (layer.distance / 1.0)) * dep
                else:
                    offset = unit * (1 + (layer.distance / 1.0))
                left_eye.blit(l, [offset, 0])
                dep -= 1
                
            #right eye
            right_pos = int(window_size[0] / 2)
            dep = len(self.layers) - 1
            for layer in self.layers:
                l = pygame.transform.scale(layer.surface, eye_size)
                if self.auto_depth == True:
                    offset = unit * (1 + (layer.distance / 1.0)) * dep
                else:
                    offset = unit * (1 + (layer.distance / 1.0))
                right_eye.blit(l, [-offset, 0])
                dep -= 1

            eye_distance = self.eye_distance
            
            canvas.blit(left_eye, [int(window_size[0] / 2) - left_eye.get_width() + big_dist - int(eye_distance / 2), int((window_size[1] / 2) - eye_size[1] / 2)], [big_dist, 0, eye_size[0], eye_size[1]])
            
            canvas.blit(right_eye, [window_size[0] / 2 + int(eye_distance / 2), int((window_size[1] / 2) - eye_size[1] / 2)], [0, 0, eye_size[0] - big_dist, eye_size[1]])
            #clear the old layers
            for l in self.layers:
                l.clear()
            #draw caption
            
            font_size = int(0.7 * int((window_size[1] / 2) - eye_size[1] / 2))
            if font_size < 50:
                self.font = pygame.font.Font("osl.ttf", font_size)
            caption = self.font.render(self.caption + " py2stereo " + version, True, [255, 255, 255])
            canvas.blit(caption, [10, 0])
            
        if self.mode == "rb":
            #left eye
            left_pos = 0
            dep = len(self.layers) - 1
            for layer in self.layers:
                l = pygame.transform.scale(layer.surface, eye_size)
                if self.auto_depth == True:
                    offset = unit * (1 + (layer.distance / 1.0)) * dep
                else:
                    offset = unit * (1 + (layer.distance / 1.0))
                left_eye.blit(l, [offset, 0])
                dep -= 1
                
            #right eye
            right_pos = int(window_size[0] / 2)
            dep = len(self.layers) - 1
            for layer in self.layers:
                l = pygame.transform.scale(layer.surface, eye_size)
                if self.auto_depth == True:
                    offset = unit * (1 + (layer.distance / 1.0)) * dep
                else:
                    offset = unit * (1 + (layer.distance / 1.0))
                right_eye.blit(l, [-offset, 0])
                dep -= 1

            eye_distance = self.eye_distance
            
            pygame.gfxdraw.filled_polygon(left_eye, [[0, 0],
                                                     [eye_size[0], 0],
                                                     [eye_size[0], eye_size[1]],
                                                     [0, eye_size[1]]], [255, 0, 0, 100])
            left_eye.set_alpha(255)

            canvas.blit(left_eye, [int(window_size[0] / 2) - (left_eye.get_width() / 2) + (big_dist / 2.0), int((window_size[1] / 2) - eye_size[1] / 2)], [big_dist, 0, eye_size[0], eye_size[1]])


            pygame.gfxdraw.filled_polygon(right_eye, [[0, 0],
                                                     [eye_size[0], 0],
                                                     [eye_size[0], eye_size[1]],
                                                     [0, eye_size[1]]], [0, 0, 255, 100])
            right_eye.set_alpha(255 / 2)

            canvas.blit(right_eye, [int(window_size[0] / 2) - (right_eye.get_width() / 2) + (big_dist / 2.0), int((window_size[1] / 2) - eye_size[1] / 2)], [0, 0, eye_size[0] - big_dist, eye_size[1]])

            #clear the old layers
            for l in self.layers:
                l.clear()
            #draw caption
            caption = self.font.render(self.caption + " py2stereo " + version, True, [255, 255, 255])
            canvas.blit(caption, [10, 10])
        pygame.display.update()
    
        
        
   
        
