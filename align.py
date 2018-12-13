import numpy
import sys

params = dict()
ewordtypes = set()
fwordtypes = set()
counts = dict()
outputfile = 'align.out'

def EM(trainfile):
	log_likelihood = 0
	counts = dict()
	#E
	with open(trainfile) as file:
		for line in file:
			e = line.strip().split('\t')[1]
			f = line.strip().split('\t')[0]

			ewords = e.strip().split(' ')
			fwords = f.strip().split(' ')

			log_product = 1
			for j in range(len(fwords)):
				summation = 0
				for i in range(len(ewords) + 1):
					eword = ''
					fword = fwords[j]
					if i == 0:
						eword = 'NULL'
					else:
						eword = ewords[i - 1]
					summation += params[eword][fword]
				
				log_product *= (1.0/(len(ewords) + 1))*(summation) 
			log_product *= (1./100.)

			log_likelihood += numpy.log(log_product)

			for j in range(len(fwords)):
				total = 0.0
				for word in ewords:
					total += params[word][fwords[j]]

				for i in range(len(ewords) + 1):
					eword = ''
					fword = fwords[j]
					if i == 0:
						eword = 'NULL'
					else:
						eword = ewords[i - 1]
					if fword not in counts:
						counts[fword] = dict()
					if eword not in counts[fword]:
						counts[fword][eword] = params[eword][fword] / total
					else:
						counts[fword][eword] += params[eword][fword] / total


	for e in ewordtypes:
		total = 0
		for fp in params[e]:
			total += counts[fp][e]
		for f in params[e]:
			params[e][f] = counts[f][e]/total
	return log_likelihood

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) != 1:
		print("Wrong number of arguments. Expected: 1")
		exit(1)

	trainfile = args[0]
	#read in file
	with open("train.zh-en") as file:
		for line in file:
			e = line.strip().split('\t')[1]
			f = line.strip().split('\t')[0]
			ewords = e.strip().split(' ')
			ewords.append('NULL')
			for eword in ewords:
				for fword in f.strip().split(' '):
					ewordtypes.add(eword)
					fwordtypes.add(fword)
					if eword not in params:
						params[eword] = dict()
					if fword not in params[eword]:
						params[eword][fword] = 0.0

	#initialize to uniform
	for e in params:
		total = 0.0
		for f in params[e]:
			total += 1.0
		for f in params[e]:
			params[e][f] = 1.0/total

	print("Training model")
	for iteration in range(10):
		print("Starting iteration: {}".format(iteration))
		log_likelihood = EM(trainfile)
		print("The log_likelihood was: {}".format(log_likelihood))
	print("Testing model from train.zh-en and writing to align.out")

	with open(outputfile, 'w') as outfile, open(trainfile) as infile:
		for line in infile:
			e = line.strip().split('\t')[1]
			f = line.strip().split('\t')[0]
			ewords = e.strip().split(' ')
			ewords.append('NULL')
			fwords = f.strip().split(' ')
			for j in range(len(fwords)):
				best = None
				for i in range(len(ewords)):
					if not best or params[ewords[i]][fwords[j]] > best[2]:
						best = (j, i, params[ewords[i]][fwords[j]])
				if not best[1] == len(ewords) - 1:
					outfile.write('{}-{} '.format(best[0],best[1]))
				else:
					outfile.write('{}-{} '.format(best[0], '_' ))
			outfile.write('\n')

