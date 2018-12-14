
import sys
import csv

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) != 2:
		print("Wrong number of arguments. Expected: 2")

	spookyfilepath = args[0]
	englishfilepath = args[1]

	with open(spookyfilepath) as spookyfile, open(englishfilepath) as englishfile, open("pairs.out", 'w+') as outfile:
		spookyreader = csv.reader(spookyfile, delimiter = ',', quotechar = '\"')
		englishreader = csv.reader(englishfile, delimiter =',', quotechar = '\"')
		for spookyrow in spookyreader:
			englishrow = next(englishreader) 
			outfile.write("{}\t{}\n".format(spookyrow[1], englishrow[1]))
