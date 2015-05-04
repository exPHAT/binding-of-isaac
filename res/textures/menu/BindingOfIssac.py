from pygame import *
from math import *
from random import *
import os

icon = image.load("icon.png")
iconsize = transform.scale(icon,(25,25))
display.set_icon(iconsize)

os.environ['SDL_VIDEO_WINDOW_POS'] = '170,140'

display.set_caption("The Binding of Issac")
screen = display.set_mode((960,540),HWSURFACE)
mouse.set_cursor(*cursors.tri_left)

running = True 
arrowpoint = 0
rotate = 50
spotlight = 0
total = 80
arrowlocation = [(310,147),(315,255),(330,370)]
swap = False
menu = "main"
select = Rect(400,200,200,245)
loadingimage = image.load("loadingimage.jpg")
loadingimage.set_alpha(None)

for x in range(0,50):
    time.wait(60)
    loadingimage.set_alpha(x)
    screen.blit(loadingimage,(0,0))
    display.flip()

menuoverlay = image.load("menuoverlay.png")
menuoverlay2 = image.load("menuoverlay2.png")
mainbackground = image.load("mainbackground.png")
file = image.load("file.png")
issac = image.load("issac.png")
maintitle = image.load("maintitle.png")
arrow = image.load("arrow.png")
selectspotlight = [None,None]
selectspotlight[0] = image.load("fileselect1.png")
selectspotlight[1] = image.load("fileselect2.png")
filespotlight = [None,None]
filespotlight[0] = image.load("filespotlight1.png")
filespotlight[1] = image.load("filespotlight2.png")
spotlightcry = [None,None]
spotlightcry[0] = image.load("spotlightcry1.png")
spotlightcry[1] = image.load("spotlightcry2.png")
controloverlay = image.load("controloverlay.png")
fileunselect = image.load("fileunselect.png")

screen.blit(mainbackground,(0,0))
display.flip()
degrees = -1
increase = -0.05
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
        if e.type == QUIT:
            running = False

        if e.type == KEYDOWN and menu == "selection" and e.key == 273:
            arrowpoint -= 1

        elif e.type == KEYDOWN and menu == "selection" and e.key == 274:
            arrowpoint += 1

        if arrowpoint > 2:
            arrowpoint = 0

        elif arrowpoint < 0:
            arrowpoint = 2

        if menu == "selection" and e.type == KEYDOWN and e.key == 27:     
            menu = "file"
            for x in range(0,960,70):
                screen.blit(mainbackground,(-960+x,-540))
                screen.blit(slide,(0+x,0))
                screen.blit(menuoverlay2,(0,0))
                display.flip()
            continue

        elif menu == "main" and e.type == KEYDOWN and e.key == 32:
            menu = "file"
            for x in range(0,540,40):
                screen.blit(mainbackground,(0,0-x))
                screen.blit(slide,(0,0-x))
                screen.blit(menuoverlay,(0,0))
                screen.blit(controloverlay,(0,540-x))
                display.flip()
            continue

        elif  menu == "file" and e.type == KEYDOWN and e.key == 27:          
            menu = "main"
            for x in range(0,540,40):
                screen.blit(mainbackground,(0,-540+x))
                screen.blit(slide,(0,0+x))
                screen.blit(menuoverlay,(0,0))
                screen.blit(controloverlay,(0,0+x))
                display.flip()
            continue

        elif menu == "file" and e.type == KEYDOWN and e.key == 32:
            menu = "selection"
            for x in range(0,960,70):
                screen.blit(mainbackground,(0-x,-540))
                screen.blit(slide,(0-x,0))
                screen.blit(file,(320-x,total))
                screen.blit(selectspotlight[spotlight],(320-x,total))
                screen.blit(menuoverlay2,(0,0))
                display.flip()
            continue

    if menu == "main":
        if degrees < -2:
            increase *= -1
        elif degrees > 2:
            increase *= -1            
        screen.blit(mainbackground,(0,0))
        screen.blit(spotlightcry[spotlight],(270,140))
        rottitle = transform.rotate(maintitle, degrees)
        screen.blit(rottitle,(90,50))
        degrees += increase
        slide = screen.copy()
        screen.blit(menuoverlay,(0,0))
        
    elif menu == "file":
        screen.blit(mainbackground,(0,-540)) 
        if select.collidepoint(mx,my):
            if total == 15:
                total = 20
            total -= 5
            screen.blit(file,(320,total))
            screen.blit(file,(320,total))
            screen.blit(selectspotlight[spotlight],(320,total))
            slide = screen.copy()
            screen.blit(menuoverlay2,(0,0))
        else:
            if total == 80:
                total = 75
            total += 5
            screen.blit(fileunselect,(320,total))
            screen.blit(filespotlight[spotlight],(320,total))
            slide = screen.copy()
            screen.blit(menuoverlay2,(0,0))
        
    elif menu == "selection":
        screen.blit(mainbackground,(-960,-540))
        screen.blit(arrow,arrowlocation[arrowpoint])
        slide = screen.copy()
        screen.blit(menuoverlay2,(0,0))
        
        
    clock.tick(200)
    print(clock.get_fps())
           
    display.flip()

        

        
quit()
