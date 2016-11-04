#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
from pprint import pprint
import sys
import re
import operator
import os
import csv
import requests
import subprocess
import time


#Global Vars
global BING_API_KEY
global CREDENTIAL
BING_API_KEY = '' #'<API_KEY>'
CREDENTIAL = ''
RESULT_NUM = 4
PREFIX = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?'
		# 'https://api.datamarket.azure.com/Bing/SearchWeb/Web?'
DIR = './'
# Queries for each class
Computers = [ \
'cpu',
'java',
'module',
'multimedia',
'perl',
'vb',
'agp card',
'application windows',
'applet code',
'array code',
'audio file',
'avi file',
'bios',
'buffer code',
'bytes code',
'shareware',
'card drivers',
'card graphics',
'card pc',
'pc windows' \
]

Health = [ \
'acupuncture',
'aerobic',
'aerobics',
'aids',
'cancer',
'cardiology',
'cholesterol',
'diabetes',
'diet',
'fitness',
'hiv',
'insulin',
'nurse',
'squats',
'treadmill',
'walkers',
'calories fat',
'carb carbs',
'doctor health',
'doctor medical',
'eating fat',
'fat muscle',
'health medicine',
'health nutritional',
'hospital medical',
'hospital patients',
'medical patient',
'medical treatment',
'patients treatment' \
]

Sports = [ \
'laker',
'ncaa',
'pacers',
'soccer',
'teams',
'wnba',
'nba',
'avg league',
'avg nba',
'ball league',
'ball referee',
'ball team',
'blazers game',
'championship team',
'club league',
'fans football',
'game league' \
]

Hardware = [ \
'bios',
'motherboard',
'board fsb',
'board overclocking',
'fsb overclocking',
'bios controller ide',
'cables drive floppy' \
]

Programming = [ \
'actionlistener',
'algorithms',
'alias',
'alloc',
'ansi',
'api',
'applet',
'argument',
'array',
'binary',
'boolean',
'borland',
'char',
'class',
'code',
'compile',
'compiler',
'component',
'container',
'controls',
'cpan',
'java',
'perl' \
]

Diseases = [ \
'aids',
'cancer',
'dental',
'diabetes',
'hiv',
'cardiology',
'aspirin cardiologist',
'aspirin cholesterol',
'blood heart',
'blood insulin',
'cholesterol doctor',
'cholesterol lipitor',
'heart surgery',
'radiation treatment' \
]

Fitness = [ \
'aerobic',
'fat',
'fitness',
'walking',
'workout',
'acid diets',
'bodybuilding protein',
'calories protein',
'calories weight',
'challenge walk',
'dairy milk',
'eating protein',
'eating weight',
'exercise protein',
'exercise weight' \
]

Soccer = [ \
'uefa',
'leeds',
'bayern',
'bundesliga',
'premiership',
'lazio',
'mls',
'hooliganism',
'juventus',
'liverpool',
'fifa' \
]

Basketball = [ \
'nba',
'pacers',
'kobe',
'laker',
'shaq ',
'blazers',
'knicks',
'sabonis',
'shaquille',
'laettner',
'wnba',
'rebounds',
'dunks' \
]


QUERY = { \
'Computers': Computers,
'Health' : Health,
'Sports' : Sports,
'Hardware' : Hardware,
'Programming' : Programming,
'Diseases' : Diseases,
'Fitness' : Fitness,
'Soccer' : Soccer,
'Basketball' : Basketball \
}

# Parent pointer pointing from child class to parent
PARENT = { \
'Root' : '',
'Computers' : 'Root',
'Health' : 'Root',
'Sports' : 'Root',
'Hardware' : 'Computers',
'Programming' : 'Computers',
'Fitness' : 'Health',
'Diseases' : 'Health',
'Basketball' : 'Sports',
'Soccer' : 'Sports' \
}

# pointer from parent to child
CHILD = { \
'Root' : ['Computers', 'Health', 'Sports'],
'Computers' : ['Hardware', 'Programming'],
'Health' : ['Fitness', 'Diseases'],
'Sports' : ['Basketball', 'Soccer'] \
}


def writeCache(line, filename):
	if not os.path.exists(filename):
		with open(filename, 'a') as cache:
			cache.write( 'query,matches' + '\n')
			
	with open(filename, 'a') as cache:
		cache.write( line + '\n')

# return the number of matches for computing the coverage and specificity
def getMatches(query, site):
	source = 'Online'
	url = '<empty>'
	
	if os.path.exists(site):
		content = csv.DictReader(open(site))
		for line in content:
			if(line['query'] == query):
				matches = int(line['matches'])
				source = 'File'
	
	if source == 'Online':
		searchString = query.split(' ')
		searchString = '%20AND%20'.join(searchString)
		searchString = '%27site%3a' + site + '%20'+searchString+'%27'
		
		# Form the URL, and get the data by issuing REST request to the Bing API
		url = PREFIX + 'Query=%s&$top=%d&$format=json' % (searchString, 1)
		request = urllib2.Request(url)
		request.add_header('Authorization', CREDENTIAL)
		requestOpener = urllib2.build_opener()
		response = requestOpener.open(request)
		results = json.load(response)['d']['results']
		
		for result in results:
			# print result
			matches = int(result['WebTotal'])
			break
			
		writeCache(query + ',' + str(matches), site)
	
	'''
	print('======================')
	print("Source: " + source)
	print("Query: " + query)
	print("URL: " + url)
	print("Matches: " + str(matches))
	print('======================')
	'''
	
	return matches
	

