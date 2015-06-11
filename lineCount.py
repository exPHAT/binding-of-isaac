from glob import glob

names = glob("*.py")
names.remove("lineCount.py")

count = 0
comments = 0
total = 0

for n in names:
	f = open(n)

	content = f.read()

	count += int(content.count("\n"))
	comments += int(content.count("#"))
	total += len(content)

	f.close()

print("Line count:",count)
print("Without comments:",count-comments)
print("Characters:", total)