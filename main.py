#Import the pygame library and initialise the game engine
import pygame
import random
import csv
import time
# from vaisseau import Vaisseau


pygame.init()
 
# Define some colors
WHITE = (255,255,255)
DARK = (0,0,0)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)
ORANGE = (255,100,0)
YELLOW = (255,255,0)
 
Gauche = False
Droite = False
vaisseau = pygame.image.load('vaisseau.png')
rectangle_vaisseau = pygame.Rect(235,600,31,32)
missiles = []

carre_blanc = pygame.image.load('carre_blanc.png')
carre_orange = pygame.image.load('carre_orange.png')
carre_vert = pygame.image.load('carre_vert.png')
carre_violet = pygame.image.load('carre_violet.png')

bricks_blanc=[]
bricks_orange=[]
bricks_violet=[]
bricks_vert=[]

running_game = True

f = open("donnees.csv","r")
lecteur = csv.DictReader(f,delimiter=",")
for ligne in lecteur:
	cooldown = int(ligne['tir'])   # la variable cooldown permettra de gérer la durée entre 2 tirs
	default_cooldown = cooldown
	vitesse_deplacement = int(ligne['vitesse'])
	credit = int(ligne['credit'])
	vitesse_defilement = float(ligne['defilement'])
	score = int(ligne['score'])
	vitesse_apparition = int(ligne['vitesse_apparition'])
	default_vitesse_apparition = vitesse_apparition
f.close()

tir_pret = True

block_pret = True

# Open a new window
size = (500, 650)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Brick Shooter by ReaGames")
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

def deplace_bricks():
	for brick in bricks_orange:
		brick.bottom=brick.bottom+ vitesse_defilement

	for brick in bricks_blanc:
		brick.bottom=brick.bottom + vitesse_defilement

	for brick in bricks_violet:
		brick.bottom=brick.bottom + vitesse_defilement

	for brick in bricks_vert:
		brick.bottom=brick.bottom + vitesse_defilement


def placer_bricks():
	global block_pret,vitesse_apparition,default_vitesse_apparition
	if block_pret == False:
		vitesse_apparition = vitesse_apparition - 1
		if vitesse_apparition == 0:
			block_pret = True

	if block_pret == True :
		y = random.randint(50,100)
		m = random.randint(10,400)
		h = 480 - m
		for i in range(m,h,y): # Margin left / Taille screen horizontal / Écart entre les blocks
			x = random.randint(1,100)
			if x < 20 and x >= 10:
				bricks_orange.append(pygame.Rect(i,random.randint(35,50),40,40))
			if x > 50:
				bricks_blanc.append(pygame.Rect(i,random.randint(35,50),40,40))
			if x < 5:
				bricks_violet.append(pygame.Rect(i,random.randint(35,50),40,40))
			if x < 10 and x >= 5:
				bricks_vert.append(pygame.Rect(i,random.randint(35,50),40,40))
			block_pret = False
			vitesse_apparition = default_vitesse_apparition

	for brick in bricks_orange:
		screen.blit(carre_orange,brick)
	
	for brick in bricks_blanc:
		screen.blit(carre_blanc,brick)
	
	for brick in bricks_violet:
		screen.blit(carre_violet,brick)
	
	for brick in bricks_vert:
		screen.blit(carre_vert,brick)

def detecte_collision():
	global vitesse_defilement, vitesse_deplacement, default_cooldown,credit,score,default_vitesse_apparition
	for missile in missiles:
		# Augmentation de la vitesse de defilement
		for brick in bricks_orange:
			if missile.colliderect(brick):
				bricks_orange.remove(brick)
				missiles.remove(missile)
				if default_vitesse_apparition > 50:
					vitesse_defilement += 0.2
					default_vitesse_apparition -= 5
				credit += 10
				score += 10

		# Diminution de la vitesse de deplacement
		for brick in bricks_vert:
			if missile.colliderect(brick):
				bricks_vert.remove(brick)
				missiles.remove(missile)
				if vitesse_deplacement > 1 :
					vitesse_deplacement -= 1
				credit += 10
				score += 10

		# Diminution de la vitesse de tir
		for brick in bricks_violet:
			if missile.colliderect(brick):
				bricks_violet.remove(brick)
				missiles.remove(missile)
				default_cooldown -= 1
				credit += 10
				score += 10

		# Brick neutre
		for brick in bricks_blanc:
			if missile.colliderect(brick):
				bricks_blanc.remove(brick)
				missiles.remove(missile)
				credit += 10
				score += 10

def detecte_end_game():
	for brick in bricks_orange:
		if rectangle_vaisseau.colliderect(brick):
			bricks_orange.remove(brick)
			game_over()
	for brick in bricks_blanc:
		if rectangle_vaisseau.colliderect(brick):
			bricks_blanc.remove(brick)
			game_over()

	for brick in bricks_violet:
		if rectangle_vaisseau.colliderect(brick):
			bricks_violet.remove(brick)
			game_over()

	for brick in bricks_vert:
		if rectangle_vaisseau.colliderect(brick):
			bricks_vert.remove(brick)
			game_over()



