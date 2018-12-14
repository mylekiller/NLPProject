
import sys


if __name__ == "__main__":

	args = sys.argv[1:]

	if len(args) != 1:
		print("Wrong number of arguments. Expected: 1")
		exit(1)


	grammarfile = args[0]

	with open(grammarfile) as infile:
		for line in infile:
			result = ""
			for word in line.strip().split():
				if word[0] == '<' and word[-1] == '>':
					result += word[1:].split(',')[0] + ' | ' + word[:-1].split(',')[1] + ' '
				elif word[0] == '<':
					if word.__contains__(','):
						result += word[1:].split(',')[0] + ' | ' + word[1:].split(',')[1] + ' '
					result += word[1:] + ' '
				elif word[-1] == '>' and word[0] != '-':
					if word.__contains__(','):
						result += word[:-1].split(',')[0] + ' | ' + word[:-1].split(',')[1] + ' '
					result += word[:-1] + ' '
				elif word.__contains__(',') and len(word) > 1:
					result+= word.split(',')[0] + ' | ' + word.split(',')[1] + ' '
				else:
					result += word + ' '
			print(result)