from os import rename
from glob import glob

things = glob("*.png")
for i in range(len(things)):
	rename(things[i], "%i.png"%(i+1))