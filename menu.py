from pygame import *
from func import *

def menu(screen, jController, sounds, nextSong, changeSong):

	running = True 
	arrowpoint = 0
	rotate = 50
	spotlight = 0
	total1 = 50
	total2 = 50
	total3 = 50
	space = 1
	arrowselectionlocation = [(335,120),(350,245),(350,380)]
	swap = False
	menu = "main"
	filepoint = 0

	menuoverlay = loadTexture("menuoverlay.png", dir="menu", double=False)
	menuoverlay2 = loadTexture("menuoverlay2.png", dir="menu", double=False)
	mainbackground = loadTexture("mainbackground.png", dir="menu").convert()
	delete = loadTexture("delete.png", dir="menu")
	unselectdelete = darken(delete,0.5)
	file = [None,None,None]
	unselectfile = [None,None,None]
	file[0] = loadTexture("file1.png", dir="menu")
	unselectfile[0] = darken(file[0],0.5)
	file[1] = loadTexture("file2.png", dir="menu")
	unselectfile[1] = darken(file[1],0.5)
	file[2] = loadTexture("file3.png", dir="menu")
	unselectfile[2] = darken(file[2],0.5)
	maintitle = loadTexture("maintitle.png", dir="menu")
	arrow = loadTexture("arrow.png", dir="menu")
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
	increase = -0.0
	frame2 = 0

	clock = time.Clock()

	while running:
		frame = time.get_ticks()
		mb = mouse.get_pressed()
		kd = key.get_pressed()
		mx,my = mouse.get_pos()

		if (frame - frame2) > 120:
			spotlight += 1
			frame2 = frame
			if spotlight > 1:
				spotlight = 0
		for e in event.get():
			if e.type == QUIT or (e.type == KEYDOWN and e.key == 27 and menu == "main"):
				running = False
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

			if e.type == KEYDOWN and menu == "file" and e.key == 273:
				space -= 1
			elif e.type == KEYDOWN and menu == "file" and e.key == 274:
				space += 1

			if e.type == KEYDOWN and menu == "file" and e.key == 32 and space == 0:
				print("delete" , filepoint)

			if e.type == KEYDOWN and menu == "selection" and e.key == 32 and arrowpoint == 1:
				running = False

			if space > 1:
				space = 0
			elif space < 0:
				space = 1


			if filepoint > 2:
				filepoint = 0
			elif filepoint < 0:
				filepoint = 2

			if menu == "selection" and e.type == KEYDOWN and e.key == 27:     
				menu = "file"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,960,70):
					screen.blit(mainbackground,(-960+x,-540))
					screen.blit(slide,(0+x,0))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

			elif menu == "main" and e.type == KEYDOWN and e.key == 32:
				menu = "file"
				sounds["pageTurn"].stop()
				sounds["pageTurn"].play()
				for x in range(0,540,40):
					screen.blit(mainbackground,(0,0-x))
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
					screen.blit(unselectfile[0],(-20-x,total1-5))
					screen.blit(unselectfile[1],(280-x,total2-5))
					screen.blit(unselectfile[2],(580-x,total3-5))
					screen.blit(filespotlight[spotlight],(45-x,total1))
					screen.blit(filespotlight[spotlight],(325-x,total2))
					screen.blit(filespotlight[spotlight],(635-x,total3))
					screen.blit(menuoverlay2,(0,0))
					display.flip()
				continue

		if menu == "main":
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


		if nextSong != "" and changeSong != -1:
			if mixer.music.get_pos()/1000 >= changeSong:
				mixer.music.load(nextSong)
				mixer.music.play(-1)
				nextSong = ""
				changeSong = -1
			

		if jController != None:
			jController.update()
			
		clock.tick(60)
		display.flip()

		loaded = True
	return 0, generateSeed()