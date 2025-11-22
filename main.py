import pgzero 
import pgzrun
from pgzero.builtins import Actor, animate, keyboard
from zombie import Zombies

#enemies = []
#enemies.append(
#for i in range(5):



WIDTH = 900
HEIGHT = 700
TITLE = "Minecraft Survivor Test"

#zombies
zombieb = Zombies(0,0)

horda = zombieb.create_zombie_tsunami()

#player
player = Actor("steve-1")
player.x = 32
player.y = 32
player.pos = [WIDTH // 2, HEIGHT // 2]
player.images = ["steve-1", "steve-2", "steve-3", "steve-4"]
player.height = 64
player.width = 64
player.speed = 1
player.size = (64, 64)
frame_index = 0
animation_timer = 0

def update_player_animation(dt):
    global frame_index, animation_timer
    animation_timer += dt
    if animation_timer >= 0.25:  # a cada 0.25s
        animation_timer = 0
        frame_index = (frame_index + 1) % 4
        player.image = player.images[frame_index]

#Update function ---------------------------ss---------------------------
def update(dt):
    global frame_index, animation_timer, horda

    moving = False

    # Moviment
    if keyboard.w:
        player.y -= player.speed
        moving = True
    if keyboard.s:
        player.y += player.speed
        moving = True
    if keyboard.a:
        player.x -= player.speed
        moving = True
    if keyboard.d:
        player.x += player.speed
        moving = True


    for zombie in horda:
        zombie.walking_zombie(dt, player)

    # Tempo entre quadros da animação
    if moving:
        update_player_animation(dt)

    
forest = []
for j in range(5):
    for i in range(5):
        forest.append(
            Actor('grass_bg', topleft=(images.grass_bg.get_width() * i, images.grass_bg.get_height() * j))
        )
#Draw function 
def draw():
    screen.clear()
    #background has to be drawn first
    for grass in forest:
        grass.draw()
    for zombie in horda:
        zombie.draw()
    player.draw()



pgzrun.go()