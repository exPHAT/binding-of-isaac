# PHD.py
# Aaron Taylor
# Moose Abumeeiz
#
# The PHD ensures you have only positive pills
# when its in the players inventory
# 

from pygame import *
from const import *
from Item import *

class PHD(Item):

	collideable = False
	pickedUp = False
	
	tWidth = 64
	tHeight = 64
