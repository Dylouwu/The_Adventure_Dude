#!/usr/bin/env python3
# -*- coding: utf-8 -*
import os, sys
with open(os.devnull, 'w') as f: #pour éviter le message pygame contributors
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame
from pygame.locals import *

#définition
clock = pygame.time.Clock() #définition pour la vitesse du jeu
pygame.init()
pygame.display.set_caption('The Adventure Dude')
format = (1280,720)
écran = pygame.display.set_mode(format,0,32)
affichage = pygame.Surface((450,300))
#---MUSIQUES---#
musique = pygame.mixer.Sound("Musiques/theme.wav")
musiquedebut = pygame.mixer.Sound("Musiques/musiquedebut.wav")
musiquefin = pygame.mixer.Sound("Musiques/musiquefin.wav")
musique.set_volume(0.2)
musiquedebut.set_volume(0.02)
musiquefin.set_volume(0.04)
#---IMAGES---#
écrantitre = pygame.image.load('Backgrounds/bg1.png')
écranfin = pygame.image.load('Backgrounds/bg2.png')
icone = pygame.image.load('icon.png')
#---Initialisation des premières variables---#
a_droite = False
a_gauche = False
tair = 0
vitesse_y = 0
intro = True
outro = False
caméra = [0,0]

def charge_carte(path):
    lecture_carte= open(path + '.txt','r')
    valeur_carte = lecture_carte.read()
    lecture_carte.close()
    valeur_carte = valeur_carte.split('\n') #sépare les rangées
    carte = [] #création de la matrice pour la carte
    for rangées in valeur_carte:
        carte.append(list(rangées))
    return carte

sable1 = pygame.image.load('Tiles/sable1.png')
sable2 = pygame.image.load('Tiles/sable2.png')
sable3 = pygame.image.load('Tiles/sable3.png')
roche1 = pygame.image.load('Tiles/roche1.png')
roche2 = pygame.image.load('Tiles/roche2.png')
roche3 = pygame.image.load('Tiles/roche3.png')
glace1 = pygame.image.load('Tiles/glace1.png')
glace2 = pygame.image.load('Tiles/glace2.png')
glace3 = pygame.image.load('Tiles/glace3.png')
coffre = pygame.image.load('Tiles/coffre.png')
password1 = pygame.image.load('Tiles/password1.png')
password2 = pygame.image.load('Tiles/password2.png')
password3 = pygame.image.load('Tiles/password3.png')
password4 = pygame.image.load('Tiles/password4.png')
password5 = pygame.image.load('Tiles/password5.png')
autelfin = pygame.image.load('Tiles/autel1.png')
autelsecret = pygame.image.load('Tiles/autel2.png')

global images_animation
images_animation={}

def animation(path,durée_frame):
    global images_animation
    nom_animation = path.split('/')[-1] #on divise le chemin en nom dans une liste et on prend le dernier élément
    données_animation=[]
    n=1
    for frame in durée_frame:
        numero_animation = nom_animation + '_'+str(n)
        emplacement_image= path + '/'+ numero_animation + '.png'#on cherche où se trouve l'image dans les fichiers
        image_perso=pygame.image.load(emplacement_image).convert()
        image_perso.set_colorkey((255,255,255))
        images_animation[numero_animation]=image_perso.copy()
        for i in range(frame):
            données_animation.append(numero_animation) #on ajoute l'aniamtion à la liste de données
        n +=1
    return données_animation

def change_action(variation_action,frame,nouvelle_valeur):
    if variation_action != nouvelle_valeur:
        variation_action = nouvelle_valeur
        frame = 0
    return variation_action,frame

basededonnées_animation = {}
basededonnées_animation['mouvement']=animation('Animations/mouvement',[5,3,5,3,5,3,5,3])
basededonnées_animation['immobile'] = animation('Animations/immobile',[20,20])
basededonnées_animation['air'] = animation('Animations/air',[200])
basededonnées_animation['chutelibre'] = animation('Animations/chutelibre',[200])
#on donne l'emplacement des images elon le mouvement ainsi que le nombre de frames que l'animation dure

#on initialise les variables pour les définitions
action_joueur = 'immobile'
frame_joueur = 0
joueur_retourné = False

