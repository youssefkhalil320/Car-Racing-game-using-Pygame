#importing used packages 
import pygame 
import time 
import math 
import time 
from utils import scale_image , blit_rotate_center
from pygame import mixer 

#identifing the parts 
GRASS = pygame.image.load(r"images\grass.png")
TRACK = pygame.image.load(r"images\track.png")
TRACK_BORDER = pygame.image.load(r"images\track-border.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load(r"images\finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS= (130, 250)
YELLOW_CAR = scale_image(pygame.image.load(r"images\yellow_car.png"),0.09)   
RED_CAR = scale_image(pygame.image.load(r"images\RED_CAR.png"),0.04) 
pygame.mixer.init()
driving_sound = mixer.Sound('driving2.wav')
#initializing the window 
WIDTH , HEIGHT = TRACK.get_width() , TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Top Racer1")
pygame.font.init()
BLACK = (0, 0, 0)


#Running the screen 
FBS = 60
PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]
run = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
myfont = pygame.font.SysFont('Comic Sans MS', 55)
frame_count = 0
start_time = 90

class AbstractCar:
    def __init__(self,max_vel,rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left= False , right = False):
        if left:
            self.angle += self.rotation_vel
        if right: 
            self.angle -= self.rotation_vel

    def draw(self,win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        driving_sound.play()
        self.move()

    def stop_moving(self):
        self.vel = 0
        self.move()    

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()    
    
    def bounce(self):
        self.vel = -(self.vel/2)
        self.move()
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def move_player(player):
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT]:
            player_car.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            player_car.rotate(right=True)  
        if keys[pygame.K_UP]:
            moved = True
            player_car.move_forward()
        if keys[pygame.K_DOWN]:
            moved = True
            player_car.move_backward()
        if keys[pygame.K_SPACE]:
            moved = True
            player_car.stop_moving()    
        if not moved:
            player_car.reduce_speed()   


    def move_player_two(player):
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_a]:
            computer_car.rotate(left=True)
        if keys[pygame.K_d]:
            computer_car.rotate(right=True)  
        if keys[pygame.K_w]:
            moved = True
            computer_car.move_forward()
        if keys[pygame.K_s]:
            moved = True
            computer_car.move_backward()
        if keys[pygame.K_f]:
            moved = True
            computer_car.stop_moving()    
        if not moved:
            computer_car.reduce_speed()        


    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()     

    def reset(self):
        self.x , self.y = self.START_POS
        self.vel = 0
        self.angle = 0


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (190,200)

class ComputerCar(AbstractCar):
    IMG = YELLOW_CAR 
    START_POS = (160,170)

    

def draw(win, images,player_car,computer_car):
    for image, pos in images :
        win.blit(image,pos)
    player_car.draw(win)   
    computer_car.draw(win) 
    pygame.display.update()

images = [(GRASS,(0,0)), (TRACK,(0,0)),(FINISH, FINISH_POS), (TRACK_BORDER, (0, 0))]      
player_car = PlayerCar(8,4) 
computer_car = ComputerCar(4,4) 


for i in range(0,10):
    player_car.move_forward()
    computer_car.move_forward()
    
player_car.stop_moving() 

while run:
    draw(WIN, images,player_car,computer_car)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    computer_car.move()

    AbstractCar.move_player(player_car)
    AbstractCar.move_player_two(computer_car)

    total_seconds = start_time - (frame_count // FBS)
    if total_seconds < 0:
        total_seconds = 0
 
    # Divide by 60 to get total minutes
    minutes = total_seconds // 60
 
    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60
 
    # Use python string formatting to format in leading zeros
    output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
 
    # Blit to the screen
    text = font.render(output_string, True, BLACK)
 
    WIN.blit(text, [500, 850])
 
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    frame_count += 1
 
    # Limit frames per second
    clock.tick(FBS)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    
    
    if minutes != 0 and seconds != 0:
        if player_car.collide(TRACK_BORDER_MASK) != None:
            player_car.bounce()
        finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POS)
        if finish_poi_collide != None:
            if finish_poi_collide[1] == 0:
                player_car.bounce()
            else:
                textsurface = myfont.render('RED car Won', False, (0, 0, 0)) 
                WIN.blit(textsurface, [250, 250])
                pygame.display.flip()
                time.sleep(3)
                player_car.reset()
                computer_car.reset()

        if computer_car.collide(TRACK_BORDER_MASK) != None:
            computer_car.bounce()
        finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POS)
        if finish_poi_collide != None:
            if finish_poi_collide[1] == 0:
                computer_car.bounce()
            else:
                textsurface = myfont.render('Yellow car Won ', False, (0, 0, 0))   
                WIN.blit(textsurface, [250, 250]) 
                pygame.display.flip()    
                time.sleep(3) 
                computer.reset()
                player_car.reset()

    else:
        textsurface = myfont.render('Time Out', False, (0, 0, 0)) 
        WIN.blit(textsurface, [250, 250])
        pygame.display.flip()
        time.sleep(3)
        player_car.reset()
        computer_car.reset()


       
pygame.quit()            