def game_over():
	global vitesse_defilement, vitesse_deplacement, default_cooldown,credit,score,default_vitesse_apparition
	running = True
	while running == True:
		global running_game
		screen.fill(DARK)
		running_game = False
		font = pygame.font.Font(None, 100)
		title = font.render("GAME OVER", 1, WHITE)
		screen.blit(title, (45,220))
		font = pygame.font.Font(None, 30)
		text = font.render("Score: " + str(score), 1, WHITE)
		screen.blit(text, (190,360))

		font = pygame.font.Font(None, 30)
		text = font.render("ESC : Retourner au menu", 1, WHITE)
		screen.blit(text, (130,500))
		pygame.display.flip()

		for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					screen.fill(DARK)
					vitesse_deplacement = 3
					default_cooldown = 30
					vitesse_defilement = 1
					score = 0
					credit = 0
					default_vitesse_apparition = 100
					close_game()
					running = False
				if event.type == pygame.QUIT:
					close_game()

def close_game():
	
	with open('donnees.csv', 'w', newline='') as csvfile:
		fieldnames = ['credit', 'vitesse','defilement','tir','score','vitesse_apparition']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		writer.writerow({'credit': str(credit), 'vitesse': str(vitesse_deplacement), 'defilement': str(vitesse_defilement), 'tir': str(default_cooldown),'score': str(score), 'vitesse_apparition': str(default_vitesse_apparition)})
	
	pygame.quit()

def menu():
	font = pygame.font.Font(None, 74)
	text = font.render("BrickShooter", 1, WHITE)
	screen.blit(text, (95,50))
	
	font = pygame.font.Font(None, 40)
	text = font.render("A: Lancer la partie", 1, WHITE)
	screen.blit(text, (130,200))
	text = font.render("B : Règles du jeu", 1, WHITE)
	screen.blit(text, (130,250))
	text = font.render("C : Equipement", 1, WHITE)
	screen.blit(text, (130,300))
	text = font.render("D : Quitter", 1, WHITE)
	screen.blit(text, (130,350))

	pygame.display.flip()

	is_pressed = False

	while not is_pressed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				close_game()

			# Nouvelle partie : a
			if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
				screen.fill(DARK)
				new_game()
			
			# Règles du jeu : b
			if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
				screen.fill(DARK)
				rules()

			# Equipement : c
			if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
				screen.fill(DARK)
				equipement()

			# Quitter : d
			if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
				close_game()



def rules():
	running = True
	while running == True:
		font = pygame.font.Font(None, 40)
		title = font.render("Règles du jeu", 1, WHITE)
		screen.blit(title, (150,50))

		font = pygame.font.Font(None, 30)
		text = font.render("Le but du jeu est de détruire tous les blocs", 1, WHITE)
		screen.blit(text, (42,140))
		text = font.render("sans qu'ils ne vous touchent !", 1, WHITE)
		screen.blit(text, (42,160))
		text = font.render("Pour cela il suffit de vous déplacez de", 1, WHITE)
		screen.blit(text, (42,200))
		text = font.render("gauche à droite avec les flèches de votre", 1, WHITE)
		screen.blit(text, (42,220))
		text = font.render("clavier et de tirer avec espace.", 1, WHITE)
		screen.blit(text, (42,240))

		text = font.render("Tirer sur les blocs pour gagner des crédits", 1, WHITE)
		screen.blit(text, (42,280))
		text = font.render("et utilisez-les pour améliorer vos données", 1, WHITE)
		screen.blit(text, (42,300))
		text = font.render("dans Equipement.", 1, WHITE)
		screen.blit(text, (42,320))

		text = font.render("Les blocs :", 1, WHITE)
		screen.blit(text, (190,370))
		text = font.render("Orange : augmente la vitesse de défilement", 1, WHITE)
		screen.blit(text, (42,410))
		text = font.render("Vert : diminue la vitesse de déplacement", 1, WHITE)
		screen.blit(text, (42,440))
		text = font.render("Violet : diminue la vitesse de tir", 1, WHITE)
		screen.blit(text, (42,470))

		font = pygame.font.Font(None, 30)
		text = font.render("ESC : Retourner au menu", 1, WHITE)
		screen.blit(text, (130,550))

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				screen.fill(DARK)
				menu()
				running = False

			if event.type == pygame.QUIT:
				close_game()

def detecte_touches():

	global Gauche,Droite,tir_pret,cooldown,default_cooldown

	if tir_pret == False:
		cooldown = cooldown - 1
		if cooldown == 0:
			tir_pret = True

	for event in pygame.event.get():
		if event.type==pygame.QUIT:		# Traite l'évènement fermer la fenêtre avec la souris
				close_game()
		if event.type== pygame.KEYDOWN:	# Traiter les évènements du clavier
			if event.key==pygame.K_ESCAPE:
				screen.fill(DARK)
				running = False
				menu()
			if event.key==pygame.K_RIGHT:
				Droite = True
			if event.key==pygame.K_LEFT:
				Gauche = True
			if event.key==pygame.K_SPACE and tir_pret == True:
				missiles.append(pygame.Rect(rectangle_vaisseau.left+12,rectangle_vaisseau.top,5,15))
				tir_pret = False
				cooldown = default_cooldown

		if event.type== pygame.KEYUP:
			if event.key==pygame.K_RIGHT:
				Droite = False
			if event.key==pygame.K_LEFT:
				Gauche = False