def getCoverage(C, D):
	coverage = 0
	for query in QUERY[C]:
		coverage += getMatches(query, D)
	
	return coverage

def getSpec(C, D):
	if C == 'Root':
		return 1
	else:
		deno = 0
		# Sum up all the coverage of its siblings as denominator.
		for child in CHILD[PARENT[C]]:
			deno += getCoverage(child, D)
		
		spec = float(getSpec(PARENT[C], D)*getCoverage(C, D))/float(deno)
		return spec

def classify(C, D, tc, ts, r): # r is the classification result from the lower level
	# print(D + ' classified as ' + C)
	result = r + ' ' + C
	if C not in CHILD:
		return result
	# For each child, if coverage and specificity satisfies, we classify it as that class and check its child, if any
	for child in CHILD[C]: 
		spec = getSpec(child, D)
		coverage = getCoverage(child, D)
		print('Specificity for category:' + child + ' is ' + str(spec) + ' ' + str(spec >= ts) + ' ' + str(ts))
		print('Coverage for category:' + child + ' is ' + str(coverage) + ' ' + str(coverage >= tc) + ' ' + str(tc))
		if (spec >= ts) and (coverage >= tc):
			result = classify(child, D, tc, ts, result)
	getUrls(C,D)
	return result


URLs = dict()
CS = dict()# a dictionary for content summary
def getUrls(category, site):
	if category not in URLs:
		URLs[category] = set()
		CS[category] = dict()
	for child in CHILD[category]:
		# 
		for query in QUERY[child]:
			searchString = query.split(' ')
			searchString = '%20AND%20'.join(searchString)
			searchString = '%27site%3a' + site + '%20'+searchString+'%27'
			
			# Form the URL, and get the data by issuing REST request to the Bing API
			url = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/Web?' + 'Query=%s&$top=%d&$format=json' % (searchString, RESULT_NUM)
			request = urllib2.Request(url)
			request.add_header('Authorization', CREDENTIAL)
			requestOpener = urllib2.build_opener()
			response = requestOpener.open(request)
			results = json.load(response)['d']['results']
			for page in results:#[0]['Web']:
				# print("adding url "+page['Url'])
				URLs[category].add(page['Url'])


def summary(site):
	# Adjust the websites:
	for node in URLs:
		if node in CHILD:
			for cnode in CHILD[node]:
				if cnode in URLs:
					URLs[node].union(URLs[cnode])
	# 
	for node in URLs:
		for url in URLs[node]:
			# time.sleep(0.5)
			try:
				r = requests.get(url)
				content_type = r.headers.get('content-type')
				time.sleep(0.5)
			except Exception, e:
				content_type = ''
				# print('error occur requesting page')
			if 'text/html' in content_type:
				print("Getting page: "+url) #+" content-type: "+content_type
				try:
					result = subprocess.check_output("java getWordsLynx "+url, shell=True)
					word_list = result[1:-1].split(', ')
					for word in word_list:
						if word in CS[node]:
							CS[node][word] += 1
						else:
							CS[node][word] = 1
				except Exception, e:
					 print('error executing java Lynx')
	# Now we have the dictionary counting all the words, we can out put it to a file. 
	# print("\n\n Now the CS:\n")
	summary_lists = dict()
	for node in CS:
		summary_lists[node] = []
		for word in CS[node]:
			summary_lists[node].append(word+'#'+str(CS[node][word])+'\n')
		summary_lists[node] = sorted(summary_lists[node])

	for node in summary_lists:
		with open(DIR + node + "-" + site + ".txt", 'a') as f:
			for line in summary_lists[node]:
				# print(line[:-1])
				f.write(line)


##################################### Processing starts here ###############################################
if len(sys.argv) == 5:
	
	# get input
	BING_API_KEY = sys.argv[1]
	D = sys.argv[4] 
	tc = int(sys.argv[3])
	ts = float(sys.argv[2])
	CREDENTIAL = 'Basic ' + (':%s' % BING_API_KEY).encode('base64')[:-1]
	
	print
	print('Classifying...')
	print
	result = classify('Root', D, tc, ts, '')
	result = result.split(' ')
	result = '/'.join(result)
	print 
	print('Classification:')
	print(result)
	# getUrls('Root',D)
	print
	print('Constructing the content summary')
	summary(D)
	
else:
	print("Give all 4 Parameters as below")
	print('Usage: python qProber.py <BING_API_KEY> <t_es> <t_ec> <host>')