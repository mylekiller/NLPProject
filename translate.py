

import os,sys


def parsestep():
	bestrule = None
	for key in rules:
		if key.split()[0] == line.lower().split()[0]:
			if not bestrule or len(key) < len(bestrule):
				bestrule = key.split()[0]
				

if __name__ == "__main__":

	args = sys.argv[1:]

	if len(args) != 1:
		print("Wrong number of arguments. Expected: 1")
		exit(1)


	cleangrammarfile = args[0]

	rules = dict()

	for line in cleangrammarfile:
		rules[line[5:].split('|')[0].strip()] = line[5:].split('|')[1].strip()

	print("Done parsing rules. Here are your translations:")

	for line in sys.stdin:
		
			