def deplace_missiles():
	for missile in missiles:				# pour chaque missiles existant
		missile.top=missile.top-10			# soustraire 10 à la coordonnée du point haut
		pygame.draw.rect(screen,WHITE,missile)	# dessinner un rectangle de couleur blanc
		if missile.top<=5:				# si le missiles arrive en haut de l'écran
			missiles.remove(missile)

def new_game():
	global running_game
	screen.fill(DARK)
	font = pygame.font.Font(None, 200)
	text = font.render("3", 1, RED)
	screen.blit(text, (210,150))
	pygame.display.flip()
	time.sleep(1)

	screen.fill(DARK)
	text = font.render("2", 1, RED)
	screen.blit(text, (210,150))
	pygame.display.flip()
	time.sleep(1)

	screen.fill(DARK)
	text = font.render("1", 1, RED)
	screen.blit(text, (210,150))
	pygame.display.flip()
	time.sleep(1)

	while running_game == True:
		placer_bricks()
		screen.blit(vaisseau,rectangle_vaisseau)
		screen.fill(DARK)
		font = pygame.font.Font(None, 30)
		text = font.render("Score: " + str(score), 1, WHITE)
		screen.blit(text, (20,10))
		text = font.render("Crédit: " + str(credit), 1, WHITE)
		screen.blit(text, (370,10))
		pygame.draw.line(screen, WHITE, [0, 32], [800, 32], 2)
		screen.blit(vaisseau,rectangle_vaisseau)	# placer l'image
		detecte_collision()
		deplace_bricks()
		detecte_touches()

		# Déplacement du vaisseau d'un pixel 
		if Gauche and rectangle_vaisseau.left > 5 : rectangle_vaisseau.left -= vitesse_deplacement
		if Droite and rectangle_vaisseau.right < 495 : rectangle_vaisseau.right += vitesse_deplacement
		
		placer_bricks()
		deplace_missiles()
		detecte_end_game()
		pygame.display.update()				# rafraichir l'affichage de la fenêtre jeu  
		clock.tick(30)


def equipement():
	running = True
	while running == True:
		global credit, default_cooldown, vitesse_deplacement, vitesse_defilement, default_vitesse_apparition
		font = pygame.font.Font(None, 40)
		title = font.render("Equipements du vaisseau", 1, WHITE)
		screen.blit(title, (80,50))

		font = pygame.font.Font(None, 30)
		text = font.render("Vous pouvez ici améliorer les capacités de ", 1, WHITE)
		screen.blit(text, (42,150))
		text = font.render("votre vaisseau à l'aide des crédits que vous", 1, WHITE)
		screen.blit(text, (42,170))
		text = font.render("avez optenu lors de vos parties !", 1, WHITE)
		screen.blit(text, (42,190))

		text = font.render("Crédits: " + str(credit), 1, WHITE)
		screen.blit(text, (190,250))

		text = font.render("A : Augmenter la vitesse de tir (120c)", 1, WHITE)
		screen.blit(text, (26,320))
		text = font.render("B : Augmenter la vitesse de déplacement (100c)", 1, WHITE)
		screen.blit(text, (26,350))
		text = font.render("C : Diminuer la vitesse de défilement (100c)", 1, WHITE)
		screen.blit(text, (26,380))

		text = font.render("ESC : Retourner au menu", 1, WHITE)
		screen.blit(text, (130,550))

		pygame.display.flip()

		for event in pygame.event.get():

			# Augmenter la vitesse de tir : a
			if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
				if credit >= 120:
					screen.fill(DARK)
					if default_cooldown >= 4 :
						default_cooldown -= 2
						credit -= 120
					else :
						font = pygame.font.Font(None, 25)
						text = font.render("Vous avez atteint la vitesse de tir max", 1, WHITE)
						screen.blit(text, (80,450))
					
			
			# Augmenter la vitesse de déplacement : b
			if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
				if credit >= 100:
					screen.fill(DARK)
					if vitesse_deplacement < 10 :
						vitesse_deplacement += 1
						credit -= 100
					else :
						font = pygame.font.Font(None, 25)
						text = font.render("Vous avez atteint la vitesse de déplacement max", 1, WHITE)
						screen.blit(text, (48,450))

			# Diminuer la vitesse de défilement : c
			if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
				if credit >= 100:
					screen.fill(DARK)
					if vitesse_defilement > 1 :
						vitesse_defilement -= 1
						default_vitesse_apparition += 25
						credit -= 100
					else :
						font = pygame.font.Font(None, 25)
						text = font.render("Vous avez atteint la vitesse de défilement minimale", 1, WHITE)
						screen.blit(text, (45,450))

			# Retour au menu
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				screen.fill(DARK)
				menu()
				running = False

			if event.type == pygame.QUIT:
				close_game()

def main_game_loop():
	menu()
	
main_game_loop()