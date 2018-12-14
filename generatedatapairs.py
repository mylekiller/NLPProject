
import sys
import csv
import string

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) != 2:
		print("Wrong number of arguments. Expected: 2")
		exit(1)

	spookyfilepath = args[0]
	englishfilepath = args[1]

	with open(spookyfilepath) as spookyfile, open(englishfilepath) as englishfile, open("pairs.out", 'w+') as outfile:
		spookyreader = csv.reader(spookyfile, delimiter = ',', quotechar = '\"')
		englishreader = csv.reader(englishfile, delimiter =',', quotechar = '\"')
		for spookyrow in spookyreader:
			englishrow = next(englishreader) 
			englishresult = ""
			spookyresult = ""

			for spookyword in spookyrow[1].split():
				if spookyword[-1] in string.punctuation:
					spookyresult += spookyword[:-1] + " " + spookyword[-1] + " "
				else:
					spookyresult += spookyword + " "


			for englishword in englishrow[1].split():
				if englishword[-1] in string.punctuation:
					englishresult += englishword[:-1] + " " + englishword[-1] + " "
				else:
					englishresult += englishword + " "
			outfile.write("{}\t{}\n".format(spookyresult.lower(), englishresult.lower()))
