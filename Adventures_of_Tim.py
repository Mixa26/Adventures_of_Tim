import pygame
pygame.init()
pygame.font.init()
#screen size
scrx = 1920
scry = 1080

#fps setup
clock = pygame.time.Clock()
FPS = 60

#character textures
Tim_left = pygame.image.load('Tim_L.png')
Tim_right = pygame.image.load('Tim_R.png')
Tim_up = pygame.image.load('Tim_UP.png')
Tim_down = pygame.image.load('Tim.png')

Fred_left = pygame.image.load('Fred_L.png')
Fred_right = pygame.image.load('Fred_R.png')
Fred_up = pygame.image.load('Fred_UP.png')
Fred_down = pygame.image.load('Fred.png')

Ghastle_left = pygame.image.load('Ghastle_L.png')
Ghastle_right = pygame.image.load('Ghastle_R.png')
Ghastle_up = pygame.image.load('Ghastle.png')
Ghastle_down = pygame.image.load('Ghastle.png')

#additional char reactions
Fred_right_spooked = pygame.image.load('Fred_R_spooked.png')

#main content upload
#main media
window = pygame.display.set_mode((scrx, scry))
caption = pygame.display.set_caption('Adventures of Tim')
logo = pygame.image.load('Adventures_of_Tim_logo.png')
pygame.display.set_icon(logo)
#backgrounds 'rooms'
background = pygame.image.load('background.png')
background2 = pygame.image.load('background2.jpg')
background3 = pygame.image.load('background3.png')
#music
music = pygame.mixer.music.load('circles.mp3')
pygame.mixer.music.play(-1)
#pictures emotes
questionmark = pygame.image.load('questionmark.png')
explanationmark = pygame.image.load('explanationmark.png')

#main conversation upload
interact1 = pygame.image.load('Fred_interact1.png')
interact2 = pygame.image.load('Fred_interact2.png')
interact3 = pygame.image.load('Fred_interact3.png')

class player():
    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.vel = 10
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def draw(self,window,char_l,char_r,char_up,char_down):
        if self.left:
            window.blit(char_l, (self.x, self.y))
        elif self.right:
            window.blit(char_r, (self.x, self.y))
        elif self.up:
            window.blit(char_up, (self.x, self.y))
        elif self.down:
            window.blit(char_down, (self.x, self.y))
        else:
            window.blit(char_down, (self.x, self.y))

def player_movement_left():
    Tim.x -= Tim.vel
    if fredstand > 0:
        Fred.x -= Tim.vel
        Fred.left = True
        Fred.right = False
        Fred.up = False
        Fred.down = False
    Tim.left = True
    Tim.right = False
    Tim.up = False
    Tim.down = False

def player_movement_right():
    Tim.x += Tim.vel
    if fredstand > 0:
        Fred.x += Tim.vel
        Fred.left = False
        Fred.right = True
        Fred.up = False
        Fred.down = False
    Tim.left = False
    Tim.right = True
    Tim.up = False
    Tim.down = False

def player_movement_up():
    Tim.y -= Tim.vel
    if fredstand > 0:
        Fred.y -= Tim.vel
        Fred.left = False
        Fred.right = False
        Fred.up = True
        Fred.down = False
    Tim.left = False
    Tim.right = False
    Tim.up = True
    Tim.down = False

def player_movement_down():
    Tim.y += Tim.vel
    if fredstand > 0:
        Fred.y += Tim.vel
        Fred.left = False
        Fred.right = False
        Fred.up = False
        Fred.down = True
    Tim.left = False
    Tim.right = False
    Tim.up = False
    Tim.down = True

