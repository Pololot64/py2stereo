#this is a demo project.
import stereo
import pygame, random, sys
stereo.init()



screen = stereo.display([1366, 768])

screen.set_caption("test")

screen.add_layer(0)
screen.add_layer(0)
screen.add_layer(0)
screen.add_layer(0)
screen.add_layer(0)

screen.set_auto_depth(True)


screen.set_stereo_mode("double")
layers = screen.layers

back = pygame.image.load("back2.png").convert_alpha()
back = pygame.transform.scale(back, screen.size)

front = pygame.image.load("front2.png").convert_alpha()
front = pygame.transform.scale(front, screen.size)

#person = pygame.image.load("person.png").convert_alpha()


class ball:
    def __init__(self):
        self.vel = [random.randrange(-5, 5), random.randrange(-5, 5)]
        self.pos = [random.randrange(50, screen.size[0] - 50), random.randrange(50, screen.size[1] - 50)]
        self.color = [random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)]
    def draw(self, canvas):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] <= 50 or self.pos[0] >= screen.size[0] - 50:
            self.vel[0] *= -1
        if self.pos[1] <= 50 or self.pos[1] >= screen.size[1] - 50:
            self.vel[1] *= -1
        pygame.draw.circle(canvas, self.color, self.pos, 50)


balls = []
ball_num = 20
for i in range(ball_num):
    b = ball()
    balls.append(b)



while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pass
        """
            if screen.auto_depth == False:
                screen.set_auto_depth(True)
            else:
                screen.set_auto_depth(False)
            """
            
        
    layers[0].surface.blit(back, [0, 0])
    layers[1].surface.blit(front, [0, 0])
    for i in range(ball_num):
        range_num = int(ball_num / len(layers))
        rl = 0
        for r in range(len(layers)):
            if i < range_num and i > rl:
                balls[i].draw(layers[r].surface)
                
            range_num += int(ball_num / len(layers))
            rl += int(ball_num / len(layers))
    #layers[2].surface.blit(person, [screen.size[0] / 2 - person.get_width() / 2, screen.size[1] - person.get_height()])        
    
    screen.update()
