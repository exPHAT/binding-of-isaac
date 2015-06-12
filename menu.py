# menu.py
# Aaron Taylor
# Moose Abumeeiz
#
# The main menu for the game, it is reposnible for changing
# key bindings, character selection, and seed.
# 

from pygame import *
from math import *
from random import *
from func import *

def menu(screen, jController, sounds, nextSong, changeSong):

	#Establishes all the variables and lists used in the menu
	optionpoint = 0
	edit = False
	moves = ["Move Left","Move Right","Move Up","Move Down","Shoot Left","Shoot Right","Shoot Up","Shoot Down","Take pill","Drop Bomb"]
	seed = [" "," "," "," "," "," "," "," "]
	controldisplay = ["A","D","W","S","Left Arrow","Right Arrow","Up Arrow","Down Arrow","Q","E"]
	defaultdisplay = controldisplay[:]
	controls = [97,100,119,115,276,275,273,274,113,101]
	defaultcontrols = controls[:]
	running = True
	arrowpoint = 0
	rotate = 50
	spotlight = 0
	total1 = 50
	total2 = 50
	total3 = 50
	space = 1
	char = 1
	arrowselectionlocation = [(335,120),(350,245),(350,380)]
	swap = False
	menu = "main"
	filepoint = 0

	#Loads in all the textures, scaling correctly

	menuoverlay = loadTexture("menuoverlay.png", dir="menu", double=False)
	menuoverlay2 = loadTexture("menuoverlay2.png", dir="menu", double=False)
	mainbackground = loadTexture("mainbackground.png", dir="menu").convert()
	delete = loadTexture("delete.png", dir="menu")
	unselectdelete = darken(delete,0.5)
	file = [None,None,None]
	unselectfile = [None,None,None]
	characterstats = [None,None,None]
	character = [None,None,None]
	names = [None,None,None]
	digits = loadCFont("main.png", 20, 16, 36, size=.8)
	digitstwo = loadCFont("main.png", 20, 16, 36, size=2)
	names[0] = loadTexture("laname.png", dir="menu")
	names[1] = loadTexture("isname.png", dir="menu")
	names[2] = loadTexture("evname.png", dir="menu")
	characterstats[2] = loadTexture("statev.png", dir="menu")
	characterstats[1] = loadTexture("statis.png", dir="menu")
	characterstats[0] = loadTexture("statla.png", dir="menu")
	character[0] = loadTexture("lazarus.png", dir="menu")
	character[1] = loadTexture("issac.png", dir="menu")
	character[2] = loadTexture("eve.png", dir="menu")
	file[0] = loadTexture("file1.png", dir="menu")
	unselectfile[0] = darken(file[0],0.5)
	file[1] = loadTexture("file2.png", dir="menu")
	unselectfile[1] = darken(file[1],0.5)
	file[2] = loadTexture("file3.png", dir="menu")
	unselectfile[2] = darken(file[2],0.5)
	maintitle = loadTexture("maintitle.png", dir="menu")
	arrow = loadTexture("arrow.png", dir="menu")
	optionarrow = loadTexture("arrow.png", dir="menu", double=False)
	filespotlight = [None,None]
	filespotlight[0] = loadTexture("filespotlight1.png", dir="menu")
	filespotlight[1] = loadTexture("filespotlight2.png", dir="menu")
	spotlightcry = [None,None]
	spotlightcry[0] = loadTexture("spotlightcry1.png", dir="menu")
	spotlightcry[1] = loadTexture("spotlightcry2.png", dir="menu")
	controloverlay = loadTexture("controloverlay.png", dir="menu")
	screen.blit(mainbackground,(0,0))
	display.flip()
	degrees = 0
	increase = -0.022
	frame2 = 0
	seedletter = 0

	clock = time.Clock()

	while running:
		frame = time.get_ticks()
		mb = mouse.get_pressed()
		kd = key.get_pressed()
		mx,my = mouse.get_pos()

		#Keeps track of the frames for the animations


		if (frame - frame2) > 120:           
			spotlight += 1
			frame2 = frame
			if spotlight > 1:
				spotlight = 0
		for e in event.get():
			if e.type == QUIT:
				running = False

			#All the various button clicks are managed here

			if e.type == KEYDOWN and menu == "main" and e.key == 27:
				quit()

			if e.type == KEYDOWN and menu == "selection" and e.key == 273:
				arrowpoint -= 1
			elif e.type == KEYDOWN and menu == "selection" and e.key == 274:
				arrowpoint += 1

			if arrowpoint > 2:
				arrowpoint = 0
			elif arrowpoint < 0:
				arrowpoint = 2

			if e.type == KEYDOWN and menu == "file" and e.key == 276:
				filepoint -= 1
			elif e.type == KEYDOWN and menu == "file" and e.key == 275:
				filepoint += 1
			if e.type == KEYDOWN and e.key == 32 and menu == "options":
				if edit == False:
					edit = True
				elif edit == True:
					edit = False
			if e.type == KEYDOWN and menu == "options" and e.key == 32 and optionpoint == 10:
				controldisplay = defaultdisplay[:]

				controls = defaultcontrols[:]

			#Sets the key clicked to the letter
			if e.type == KEYDOWN and menu == "seed" and e.key != 8 and e.key != 27:
				if seedletter < 8:
					if e.unicode.lower() in alph:
						seed[seedletter]= e.unicode.lower()
						seedletter += 1
			if e.type == KEYDOWN and menu == "seed" and e.key == 8:
				if seedletter > 0:
					seedletter -= 1
					seed[seedletter] = " "

			#Allows for different keys to be linked to the various controls
			if e.type == KEYDOWN and edit == True and menu == "options" and e.key != 32 and optionpoint != 10:
				if e.key == 273:
					controldisplay[optionpoint] = "Up Arrow"
					controls[optionpoint] = e.key
				elif e.key == 274:
					controldisplay[optionpoint] = "Down Arrow"
					controls[optionpoint] = e.key
				elif e.key == 275:
					controldisplay[optionpoint] = "Right Arrow"
					controls[optionpoint] = e.key
				elif e.key == 276:
					controldisplay[optionpoint] = "Left Arrow"
					controls[optionpoint] = e.key
				elif e.key == 9:
					controldisplay[optionpoint] = "Tab"
					controls[optionpoint] = e.key
				elif e.key == 304:
					controldisplay[optionpoint] = "Shift"
					controls[optionpoint] = e.key
				elif e.key == 306:
					controldisplay[optionpoint] = "Control"
					controls[optionpoint] = e.key
				elif e.key == 308:
					controldisplay[optionpoint] = "Alt"
					controls[optionpoint] = e.key
				elif e.unicode in alph:
					controldisplay[optionpoint] = e.unicode.upper()
					controls[optionpoint] = e.key
				edit = False
			elif e.type == KEYDOWN and edit == False and menu == "options":
				if e.key == 273:
					optionpoint -= 1
				elif e.key == 274:
					optionpoint += 1
				if optionpoint > 10:
					optionpoint = 0
				elif optionpoint < 0:
					optionpoint = 10
			if e.type == KEYDOWN and menu == "character" and e.key == 276:
				sounds["selectLeft"].stop()
				sounds["selectLeft"].play()
				if char == 1:

			#Controls the rotation of the characters 
					for x in range(0,100,5):
						screen.blit(mainbackground,(-960,0))
						screen.blit(character[1],(430-x,230-x))
						screen.blit(character[2],(330+(x*2),130))
						screen.blit(character[0],(530-x,130+x))
						screen.blit(menuoverlay2,(0,0))
						display.flip()
				elif char == 2:
					for x in range(0,100,5):
						screen.blit(mainbackground,(-960,0))
						screen.blit(character[2],(430-x,230-x))
						screen.blit(character[0],(330+(x*2),130))
						screen.blit(character[1],(530-x,130+x))
						screen.blit(menuoverlay2,(0,0))
						display.flip()
				elif char == 0:
					for x in range(0,100,5):
						screen.blit(mainbackground,(-960,0))
						screen.blit(character[0],(430-x,230-x))
						screen.blit(character[1],(330+(x*2),130))
						screen.blit(character[2],(530-x,130+x))
						screen.blit(menuoverlay2,(0,0))
						display.flip()
				char -= 1
			elif e.type == KEYDOWN and menu == "character" and e.key == 275:
				sounds["selectRight"].stop()
				sounds["selectRight"].play()
				if char == 1:
					for x in range(0,100,5):
						screen.blit(mainbackground,(-960,0))
						screen.blit(character[1],(430+x,230-x))
						screen.blit(character[2],(330+x,130+x))
						screen.blit(character[0],(530-(x*2),130))
						screen.blit(menuoverlay2,(0,0))
						display.flip()
				elif char == 2:
					for x in range(0,100,5):
						screen.blit(mainbackground,(-960,0))
						screen.blit(character[2],(430+x,230-x))
						screen.blit(character[0],(330+x,130+x))
						screen.blit(character[1],(530-(x*2),130))
						screen.blit(menuoverlay2,(0,0))
						display.flip()
				elif char == 0:
					for x in range(0,100,5):
						screen.blit(mainbackground,(-960,0))
						screen.blit(character[0],(430+x,230-x))
						screen.blit(character[1],(330+x,130+x))
						screen.blit(character[2],(530-(x*2),130))
						screen.blit(menuoverlay2,(0,0))
						display.flip()
				char += 1

			#Controls the adjustment of the seed
			elif e.type == KEYDOWN and menu == "character" and e.key == 32:
				seed = "".join(seed)
				if seed == " "*8:
					seed = generateSeed()
				createSave(filepoint, char, seed)
				return char, controls, seed

			if e.type == KEYDOWN and menu == "file" and e.key == 273:
				space -= 1
			elif e.type == KEYDOWN and menu == "file" and e.key == 274:
				space += 1

			if e.type == KEYDOWN and menu == "file" and e.key == 32 and space == 0:
				deleteSave(filepoint)
			#Ensures selections loop in a circle

			if space > 1:
				space = 0
			elif space < 0:
				space = 1


			if filepoint > 2:
				filepoint = 0
			elif filepoint < 0:
				filepoint = 2

			if char > 2:
				char = 0
			elif char < 0:
				char = 2

			#Controls all the menu slides
			if menu == "selection" and e.type == KEYDOWN and e.key == 27:     
				menu = "file"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,960,70):
					screen.blit(mainbackground,(-960+x,-540))
					screen.blit(unselectfile[0],(-980+x,total1))
					screen.blit(filespotlight[0],(-915+x,total1))
					screen.blit(unselectfile[1],(-380+x,total2))
					screen.blit(filespotlight[0],(-325+x,total2))
					screen.blit(unselectfile[2],(-680+x,total3))
					screen.blit(filespotlight[0],(-635+x,total3))
					screen.blit(unselectdelete,(-780+x,380))             
					screen.blit(slide,(0+x,0))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue


			if menu == "seed" and e.type == KEYDOWN and e.key == 27:     
				menu = "character"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,960,70):
					screen.blit(mainbackground,(-1920+x,0))
					screen.blit(names[char],(-570+x,300))
					screen.blit(characterstats[char],(-670+x,390))
					screen.blit(character[char],(-530+x,230))
					screen.blit(character[char-1],(-630+x,130))
					screen.blit(character[char+1],(-430+x,130))
					screen.blit(slide,(0+x,0))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

			if menu == "character" and e.type == KEYDOWN and e.key == 27:     
				menu = "selection"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,540,40):
					screen.blit(mainbackground,(-960,0-x))
					screen.blit(slide,(0,0-x))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

			if menu == "character" and e.type == KEYDOWN and e.key == 9:     
				menu = "seed"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,960,70):
					screen.blit(mainbackground,(-960-x,0))
					screen.blit(slide,(0-x,0))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

			elif menu == "main" and e.type == KEYDOWN and e.key == 32:
				menu = "file"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,540,40):
					screen.blit(mainbackground,(0,0-x))
					screen.blit(unselectfile[0],(-20,total1+540-x))
					screen.blit(filespotlight[0],(45,total1+540-x))
					screen.blit(unselectfile[1],(280,total2+540-x))
					screen.blit(filespotlight[0],(325,total2+540-x))
					screen.blit(unselectfile[2],(580,total3+540-x))
					screen.blit(filespotlight[0],(635,total3+540-x))
					screen.blit(unselectdelete,(180+x,380+540-x))   
					screen.blit(slide,(0,0-x))
					screen.blit(menuoverlay,(0,0))
					screen.blit(controloverlay,(0,540-x))
					display.flip()
				continue

			elif  menu == "file" and e.type == KEYDOWN and e.key == 27:          
				menu = "main"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,540,40):
					screen.blit(mainbackground,(0,-540+x))
					screen.blit(spotlightcry[spotlight],(260,-440+x))
					screen.blit(rottitle, (475-rottitle.get_width()//2,-405-rottitle.get_height()//2+x))
					screen.blit(slide,(0,0+x))
					screen.blit(menuoverlay,(0,0))
					screen.blit(controloverlay,(0,0+x))
					display.flip()
				continue

			elif menu == "file" and e.type == KEYDOWN and e.key == 32 and space == 1:
				menu = "selection"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,960,70):
					screen.blit(mainbackground,(0-x,-540))
					screen.blit(slide,(0-x,0))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

			elif menu == "selection" and e.type == KEYDOWN and e.key == 32 and arrowpoint == 0:
				menu = "character"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				char = 1
				for x in range(0,540,40):
					screen.blit(mainbackground,(-960,-540+x))
					screen.blit(names[char],(382,-240+x))
					screen.blit(characterstats[char],(290,-150+x))
					screen.blit(character[char],(430,-310+x))
					screen.blit(character[char-1],(530,-410+x))
					screen.blit(character[char+1],(330,-410+x))
					screen.blit(slide,(0,0+x))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue
			elif menu == "selection" and e.type == KEYDOWN and e.key == 32 and arrowpoint == 1:
				# Continue
				try:
					sv = readSave(filepoint)
					return sv[0],controls,sv[1]
				except:
					sounds["error"].stop()
					sounds["error"].play()

			elif menu == "selection" and e.type == KEYDOWN and e.key == 32 and arrowpoint == 2:
				menu = "options"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,960,70):
					screen.blit(mainbackground,(-960-x,-540))
					screen.blit(slide,(0-x,0))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

			elif menu == "options" and e.type == KEYDOWN and e.key == 27 and arrowpoint == 2:
				menu = "selection"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,960,70):
					screen.blit(mainbackground,(-1920+x,-540))
					screen.blit(slide,(0+x,0))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

		if menu == "main":

			#Adjusts the rotation of the main title
			if degrees < -1:
				increase *= -1
			elif degrees > 0:
				increase *= -1            
			screen.blit(mainbackground,(0,0))
			screen.blit(spotlightcry[spotlight],(260,100))
			rottitle = transform.rotate(maintitle,degrees)
			screen.blit(rottitle, (475-rottitle.get_width()//2,145-rottitle.get_height()//2))
			degrees += increase
			slide = screen.copy()
			screen.blit(menuoverlay,(0,0))
			
		elif menu == "file":
			screen.blit(mainbackground,(0,-540)) 
			
			#controls the raise of the file menus and their deletion selection
			if filepoint == 0:
				total1 -= 5
				screen.blit(file[0],(-20,total1))
				screen.blit(filespotlight[spotlight],(45,total1))
				if total1 == 15:
					total1 = 20
			else:
				total1 += 5
				screen.blit(unselectfile[0],(-20,total1))
				screen.blit(filespotlight[0],(45,total1))
				if total1 == 55:
					total1 = 50

			if filepoint == 1:
				total2 -= 5
				screen.blit(file[1],(280,total2))
				screen.blit(filespotlight[spotlight],(325,total2))
				if total2 == 15:
					total2 = 20
			else:
				total2 += 5
				screen.blit(unselectfile[1],(280,total2))
				screen.blit(filespotlight[0],(325,total2))
				if total2 == 55:
					total2 = 50

			if filepoint == 2:
				total3 -= 5
				screen.blit(file[2],(580,total3))
				screen.blit(filespotlight[spotlight],(635,total3))
				if total3 == 15:
					total3 = 20
			else:
				total3 += 5
				screen.blit(unselectfile[2],(580,total3))
				screen.blit(filespotlight[0],(635,total3))
				if total3 == 55:
					total3 = 50

			if space == 0:
				screen.blit(delete,(180,380))
			elif space == 1:
				screen.blit(unselectdelete,(180,380))

			slide = screen.copy()
			screen.blit(menuoverlay2,(0,0))
			
		elif menu == "selection":
			screen.blit(mainbackground,(-960,-540))
			screen.blit(arrow,arrowselectionlocation[arrowpoint])
			slide = screen.copy()
			screen.blit(menuoverlay2,(0,0))

		#Adjusts the display of the characters and their respective statistics
		elif menu == "character":
			screen.blit(mainbackground,(-960,0))
			if char == 1:
				screen.blit(names[1],(382,300))
				screen.blit(characterstats[1],(290,390))
				screen.blit(character[1],(430,230))
				screen.blit(character[2],(330,130))
				screen.blit(character[0],(530,130))
				
			elif char == 0:
				screen.blit(names[0],(382,300))
				screen.blit(characterstats[0],(290,390))
				screen.blit(character[0],(430,230))
				screen.blit(character[1],(330,130))
				screen.blit(character[2],(530,130))

			elif char == 2:
				screen.blit(names[2],(390,300))
				screen.blit(characterstats[2],(290,390))
				screen.blit(character[2],(430,230))
				screen.blit(character[1],(530,130))
				screen.blit(character[0],(330,130))
			slide = screen.copy()
			screen.blit(menuoverlay2,(0,0))

		#Renders the text on the seed menu
		elif menu == "seed":
			screen.blit(mainbackground,(-1920,0))
			screen.blit(write(seed[0:4],digitstwo),((370,50)))
			screen.blit(write(seed[4:],digitstwo),((370,85)))
			slide = screen.copy()
			screen.blit(menuoverlay2,(0,0))

		#Renders the correct text on the options
		elif menu == "options":
			screen.blit(mainbackground,(-1920,-540))
			for i in range(len(moves)):
				screen.blit(write(moves[i],digits),(175,175+(i*25)))
			for i in range(len(controldisplay)):
				screen.blit(write(controldisplay[i],digits),(675,175+(i*25)))
			if optionpoint != 10:
				screen.blit(optionarrow,(150,optionpoint + (167 + (optionpoint*24))))
			else:
				screen.blit(optionarrow,(300,450))
				
			slide = screen.copy()
			screen.blit(menuoverlay2,(0,0))
			
		clock.tick(200)
			   
		display.flip()
			
	quit()
