import argparse
import logging
parser = argparse.ArgumentParser(description='Name clusters from K-means by extracting most common word(s)')
parser.add_argument("-p", "--path", help="path to file of new line delimited strings.", required=True)
parser.add_argument("-i", "--inside", help="Check cluster names against own cluster or outside clusters. For own cluster, -i true", required=True)

args = parser.parse_args()
#Text pre-processing
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

nltk.download('stopwords')
nltk.download('wordnet')

#Cleaning the text
import string
def text_process(text):
    '''
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove digits
    3. Remove all stopwords from included languages
   	4. Return the cleaned text as a list of words
    '''
    stemmer = WordNetLemmatizer()
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join([i for i in nopunc if not i.isdigit()])
    nopunc =  [word.lower() for word in nopunc.split() if word not in stopwords.words('english') and word not in stopwords.words('french') and word not in stopwords.words('german') 			and word not in stopwords.words('spanish') and word not in stopwords.words('italian') and word not in stopwords.words('dutch')]
    return [stemmer.lemmatize(word) for word in nopunc]

def toArr(arr):
	arr = arr.replace("\\\\n","")
	arr = arr.replace("\\n","")
	if len(arr[0:len(arr)].split("\', \'")) > 1:
		arr = arr[0:len(arr)].split("\', \'")
		for val in range(0,len(arr)):
			arr[val] = (re.sub("[^a-zA-Z0-9 -]", "", arr[val].lower()).strip())
	else:
		arr = [(re.sub("[^a-zA-Z0-9 -]", "", arr.lower()).strip())]
	return arr

def scoreOut(f):
	bofw = {}
	f1 = f.readlines()
	c = 0
	for l in range(0,len(f1)):
		if len(f1[l].split("\t||\t")) < 2:
			continue
		name = re.sub("/\s+/g", ' ',f1[l].split("\t||\t")[0]).strip()
		bofw[name] = 0
	for l in f1:
		c = c+1
		if len(l.split("\t||\t")) < 2:
			continue
		name = re.sub("/\s+/g", ' ',l.split("\t||\t")[0]).strip()
		t = l.split("\t||\t")[1]
		arr = toArr(t)
		group = []
		for v in arr:
			group.append(text_process(v))
		sets = map(set, group)
		for s in sets:
			for w in bofw.keys():
				if w == name:
					continue
				keys = set(w.split(" "))
				if keys.issubset(s):
					bofw[w] = int(bofw[w]) + 1
		logging.warning(str(c) + " of " + str(len(f1)))
	for w in bofw.keys():
		print(w, "\t", int(bofw[w])/len(f1))


def scoreIn(f):
	c = 0
	for l in f:
		if len(l.split("\t||\t")) < 2:
			continue
		name = re.sub("/\s+/g", ' ',l.split("\t||\t")[0]).strip().split(" ")
		t = l.split("\t||\t	")[1]
		arr = toArr(t)
		count = 0
		keys = set(name)
		for v in arr:
			val = set(text_process(v))
			if keys.issubset(val):
				count = count+1
		p = count/len(arr)
		#logging.warning(str(c))
		#print(*name)
		#print(p)
		print(*name, "\t", p, "\t", str(c))
		c = c+1

with open(args.path) as f:
	if args.inside.lower() == "true":
		print("Scoring own clusters")
		scoreIn(f)
	else:
		print("Scoring against other clusters")
		scoreOut(f)









