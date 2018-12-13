import csv
import sys
from copy import deepcopy

text = list()
for text in sys.stdin:
	text = text.strip()
	words = dict()

	args = sys.argv[1:]
	if len(args) != 1:
		print('wrong arguments!')
		exit(1)
	author = args[0]
	if not (author == 'EAP' or author == 'MWS' or author == 'HPL'):
		print('{} is not an author'.format(author))


	authors = dict()
	authors['EAP'] = list()
	authors['MWS'] = list()
	authors['HPL'] = list()


	for word in text.split(' '):
		if word in words:
			words[word] += 1
		else:
			words[word] = 1
	with open('train.csv', 'r') as csvfile:
		reader = csv.reader(csvfile)
		for line in reader:
			if line[0] == 'id':
				continue
			authors[line[2]].append(line[1])

	maxmatches = 0
	bestline = ''
	for line in authors[author]:

		tempwords = deepcopy(words)
		matches = 0
		for word in line.strip().split(' '):
			if word in tempwords and tempwords[word] > 0: 
				matches += 1
				tempwords[word] -= 1
		matches = float(matches) / len(line.strip().split(' '))
		if matches > maxmatches:
			maxmatches = matches
			bestline = line

	print('')
	print('count: {}'.format(maxmatches))
	print(bestline)