def collision_test(rect,tiles):
    collision_liste = []
    for tile in tiles:
        if rect.colliderect(tile):
            collision_liste.append(tile)
    return collision_liste

def bouger(rect,mouvement,tiles): #on définit comment le personnage bouge sans animations pour le moment
    collision_types = {'top':False,'bottom':False,'right':False,'left':False,'c' :False}
    rect.x += mouvement[0]
    collision_liste = collision_test(rect,tiles)
    for tile in collision_liste:
        if mouvement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif mouvement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += mouvement[1]
    collision_liste = collision_test(rect,tiles)
    for tile in collision_liste:
        if mouvement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif mouvement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

pygame.display.set_icon(icone)

while True: #boucle du jeu
    while intro: #menu principal
        musique.stop()
        musiquedebut.play(loops = -1)
        for événement in pygame.event.get():
            if événement.type == QUIT:
                pygame.quit()
                sys.exit()
            if événement.type == KEYDOWN:
                if événement.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if événement.key == K_RETURN:
                    carte = charge_carte('Cartes/map1')
                    musiquedebut.stop()
                    musique.play(loops = -1)
                    joueur_rect = pygame.Rect(250,165,20,27) #point d'apparition + hitbox
                    intro = False
            if événement.type == MOUSEBUTTONDOWN :
                if événement.button == 1:
                    carte = charge_carte('Cartes/map1')
                    musiquedebut.stop()
                    musique.play(loops = -1)
                    joueur_rect = pygame.Rect(250,165,20,27) #point d'apparition + hitbox
                    intro = False

        écran.blit(écrantitre,(0,0))

        pygame.display.update()
    while outro:
        musique.stop()
        musiquefin.play(loops = -1)
        for événement in pygame.event.get():
            if événement.type == QUIT :
                pygame.quit()
                sys.exit()
            if événement.type == KEYDOWN:
                if événement.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if événement.type == MOUSEBUTTONDOWN:
                if événement.button == 1:
                    musiquefin.stop()
                    outro = False
                    intro = True


        écran.blit(écranfin,(0,0))

        pygame.display.update()

    affichage.fill((0,186,255)) #couleur du fond

    caméra[0] += (joueur_rect.x-caméra[0]-100)/20
    caméra[1] += (joueur_rect.y-caméra[1]-150)/20
    caméra_int = caméra.copy()

    tile_rects = []
    y = 0
    for layer in carte:
        x = 0
        for tile in layer: #on associe un caractère alphanumérique à une tile de la carte afin de simplifier la carte
            if tile == '1':
                affichage.blit(sable1,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == '2':
                affichage.blit(sable2,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == '3':
                affichage.blit(sable3,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == '4':
                affichage.blit(roche1,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == '5':
                affichage.blit(roche2,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == '6':
                affichage.blit(roche3,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == '7':
                affichage.blit(glace1,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == 'j':
                affichage.blit(glace1,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == '8':
                affichage.blit(glace2,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == '9':
                affichage.blit(glace3,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == 'i':
                affichage.blit(glace3,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile != '0' and tile != 'p' and tile != 'q' and tile != 'r' and tile != 's'and tile != 't' and tile != 'i' and tile != 'j':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            if tile == 'c':
                affichage.blit(coffre,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == 'p':
                affichage.blit(password1,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == 'q':
                affichage.blit(password2,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == 'r':
                affichage.blit(password3,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == 's':
                affichage.blit(password4,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == 't':
                affichage.blit(password5,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == 'y':
                affichage.blit(autelsecret,(x*16-caméra_int[0],y*16-caméra_int[1]))
            if tile == 'z':
                affichage.blit(autelfin,(x*16-caméra_int[0],y*16-caméra_int[1]))
            x += 1
        y += 1

    mouvement_joueur = [0,0] #initialisation du mouvement du joueur
    if a_droite == True:
        mouvement_joueur[0] += 2
    if a_gauche == True:
        mouvement_joueur[0] -= 2
    mouvement_joueur[1] += vitesse_y
    vitesse_y += 0.2
    if vitesse_y > 3.5: #gravité
        vitesse_y = 3.5

    if vitesse_y<1.3:#si le joueur n'est pas en l'air, on lui donne une animation "normale"
        if mouvement_joueur[0] == 0: #si le joueur n'a pas de mouvement on lui donne l'animation immobile
            action_joueur,frame_joueur = change_action(action_joueur,frame_joueur,'immobile')
        if mouvement_joueur[0] > 0:#si le joueur est en mouvement on lui donne l'animation de courir
               joueur_retourné = False
               action_joueur,frame_joueur = change_action(action_joueur,frame_joueur,'mouvement')
        if mouvement_joueur[0] < 0:#si le joueur vva à gauche on retourne le sprite
            joueur_retourné = True
            action_joueur,frame_joueur = change_action(action_joueur,frame_joueur,'mouvement')
    else:#si le joueur est en l'air, on modifie son animation
        if mouvement_joueur[0] == 0:#immobile, il tombe droit
            action_joueur,frame_joueur = change_action(action_joueur,frame_joueur,'chutelibre')
        if mouvement_joueur[0] > 0:#en mouvement, vers la droite
               joueur_retourné = False
               action_joueur,frame_joueur = change_action(action_joueur,frame_joueur,'air')
        if mouvement_joueur[0] < 0:#en mouvement, vers la gauche en retournant son sprite
            joueur_retourné = True
            action_joueur,frame_joueur = change_action(action_joueur,frame_joueur,'air')


    joueur_rect,collisions = bouger(joueur_rect,mouvement_joueur,tile_rects) #définition des collisions avec le joueur

    if collisions['bottom'] == True: #perte d'élan si le personnage touche le sol
        tair = 0
        vitesse_y = 0
    else:
        tair += 1

    if collisions['top'] == True: #perte d'élan si le personnage se cogne la tête au plafond
        tair = 0
        vitesse_y = 0

    frame_joueur += 1
    if frame_joueur >= len(basededonnées_animation[action_joueur]):
        frame_joueur= 0
    numero_joueur = basededonnées_animation[action_joueur][frame_joueur]
    image_joueur=images_animation[numero_joueur]
    affichage.blit(pygame.transform.flip(image_joueur, joueur_retourné, False),(joueur_rect.x-caméra_int[0],joueur_rect.y-caméra_int[1])) #afficher le personnage en fonction de la caméra

    for événement in pygame.event.get(): #boucle d'événement
        if événement.type == QUIT :
            pygame.quit()
            sys.exit()
        if événement.type == KEYDOWN: #si le bouton est appuyé alors les actions attribuées à ce bouton s'enclencheront
            if événement.key == K_RIGHT  or événement.key == K_d :
                a_droite = True
            if événement.key == K_LEFT or événement.key == K_q :
                a_gauche = True
            if événement.key == événement.key == K_UP  or événement.key == K_z :
                if tair < 6:
                    vitesse_y = -4.5 #vitesse de saut
            if événement.key == K_ESCAPE :
                intro = True

            if collisions['left'] == True: #saut contre le mur de de gauche
                if événement.key == K_z or événement.key == K_UP :
                    if vitesse_y > 2:
                        vitesse_y = -3.65

            if collisions['right'] == True: #saut contre le mur de droite
                if événement.key == K_z or événement.key == K_UP :
                    if vitesse_y > 2:
                        vitesse_y = -3.65

            if événement.key == K_KP6 or événement.key == K_6:
                carte = charge_carte('Cartes/map2')
                joueur_rect = pygame.Rect(207,340,20,27)
            if événement.key == K_KP9 or événement.key == K_9:
                carte = charge_carte('Cartes/map3')
                joueur_rect = pygame.Rect(250,420,20,27)
            if événement.key == K_DOLLAR :
                carte = charge_carte('Cartes/mapsecrete')
                joueur_rect = pygame.Rect(100,120,20,27)
            if événement.key == K_KP7 or événement.key == K_7:
                carte = charge_carte('Cartes/map3')
                joueur_rect = pygame.Rect(1568,220,20,27)
            if événement.key == K_F9 :
                outro = True

        if événement.type == KEYUP: #si le bouton est relâché alors les actions attribuées à ce bouton s'enclencheront
            if événement.key == K_RIGHT or événement.key == K_d :
                a_droite = False
            if événement.key == K_LEFT or événement.key == K_q:
                a_gauche = False

    écran.blit(pygame.transform.scale(affichage,format),(0,0))
    pygame.display.update()
    clock.tick(60) #vitesse du jeu





