import math
import random
import pgzero 
import pgzrun
from pgzero.builtins import Actor, animate, keyboard, clock
from zombie import Zombies #import my zombie class
from player import Player #import my player class
from bow_arrow import  Bow, arrow #import my bow class

WIDTH = 900
HEIGHT = 700
TITLE = "Minecraft Survivor Test"




forest = []
for j in range(5):
    for i in range(5):
        forest.append(
            Actor('grass_bg', topleft=(images.grass_bg.get_width() * i, images.grass_bg.get_height() * j))
        )
chickens = []
chicken_spawn_timer = 20.0


#player
player = Player(WIDTH//2, HEIGHT//2)
arrows = []
arrow_cooldown = 3.0
texto_xp = "Player level: {} \nXP: {}/{}".format(player.level, player.xp, (2*player.level + 7))
texto_vida = "Player Health: {}/{}".format(player.health, player.max_health)





# function to separate enemies, and not overlap. Generated with help from ChatGPT
def separate_enemies(enemies,player):
    for i in range(len(enemies)):
        for j in range(i + 1, len(enemies)):
            a = enemies[i]
            b = enemies[j]

            # separate enemy from player 
            pdx = player.actor.x - b.actor.x
            pdy = player.actor.y - b.actor.y
            pdist = math.hypot(pdx, pdy)
            min_pdist = b.radius + player.radius
            if pdist < min_pdist and pdist != 0:
                poverlap = min_pdist - pdist
                pnx = pdx / pdist
                pny = pdy / pdist

                # push the enemy away from the player
                b.actor.x -= pnx * poverlap
                b.actor.y -= pny * poverlap

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

#zombies
zombieb = Zombies(0,0,player)
horda_cooldown = 15.0
horda = zombieb.create_zombie_tsunami(player)

time = 0
texto_tempo = "Time: {:.1f} s".format(time)
texto_horda = "Horda em: {:.1f} s".format(horda_cooldown)

#Update function ------------------------------------------------------
def update(dt):
    global player, horda, arrows, arrow_cooldown, horda_cooldown, texto_xp, texto_vida, chicken_spawn_timer, chickens, texto_tempo, time
    texto_xp = "Player level: {} \nXP: {}/{}".format(player.level, player.xp, (2*player.level + 7))
    texto_vida = "Player Health: {}/{}".format(player.health, player.max_health)
    texto_horda = "Horda em: {:.1f} s".format(horda_cooldown)
    time += dt
    texto_tempo = "Time: {:.1f} s".format(time)
    if horda_cooldown <= 0:
        new_horda = zombieb.create_zombie_tsunami(player)
        horda.extend(new_horda)
        horda_cooldown = 15.0
    horda_cooldown -= dt
    separate_enemies(horda, player)


    chicken_spawn_timer -= dt
    if chicken_spawn_timer <= 0 and random.randint(0,10)% 2 == 0:
        chicken = Actor("frango_assado", topleft=(random.randint(0, WIDTH),random.randint(0, HEIGHT)))
        chicken.radius = 20
        chicken.heal = 5
        chickens.append(chicken)
        chicken_spawn_timer = 20.0

    for chicken in chickens[:]:
        dx = chicken.x - player.actor.x
        dy = chicken.y - player.actor.y
        dist = math.hypot(dx, dy)

        if dist < chicken.radius + player.radius:
            chickens.remove(chicken)
            player.heal(chicken.heal)
            print("Player has been healed.") #test



    for zombie in horda:
        zombie.walking_zombie(dt, player)
        if zombie.life <= 0:
            horda.remove(zombie)
        dx = zombie.actor.x - player.actor.x
        dy = zombie.actor.y - player.actor.y
        dist = math.hypot(dx, dy)

        if dist < zombie.radius + player.radius and player.invulnerable <= 0:
            if player.receive_damage(zombie.damage):
                print("Player has died! Game Over.") #test
            player.actor.image = "steve_damage"
            player.invulnerable = 1.0  # 1.0 seconds of invulnerability
        player.invulnerable -= dt

    # Moviment
    player.update_player(dt, keyboard)
    if arrow_cooldown <= 0:
        new_arrow = arrow(player.actor.x, player.actor.y)
        new_arrow.aim_at(horda)   # sets dx, dy, angle
        arrows.append(new_arrow)
        arrow_cooldown = 3.5 - player.level * 0.5
        if arrow_cooldown < 0.7:
            arrow_cooldown = 0.7

    arrow_cooldown -= dt

    for arr in arrows[:]:
        if arr.update(horda):
            arrows.remove(arr)
    

#Draw function 
def draw():
    screen.clear()
    
    #background has to be drawn first
    for grass in forest:
        grass.draw()
    for zombie in horda:
        zombie.draw()
    player.draw()
    for arr in arrows:
        arr.draw()

    for chicken in chickens:
        chicken.draw()
    screen.draw.text(texto_xp, (10, 10), color="white")
    screen.draw.text(texto_vida, (10, 50), color="white")
    screen.draw.text(texto_tempo, (700, 10), color="white")
    



pgzrun.go()