import pygame
import time
import math
from utils import scale_image, blit_rotate_center, text
import os, sys

pygame.font.init()
pygame.mixer.init()

f = open('score.txt','r')
k = f.read()
bonus = int(k)

print(k)

#loading all assests

music= pygame.mixer.music.load('sounds/bg.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

acc_sound = pygame.mixer.Sound('sounds/acc.wav')
col_sound = pygame.mixer.Sound('sounds/collision.wav')
GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load("imgs/pitstop_car_1.png"), 0.035)
CMP_CAR = scale_image(pygame.image.load("imgs/pitstop_car_19.png"), 0.04)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

main_font = pygame.font.SysFont('comicsans',30)

FPS = 60
PATH = [(137, 51), (40, 165), (58, 462), (268, 720), (410, 693), (423, 503), (581, 493), (614, 707), (753, 714), (747, 534), (715, 359), (415, 354), (426, 255), (712, 240), (720, 67), (308, 77), (253, 304), (231, 433), (144, 338), (178, 259)]

# a class to handle the information of the game
class Info:
    LEVELS =5  #max level

    def __init__(self,level=1):
        self.lvl = level
        self.started = False
        self.level_start_time = 0

    def nxtlvl(self):
        self.lvl +=1
        self.started = False

    def reset(self):
        self.lvl = 1
        self.started = False
        self.level_start_time = 0

    def game_fns(self):  #checking game finsished
        return self.lvl > self.LEVELS
    
    def start(self):
        self.started = True
        self.level_start_time = time.time()

    def get_lvl_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)  #returning the game time per lvl






class AbstractCar:  #class to handle the generic behavior of both computer and player car
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1 + bonus*0.5

    def rotate(self, left=False, right=False):  #checking rotation
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):#putting rotated car on screen 
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):#checking collision with help of mask of track border with car
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):#class specific to player car
    IMG = RED_CAR
    START_POS = (180, 195)

    def reduce_speed(self):#physics to account for constant deceleration
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self): #make the car jump back when touch the track border and play sound
        self.vel = -self.vel/8
        col_sound.play()
        self.move()

        


def draw(win, images, player_car,computer_car,game_info):  #to show all the images on the window
    for img, pos in images:
        win.blit(img, pos)

    #showing information related to text at bottom hand corner
    time_txt = main_font.render(f"Level {game_info.lvl}",1,(255,255,255))
    win.blit(time_txt,(10,630))

    lvl_txt = main_font.render(f"Time: {game_info.get_lvl_time()}s",1,(255,255,255))
    win.blit(lvl_txt,(10,670))

    vel_txt = main_font.render(f"Velocity {round(player_car.vel,2)}px/s",1,(255,255,255))
    win.blit(vel_txt,(10,710))

    acc_txt = main_font.render(f"accleration: {round(player_car.acceleration,2)}px/s",1,(255,255,255))
    win.blit(acc_txt,(10,750))


    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()



class ComputerCar(AbstractCar):#class specific to computer car
    IMG = CMP_CAR
    START_POS = (155,195)

    def __init__(self,max_vel,rotation_vel,path=[]):
        super().__init__(max_vel,rotation_vel)
        self.path = path #coordinates of the points for car to follow
        self.current_point = 0
        self.vel = max_vel


    def draw_points(self,win):  #assigning the points to to computer to follow
        for point in self.path:
            pygame.draw.circle(win,(255,0,0),point,5)

    def draw(self,win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):#checking angle at each point for the car to follow
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff ==0:
            desired_radian_angle = math.pi/2 
        else:
            desired_radian_angle = math.atan(x_diff/y_diff) #at any arbitary point checking angle with the target point

        if target_y > self.y:
            desired_radian_angle+=math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)

        if difference_in_angle >=180:
            difference_in_angle -=360

        if difference_in_angle >0:
            self.angle-=min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle+=min(self.rotation_vel, abs(difference_in_angle))

    
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x,self.y, self.img.get_width(), self.img.get_height())

        if rect.collidepoint(*target):  #checking if touching the points
            self.current_point +=1




    def move(self):
        if self.current_point >= len(self.path):
            return
        
        self.calculate_angle()
        self.update_path_point()
        super().move()

    def nxt_lvl(self,level):
        self.reset()
        self.vel = self.max_vel + (level - 1)*0.4  #increasing velocity of computer car
        self.current_point = 0



def move_player(player_car):#assigning keys to move the player car
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        acc_sound.play()
        moved = True
        player_car.move_forward() 
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player,comp,info): #using mask to check for collision with border and finish line
    if player_car.collide(TRACK_BORDER_MASK) != None:
        
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)

    if computer_finish_poi_collide!=None:
        text(WIN, main_font,'You Lost!')
        pygame.quit()
    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
   
    if player_finish_poi_collide != None: #not allowing the player car to g0 behind the finish line
        if player_finish_poi_collide[1] == 0: #checking if player has touched finish line then implement bouce to prevent going backwards
            player_car.bounce()
        else:
            game_info.nxtlvl()
            player_car.reset()
            computer_car.nxt_lvl(game_info.lvl)

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
#instance of the all the classes
player_car = PlayerCar(4, 8)
computer_car = ComputerCar(2, 16,PATH)
game_info = Info()

#main loop constantly checking for updates on the map
while run:
    clock.tick(FPS)

    draw(WIN, images, player_car,computer_car,game_info)



    while not game_info.started:
        text(WIN, main_font, f'Press any key to start level {game_info.lvl}!')
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.start()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     computer_car.path.append(pos)
        

    move_player(player_car)
    computer_car.move()

    handle_collision(player_car,computer_car,game_info)

    if game_info.game_fns():
        text(WIN, main_font,'You WON!')
        pygame.time.wait(5000)
        game_info.reset()
        pygame.quit()
        player_car.reset()
        computer_car.reset()
        
    
pygame.quit()
