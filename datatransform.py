from google.cloud import translate
import csv
import itertools

def chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i+n]

translate_client = translate.Client()

texttotranslate = []
supportinginfo = []
spanish = []
tengligh = []
result = []
spansishcode = 'es'
englishcode = 'en'
with open('train.csv', newline='') as train:
	trainreader = csv.reader(train, delimiter=',')
	for row in trainreader:
		texttotranslate.append(row[1])
		supportinginfo.append((row[0], row[2]))

texttotranslateparts = chunks(texttotranslate, 128)
for chunk in texttotranslateparts:
	result.append(translate_client.translate(chunk, spansishcode))

result = list(itertools.chain.from_iterable(result))

for i in range(len(result)):
	spanish.append((supportinginfo[i][0], result[i]['translatedText'], supportinginfo[i][1]))

texttotranslate.clear()
for row in spanish:
	texttotranslate.append(row[1])

texttotranslateparts = chunks(texttotranslate, 128)
result.clear()
for chunk in texttotranslateparts:
	result.append(translate_client.translate(chunk, englishcode))

result = list(itertools.chain.from_iterable(result))

for i in range(len(result)):
	tengligh.append((supportinginfo[i][0], result[i]['translatedText'], supportinginfo[i][1]))

with open('translatedenglish.csv', 'w', newline='') as tcsv:
	trainwriter = csv.writer(tcsv, delimiter=',', quoting=csv.QUOTE_ALL)
	trainwriter.writerows(tengligh)

with open('translatedspanish.csv', 'w', newline='') as tcsv:
	spanishwriter = csv.writer(tcsv, delimiter=',', quoting=csv.QUOTE_ALL)
	spanishwriter.writerows(spanish)
