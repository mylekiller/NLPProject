
import sys

rules = list()


def dedup(newrule):
	realnewrule = dict()
	realnewrule['e'] = list()
	realnewrule['f'] = list()
	found = False
	allowed = False
	for word in newrule['e']:
		if word != '*':
			allowed = True
			realnewrule['e'].append(word)
		else:
			if not found:
				realnewrule['e'].append(word)
				found = True
	for word in newrule['f']:
		if word != '*':
			allowed = True
			realnewrule['f'].append(word)
		else:
			if not found:
				realnewrule['f'].append(word)
				found = True
	if(allowed):
		newrule = realnewrule
	return allowed

def parsealignment(alignment):
	try:
		return (int(alignment.split('-')[0]), int(alignment.split('-')[1]))
	except:
		return (int(alignment.split('-')[0]), '_')
def issequential(positions, noaligns):
	if not len(positions):
		return False
	positionset = set(positions)
	for i in range(min(positions) , max(positions) + 1):
		if i not in positionset and i not in noaligns:
			return False
	return True
def isinconsistent(start, end, alignments):
	coalignments = set()
	for i in range(start, end + 1):
		if(parsealignment(alignments[i])[1] != len(ewords) - 1):
			coalignments.add(parsealignment(alignments[i])[1])
	for i in range(len(alignments)):
		if (i < start or i > end) and parsealignment(alignments[i])[1] in coalignments and parsealignment(alignments[i])[1] != '_':
			return True
	return False
def subtractrules(rule, start, end, coalignments):
	pass


def printrules(rules, file = None):
	with open(file, 'w') as outfile:

		for rule in rules:
			eoutput = ''
			foutput = ''
			for i in range(len(rule['e'])):
				eoutput += rule['e'][i]
				if i != len(rule['e']) - 1:
					eoutput += ' '
			for i in range(len(rule['f'])):
				foutput += rule['f'][i]
				if i != len(rule['f']) - 1:
					foutput += ' '

			outfile.write("* -> <{},{}>".format(foutput, eoutput))

if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) != 2:
		print("Wrong number of arguments. Expected: 2")
		exit(1)


	trainfilepath = args[0]
	alignfilepath = args[1]

	progress = 0
	with open(trainfilepath) as trainfile, open(alignfilepath) as alignfile:
		for line in trainfile:
			print(progress)
			ewords = line.strip().split('\t')[1].split()
			fwords = line.strip().split('\t')[0].split()
			ewords.append('NULL')
			noaligns = set()
			alignments = next(alignfile).split()

			positions = dict()
			for alignment in alignments:
				positions[parsealignment(alignment)[0]] = parsealignment(alignment)[1]
			for i in range(len(ewords) - 1):
				found = False
				for key in positions:
					if positions[key] == i:
						found = True
						break
				if not found:
					noaligns.add(i)


			for start in range(len(fwords)):
				for end in range(start,len(fwords)):
					if isinconsistent(start, end, alignments):
						continue
					coalignments = list()
					
					for i in range(start, end + 1):
						if(parsealignment(alignments[i])[1] != len(ewords) - 1):
							if parsealignment(alignments[i])[1] !='_':
								coalignments.append(parsealignment(alignments[i])[1])
					
					if(issequential(coalignments, noaligns)):
						rule = dict()
						rule['e'] = list()
						rule['f'] = list()
						eoutput = ''
						for i in range(min(coalignments), max(coalignments) + 1):
							rule['e'].append(ewords[i])
						for i in range(start, end + 1):
							rule['f'].append(fwords[i])
						rules.append(rule)

						for i in range(min(coalignments), max(coalignments) + 1):
							newrule = dict()
							newrule['e'] = list()
							newrule['f'] = list()
							for wordpos in range(start, end + 1):
								if positions[wordpos]== i:
									newrule['f'].append('*')
								else:
									newrule['f'].append(fwords[wordpos])
							for wordpos in range(min(coalignments), max(coalignments) + 1):
								if wordpos == i:
									newrule['e'].append('*')
								else:
									newrule['e'].append(ewords[wordpos])
							if(dedup(newrule)):
								rules.append(newrule)
			progress = progress + 1
	printrules(rules, "SCFGbackup.txt")

