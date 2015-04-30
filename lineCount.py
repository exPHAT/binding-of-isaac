from glob import glob

names = glob("*.py")

count = 0

for n in names:
	f = open(n)

	count += int(f.read().count("\n"))

	f.close()

print(count)