class room():
    def __init__(self, room, previous_room, refreshroom):
        self.room = room
        self.previous_room = previous_room
        self.refreshroom = refreshroom

    def room_up(self):
        if self.room == 1:
            if Tim.x + 80 > scrx - 50 and fredstand > 0:
                self.room += 1
                self.previous_room = self.room - 1
                self.refreshroom = 1

        if self.room == 2:
            if Tim.y < 550:
                self.room += 1
                self.previous_room = self.room - 1
                self.refreshroom = 1

    def room_down(self):
        if Tim.x < scrx - 1870:
            if self.room != 1:
                self.room -= 1
                self.previous_room = self.room + 1
                self.refreshroom = 1

    def draw_characters(self):
        if self.room == 1 and self.refreshroom == 1:
            Tim.x = 1770
            Tim.y = 720
            if fredstand == 0:
                Fred.x = 1400
                Fred.y = 650
            else:
                Fred.x = Tim.x - 100
                Fred.y = Tim.y - 78
            self.refreshroom = 0

        elif self.room == 2 and self.refreshroom == 1:
            if self.previous_room == 3:
                Tim.x = 1350
                Tim.y = 550
                Fred.x = Tim.x - 100
                Fred.y = Tim.y - 78
                self.refreshroom = 0
            else:
                Tim.x = 200
                Tim.y = 720
                Fred.x = Tim.x - 100
                Fred.y = Tim.y - 78
                self.refreshroom = 0
        elif self.room == 3 and self.refreshroom == 1:
            Tim.x = 200
            Tim.y = 720
            Fred.x = Tim.x - 100
            Fred.y = Tim.y - 78
            Ghastle.x = 1600
            Ghastle.y = 650
            self.refreshroom = 0

    def walk_collision_left(self):
        if self.room == 1:
            return Tim.x - Tim.vel > 0
        if self.room == 2:
            if Tim.y < 720:
                return Tim.x > 1250
            else:
                return Tim.x - Tim.vel > 0
        if self.room == 3:
            return Fred.x - Tim.vel > 0

    def walk_collision_right(self):
        if self.room == 1 or self.room == 3:
            return Tim.x + Tim.vel < scrx - 50
        if self.room == 2:
            if Tim.y < 720:
                return Tim.x < 1450
            else:
                return Tim.x + Tim.vel < scrx - 50

    def walk_collision_up(self):
        if self.room == 1 or self.room == 3:
            return Tim.y - Tim.vel > 720
        if self.room == 2:
            if Tim.x > 1249 and Tim.x < 1451:
                return Tim.y - Tim.vel > 530
            elif Tim.x < 1249 or Tim.x > 1451:
                return Tim.y - Tim.vel > 720

    def walk_collision_down(self):
        if self.room == 1 or self.room == 3:
            return Tim.y + Tim.vel < scry - 100
        if self.room == 2:
            return Tim.y + Tim.vel < scry - 100

fredstand = 0

Tim = player(800, 720)
if fredstand == 0:
    Fred = player(1400, 650)
Ghastle = player(1600, 650)

Mainenvironment = room(1, 1, 0)
#determines which character is infront/behind the other
def drawcharschedule():
    if Mainenvironment.room == 1:
        if Tim.y - 85 > Fred.y:
            Fred.draw(window, Fred_left, Fred_right, Fred_up, Fred_down)
            Tim.draw(window, Tim_left, Tim_right, Tim_up, Tim_down)
        elif Tim.y - 85 < Fred.y:
            Tim.draw(window, Tim_left, Tim_right, Tim_up, Tim_down)
            Fred.draw(window, Fred_left, Fred_right, Fred_up, Fred_down)
    elif Mainenvironment.room == 2:
        Tim.draw(window, Tim_left, Tim_right, Tim_up, Tim_down)
        Fred.draw(window, Fred_left, Fred_right, Fred_up, Fred_down)
    elif Mainenvironment.room == 3:
        Tim.draw(window, Tim_left, Tim_right, Tim_up, Tim_down)
        Fred.draw(window, Fred_left, Fred_right, Fred_up, Fred_down)
        Ghastle.draw(window, Ghastle_left, Ghastle_right, Ghastle_up, Ghastle_down)

#draws everything on the screen and refreshes it
def redrawgamewindow():
    roomdraw()
    if fredstand == 0:
        interactwithfred()
    drawcharschedule()
    talktext1()
    talktext2()
    talktext3()
    pygame.display.update()

def roomdraw():
    if Mainenvironment.room == 1:
        window.blit(background, (0, 0))
        if fredstand == 0:
            window.blit(explanationmark, (Fred.x - 44, Fred.y - 44))
    elif Mainenvironment.room == 2:
        window.blit(background2, (0, 0))
    elif Mainenvironment.room == 3:
        window.blit(background3, (0,0))

