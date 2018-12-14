

import os,sys
import copy

def retracepath(path, rules):
	resultlist = list()
	resultlist.append('*')
	result = ''

	for rule in path:
		newlist = []
		for resultword in resultlist:
			if resultword != '*':
				newlist.append(resultword)
			else:
				for word in rules[rule].split():
					newlist.append(word)
		resultlist = newlist


	for word in resultlist:
		if word != '*':
			result += word + ' '
	result = result[:-1]
	return result
def parsestep(target, current, path, rules):
	bestrule = None
	currentwords = current.split()
	targetwords = target.split()
	testwords = list()
	for word in currentwords:
		if word != '*':
			testwords.append(word)
	if len(testwords) > len(targetwords):
		return None
	start = -1
	for i in range(len(targetwords)):
		if i > len(currentwords) - 1:
			return None
		elif currentwords[i] == '*':
			start = i
			break
		elif currentwords[i] != targetwords[i]:
			return None
	if start == -1:
		return path
	keylist = list()
	for key in rules:
		if not key:
			continue
		acceptable = True
		for i in range(len(key.split())):
			if not start + i > len(targetwords) - 1 and key.split()[i] == targetwords[start + i] or key.split()[i] == '*':
				if key.split()[i] == '*':
					acceptable = True
					break
			else:
				acceptable = False
				break
		if not acceptable:
			continue
		if key.split()[0] == targetwords[start] and len(key.split()) <= len(targetwords):
			keylist.append((key, len(key.split())))
	keylist.sort(key = lambda x : x[1])
	for keyt in keylist[0:30]:
		key = keyt[0]
		newcurrent = ''
		for i in range(len(currentwords)):
			if i == start:
				newcurrent += key + ' '
			else:
				newcurrent += currentwords[i] + ' '
		newcurrent = newcurrent[:-1]
		newpath = copy.deepcopy(path)
		newpath.append(key)
		result = parsestep(target,newcurrent, newpath, rules)
		if result != None:
			return result

def translate(line, rules):
	path = parsestep(line, '*', list(), rules)
	if path:
		return retracepath(path,rules)
	return line

if __name__ == "__main__":

	args = sys.argv[1:]

	if len(args) != 1:
		print("Wrong number of arguments. Expected: 1")
		exit(1)


	cleangrammarfilepath = args[0]

	rules = dict()
	with open(cleangrammarfilepath) as cleangrammarfile:
		for line in cleangrammarfile:
			rules[line[5:].split('|')[0].strip()] = line[5:].split('|')[1].strip()

	print("Done parsing rules. Here are your translations (this may take awhile!):")

	for line in sys.stdin:
		print translate(line.lower(), rules).strip()
		
		
			