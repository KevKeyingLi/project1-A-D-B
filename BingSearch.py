#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
from pprint import pprint
import sys
import re
import operator
import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
STOP_WORDS = ['a', 'ii', 'about', 'above', 'according', 'across', '39', 'actually', 'ad', 'adj', 'ae', 'af', 'after', 'afterwards', 'ag', 'again', 'against', 'ai', 'al', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anywhere', 'ao', 'aq', 'ar', 'are', 'aren', "aren't", 'around', 'arpa', 'as', 'associate', 'at', 'au', 'aw', 'az', 'b', 'ba', 'bb', 'bd', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bf', 'bg', 'bh', 'bi', 'billion', 'bj', 'bm', 'bn', 'bo', 'both', 'br', 'bs', 'bt', 'but', 'buy', 'bv', 'bw', 'by', 'bz', 'c', 'ca', 'can', "can't", 'cannot', 'caption', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'click', 'cm', 'cn', 'co', 'co.', 'com', 'copy', 'could', 'couldn', "couldn't", 'cr', 'cs', 'cu', 'cv', 'cx', 'cy', 'cz', 'd', 'de', 'did', 'didn', "didn't", 'dj', 'dk', 'dm', 'do', 'does', 'doesn', "doesn't", 'don', "don't", 'down', 'during', 'dz', 'e', 'each', 'ec', 'edu', 'ee', 'eg', 'eh', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'ep', 'er', 'es', 'et', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'f', 'few', 'fi', 'fifty', 'find', 'first', 'five', 'fj', 'fk', 'fm', 'fo', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'fr', 'free', 'from', 'further', 'fx', 'g', 'ga', 'gb', 'gd', 'ge', 'get', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gmt', 'gn', 'go', 'gov', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'h', 'had', 'has', 'hasn', "hasn't", 'have', 'haven', "haven't", 'he', "he'd", "he'll", "he's", 'help', 'hence', 'her', 'here', "here's", 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'hk', 'hm', 'hn', 'home', 'homepage', 'how', 'however', 'hr', 'ht', 'htm', 'html', 'http', 'hu', 'hundred', 'i', "i'd", "i'll", "i'm", "i've", 'i.e.', 'id', 'ie', 'if', 'il', 'im', 'in', 'inc', 'inc.', 'indeed', 'information', 'instead', 'int', 'into', 'io', 'iq', 'ir', 'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'j', 'je', 'jm', 'jo', 'join', 'jp', 'k', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'l', 'la', 'last', 'later', 'latter', 'lb', 'lc', 'least', 'less', 'let', "let's", 'li', 'like', 'likely', 'lk', 'll', 'lr', 'ls', 'lt', 'ltd', 'lu', 'lv', 'ly', 'm', 'ma', 'made', 'make', 'makes', 'many', 'maybe', 'mc', 'md', 'me', 'meantime', 'meanwhile', 'mg', 'mh', 'microsoft', 'might', 'mil', 'million', 'miss', 'mk', 'ml', 'mm', 'mn', 'mo', 'more', 'moreover', 'most', 'mostly', 'mp', 'mq', 'mr', 'mrs', 'ms', 'msie', 'mt', 'mu', 'much', 'must', 'mv', 'mw', 'mx', 'my', 'myself', 'mz', 'n', 'na', 'namely', 'nc', 'ne', 'neither', 'net', 'netscape', 'never', 'nevertheless', 'new', 'next', 'nf', 'ng', 'ni', 'nine', 'ninety', 'nl', 'no', 'nobody', 'none', 'nonetheless', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'np', 'nr', 'nu', 'nz', 'o', 'of', 'off', 'often', 'om', 'on', 'once', 'one', "one's", 'only', 'onto', 'or', 'org', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'overall', 'own', 'p', 'pa', 'page', 'pe', 'per', 'perhaps', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'pt', 'pw', 'py', 'q', 'qa', 'r', 'rather', 're', 'recent', 'recently', 'reserved', 'ring', 'ro', 'ru', 'rw', 's', 'sa', 'same', 'sb', 'sc', 'sd', 'se', 'seem', 'seemed', 'seeming', 'seems', 'seven', 'seventy', 'several', 'sg', 'sh', 'she', "she'd", "she'll", "she's", 'should', 'shouldn', "shouldn't", 'si', 'since', 'site', 'six', 'sixty', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'sr', 'st', 'still', 'stop', 'su', 'such', 'sv', 'sy', 'sz', 't', 'taking', 'tc', 'td', 'ten', 'tells', 'text', 'tf', 'tg', 'test', 'th', 'than', 'that', "that'll", "that's", 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', "there'll", "there's", 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', "they'd", "they'll", "they're", "they've", 'thirty', 'this', 'those', 'though', 'thousand', 'three', 'through', 'throughout', 'thru', 'thus', 'tj', 'tk', 'tm', 'tn', 'to', 'together', 'too', 'toward', 'towards', 'tp', 'tr', 'trillion', 'tt', 'tv', 'tw', 'twenty', 'two', 'tz', 'u', 'ua', 'ug', 'uk', 'um', 'under', 'unless', 'unlike', 'unlikely', 'until', 'up', 'upon', 'us', 'use', 'used', 'using', 'uy', 'uz', 'v', 'va', 'vc', 've', 'very', 'vg', 'vi', 'via', 'vn', 'vu', 'w', 'was', 'wasn', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'web', 'webpage', 'website', 'welcome', 'well', 'were', 'weren', "weren't", 'wf', 'what', "what'll", "what's", 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', "who'd", "who'll", "who's", 'whoever', 'NULL', 'whole', 'whom', 'whomever', 'whose', 'why', 'wi', 'will', 'with', 'within', 'without', 'won', "won't", 'would', 'wouldn', "wouldn't", 'ws', 'www', 'x', 'y', 'ye', 'yes', 'yet', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'yt', 'yu', 'z', 'za', 'zm', 'zr', '10', 'z', 'href']
# same list of words,
def preprocessTitle(Title):
	# print("Title before preprocess: "+ Title)
	if ' - ' in Title:
		Title = Title[:Title.find(' - ')] 
	elif ' — ' in Title:
		Title = Title[:Title.find(' — ')]
	elif ' -- ' in Title:
		Title = Title[:Title.find(' -- ')] 
	elif ' | ' in Title:
		Title = Title[:Title.find(' | ')]
	elif ': ' in Title:
		Title = Title[:Title.find(': ')]
	# print("Title after preprocess: "+ Title)
	return Title

def writeTranscript(msg):
    if not os.path.exists(os.path.dirname(TRANSCRIPT_FILE)):
      os.makedirs(os.path.dirname(TRANSCRIPT_FILE))
    with open(TRANSCRIPT_FILE, 'a') as logFile:
        logFile.write( msg+'\n')

def containsNumbers(s):
		return any(char.isdigit() for char in s)
	
def stemDerivaties(dictionary):
	stemmedDict = dict(dictionary)
	derivatives = []
	for root in dictionary:
		for word in dictionary:
			if (not containsNumbers(root)) and (not containsNumbers(word)) and (root != word) and (root in word) and (word not in derivatives):
				stemmedDict[root] += stemmedDict[word]
				derivatives.append(word)
				
	for der in derivatives:
		if der in stemmedDict:
			del stemmedDict[der]
			print ('Deleted ' + der)
	
	return stemmedDict



def extractWords(db):
	word_list = re.compile('\w+').findall(db)
	word_list = [word.lower() for word in word_list]
	word_list = [word for word in word_list if word not in STOP_WORDS]
	return word_list
	
def processFeedBack(Q, R, NR):
	dictionary = dict()
	global QUERY
	for word in Q:
		if word in dictionary:
			dictionary[word] += ALPHA
		else:
			dictionary[word] = ALPHA
			
	for entries in R:
		for key in entries:
			for word in entries[key]:
				if word in dictionary:
					if key == 'Title':
						dictionary[word] += BETA1
					elif key == 'Description':
						dictionary[word] += BETA2
				else:
					if key == 'Title':
						dictionary[word] = BETA1
					elif key == 'Description':
						dictionary[word] = BETA2

	for entries in NR:
		for key in entries:
			for word in entries[key]:
				if word in dictionary:
					if key == 'Title':
						dictionary[word] += GAMMA1
					elif key == 'Description':
						dictionary[word] += GAMMA2
				else:
					if key == 'Title':
						dictionary[word] = GAMMA1
					elif key == 'Description':
						dictionary[word] = GAMMA2
	dictionary = stemDerivaties(dictionary)	
	sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
	word_cnt = 0
	qry_str = ''
	for word in sorted_dict:
		if word[0] in Q:
			pass
		else:
			if word_cnt < 2:
				qry_str += '%20' + word[0]
				QUERY += ' '+word[0]
				word_cnt += 1
	return [qry_str,Q]

#def getKeyWords(wordList)
	

# /home/gravano/6111/Html/Proj1/run.sh mz6wWvhFVxhgbqlz+aDPIa/V1uaygzWZreeE3L3+7CA 0.9 'gates'
# python search.py target precision keywords
# TARGET_PRECISION = 2
# QUERY = 'Taj Mahal'
R = [dict()]
NR = [dict()]
BING_API_KEY = 'mz6wWvhFVxhgbqlz+aDPIa/V1uaygzWZreeE3L3+7CA'
CREDENTIAL = 'Basic ' + (':%s' % BING_API_KEY).encode('base64')[:-1]
RESULT_NUM = 10
TRANSCRIPT_FILE = './transcript.txt'
ALPHA = 1
BETA1 = 1.5
BETA2 = 1
GAMMA1 = -0.75
GAMMA2 = -0.5
fail = False
if len(sys.argv) == 3:
	TARGET_PRECISION = float(sys.argv[1])
	QUERY = sys.argv[2]
	precision = 0
	searchString = QUERY.split(' ')
	searchString = '+'.join(searchString)
	searchString = '%27'+searchString+'%27'
	round_cnt = 1
	print('Parameters:')
	# print('Client key  = '+BING_API_KEY)
	print('Query\t\t = '+QUERY)
	print('Target Precision= '+str(TARGET_PRECISION))
	# writeTranscript('\n')
	while precision<TARGET_PRECISION:
		writeTranscript('=====================================')
		writeTranscript('ROUND '+str(round_cnt) )
		writeTranscript('QUERY: '+QUERY)
		print('======================')
		relevantCount = 0
		nrCount = 0
		url = 'https://api.datamarket.azure.com/Bing/Search/Web?' + \
		'Query=%s&$top=%d&$format=json' % (searchString, RESULT_NUM)
		print("URL: "+url)

		request = urllib2.Request(url)
		request.add_header('Authorization', CREDENTIAL)
		requestOpener = urllib2.build_opener()
		response = requestOpener.open(request)
		results = json.load(response)['d']['results']
		print('Total number of results : '+str(len(results)))
		print('======================')
		print('Bing Search Results: ')
		idx = 1
		if len(results) < 10:
			print("Only "+str(len(results))+" results available. ")
			print("Terminated due to not enough documents")
			fail = True
			break
		for result in results:
			writeTranscript('\nResult '+str(idx))
			print('Result '+ str(idx))
			print("[")
			print("\tUrl: "+result['DisplayUrl'])
			print("\tTitle: "+result['Title'])
			print("\tSummary: "+result['Description'])
			print("]")
			while True:
				userFeedback = raw_input("Relevant (Y/N)?")
				print('\n')
				if len(userFeedback) > 1:
					print("Wrong input. ")
					continue
				elif userFeedback == 'Y' or userFeedback == 'y':
					# This is a positive example
					entry = {}
					entry['Title'] = extractWords(preprocessTitle(result['Title']))
					# print ('Title: ' + str(entry['Title']))
					entry['Description'] = extractWords(result['Description'])
					#print ('Desc: ' + str(entry['Description']))
					R.append(entry)
					relevantCount += 1
					writeTranscript("Relevant: YES")
					break
				elif userFeedback == 'N' or userFeedback == 'n':
					# This is a negative example
					entry = {}
					entry['Title'] = extractWords(preprocessTitle(result['Title']))
					entry['Description'] = extractWords(result['Description'])
					NR.append(entry)
					nrCount += 1
					writeTranscript("Relevant: NO")
					break
			writeTranscript('[')
			writeTranscript(" Url: "+result['DisplayUrl'])
			writeTranscript(" Title: "+result['Title'])
			writeTranscript(" Summary: "+result['Description'])
			writeTranscript("]\n")
			idx += 1
		precision = float(relevantCount)/RESULT_NUM
		writeTranscript('Precision: %.1f' % precision )
		if precision == 0:
			print('Precision is: %.1f' % precision)
			print('Program Terminated')
			fail = True
			break
		if precision<TARGET_PRECISION:
			print('Precision of this round: %.4f' % precision)
			Q = extractWords(QUERY)
			qry_str,Q = processFeedBack(Q, R, NR)
			print("Precision: "+str(precision))
			print("New Query: "+QUERY)
			searchString = searchString[:-3] + qry_str+'%27'
		# else:
		round_cnt += 1
	if not fail:
		print("Succeeded. "+("\nFinal precision: %.1f" % precision)+".\nFinal Query: "+QUERY )
else:
	print('Usage: python BingSearch.py <TARGET_PRECISION> <QUERY>')
	print("Take 2 Parameters")