def talktext1():
    if Mainenvironment.room == 1 and abs(Tim.x - Fred.x) <= 200:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                window.blit(interact1, (0, 774))
            if fredstand == 0 and (abs(Tim.x - Fred.x) <= 200 and abs(Tim.y - Fred.y) <= 250):
                try:
                    if event.key == pygame.K_f:
                        fredfollowstim()
                except:
                    print('Please don\'t use your mouse.')

def talktext2():
    if Mainenvironment.room == 2 and Tim.x > 1100:
        window.blit(questionmark, (1350, 450))
        if Tim.y < 700:
            window.blit(interact2, (0,774))
            Tim.left = False
            Tim.right = False
            Tim.up = True
            Tim.down = False
            Fred.left = False
            Fred.right = False
            Fred.up = True
            Fred.down = False

def talktext3():
    global spooked
    global move
    move_var = 0
    if Mainenvironment.room == 3 and Ghastle.x > 1915:
        if spooked:
            window.blit(interact3, (0, 0))
            Fred.draw(window, Fred_left, Fred_right_spooked, Fred_up, Fred_down)
            Fred.left = False
            Fred.right = True
            Fred.up = False
            Fred.down = False
            move = False
            if pygame.event == pygame.KEYDOWN:
                if pygame.key == pygame.K_e:
                    move_var += 1
                    if move_var > 0:
                        move = True
                        spooked = False

def interactwithfred():
    font = pygame.font.SysFont(None, 25)
    text = font.render('Press E to interact', False, (255, 255, 255))
    if abs(Tim.x - Fred.x) <= 200 and abs(Tim.y - Fred.y) <= 250:
        window.blit(text, (1300, 595))

def fredstands():
    if fredstand == 0:
        if abs(Tim.x - Fred.x) <= 200 and abs(Tim.y - Fred.y) <= 150:
            if Tim.x - Fred.x < 0:
                Fred.left = True
                Fred.right = False
                Fred.up = False
                Fred.down = False
            elif Tim.x - Fred.x > 0:
                Fred.left = False
                Fred.right = True
                Fred.up = False
                Fred.down = False
        else:
            Fred.left = False
            Fred.right = False
            Fred.up = False
            Fred.down = True

def fredfollowstim():
    global fredstand
    global Fred
    fredstand += 1
    Fred = player(Tim.x - 100, Tim.y - 78)

def checkpoint1music():
    global once
    if Mainenvironment.room == 3 and once:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('CaveAmbience.mp3')
        pygame.mixer.music.play(-1)
        once = False

def ghastle3():
    global once_ghastle
    if Tim.x > 250:
        Ghastle.left = False
        Ghastle.right = True
        Ghastle.up = False
        Ghastle.down = False
        if Ghastle.x < 1920:
            Ghastle.x += Ghastle.vel
            if Mainenvironment.room == 3:
                if once_ghastle:
                    effect = pygame.mixer.Sound('Ghastle_effect1.wav')
                    effect.play()
                    once_ghastle = False
    else:
        Ghastle.left = False
        Ghastle.right = False
        Ghastle.up = False
        Ghastle.down = True

run = True
once = True
once_ghastle = True
spooked = True
move = True

#main loop
while run:
    clock.tick(FPS)
#gets the input from the game
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

#input from the player
    pygame.event.pump()
    keys = pygame.key.get_pressed()

    if move:
        if keys[pygame.K_LEFT] and Mainenvironment.walk_collision_left():
            player_movement_left()

        if keys[pygame.K_RIGHT] and Mainenvironment.walk_collision_right():
            player_movement_right()

        if keys[pygame.K_UP] and Mainenvironment.walk_collision_up():
            player_movement_up()

        if keys[pygame.K_DOWN] and Mainenvironment.walk_collision_down():
            player_movement_down()

    fredstands()

#updates on_the screen
    Mainenvironment.room_up()
    if Mainenvironment.room != 3:
        Mainenvironment.room_down()
    Mainenvironment.draw_characters()
    checkpoint1music()
    ghastle3()
    redrawgamewindow()

pygame.quit()