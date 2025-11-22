import math
import pgzero 
import pgzrun
from pgzero.builtins import Actor, animate, keyboard
from zombie import Zombies #import my zombie class
from player import Player #import my player class

WIDTH = 900
HEIGHT = 700
TITLE = "Minecraft Survivor Test"

chicken = Actor("frango_assado", topleft=(100, 100))
enchanted_book = Actor("livro_encantado", topleft=(400, 300))

#zombies
zombieb = Zombies(0,0)

horda = zombieb.create_zombie_tsunami()

#player
player = Player(WIDTH//2, HEIGHT//2)


# function to separate enemies, and not overlap. Generated with help from ChatGPT
def separate_enemies(enemies,player):
    for i in range(len(enemies)):
        for j in range(i + 1, len(enemies)):
            a = enemies[i]
            b = enemies[j]

            # separate enemy from player 
            pdx = player.actor.x - a.actor.x
            pdy = player.actor.y - a.actor.y
            pdist = math.hypot(pdx, pdy)
            min_pdist = a.radius + player.radius
            if pdist < min_pdist and pdist != 0:
                poverlap = min_pdist - pdist
                pnx = pdx / pdist
                pny = pdy / pdist

                # push the enemy away from the player
                a.actor.x -= pnx * poverlap
                a.actor.y -= pny * poverlap

            # separate enemies from each other
            dx = b.actor.x - a.actor.x
            dy = b.actor.y - a.actor.y
            dist = math.hypot(dx, dy) # Note: math.hypot computes sqrt(dx*dx + dy*dy)
            min_dist = a.radius + b.radius

            if dist < min_dist and dist != 0:# Note: create a normal vector
                overlap = min_dist - dist
                nx = dx / dist
                ny = dy / dist

                # push each enemy 50% of the overlap
                a.actor.x -= nx * overlap * 0.5
                a.actor.y -= ny * overlap * 0.5
                b.actor.x += nx * overlap * 0.5
                b.actor.y += ny * overlap * 0.5

#Update function ------------------------------------------------------
def update(dt):
    global player, horda
    separate_enemies(horda, player)

    
    # Moviment

    for zombie in horda:
        zombie.walking_zombie(dt, player)

    player.update_player(dt, keyboard)

    
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
    chicken.draw()
    



pgzrun.go()