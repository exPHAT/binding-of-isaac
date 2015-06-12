from pygame import *
from time import time as cTime
from func import *

class Banner:
    def __init__(self, text, textures):
        self.text = text

        self.hit = [False, False]
        self.snap = loadCFont("banner.png", 12, 10, 26)
        self.streak = textures["streak"]

        self.start = cTime()

        self.drawText = write(text, self.snap, alph="abcdefghijklmnopqrstuvwxyz ")
    def draw(self, surface, direction, text):
        if direction == "in":
            self.slide = surface.copy()
            self.hit[0] = True
            for i in range(0,780,16):
                surface.blit(self.slide,(0,0))
                surface.blit(self.streak,(0-700+i,100))
                surface.blit(self.drawText,(0-400 + i,150))
                display.flip()
        elif direction == "still":
            surface.blit(self.streak,(80,100))
            surface.blit(self.drawText,(380,150))
            display.flip()

        elif direction == "out":
            self.hit[1] = True
            for i in range(0,1560,16):
                surface.blit(self.slide,(0,0))
                surface.blit(self.streak,(80+i,100))
                surface.blit(self.drawText,(380 + i,150))
                display.flip()
            self.hit[0] = False
            self.hit[1] = False

        return self.finish

    def render(self, surface):
        self.finish = cTime()
        if (self.finish - self.start) < 0.9 and (self.finish - self.start) > 0 and not self.hit[0]:
            self.draw(surface, "in", self.drawText)
        elif (self.finish - self.start) < 1.50 and (self.finish - self.start) > 0.00:
            self.draw(surface, "still", self.drawText)
        elif (self.finish-self.start) < 2.1 and not self.hit[1]:
            self.draw(surface, "out", self.drawText)
        elif (self.finish-self.start) >= 2.1:
            return True

        return False
