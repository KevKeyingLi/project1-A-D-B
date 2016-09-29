#!/usr/bin/python

import urllib2
import json
from pprint import pprint
import sys

# /home/gravano/6111/Html/Proj1/run.sh mz6wWvhFVxhgbqlz+aDPIa/V1uaygzWZreeE3L3+7CA 0.9 'gates'
# python search.py target precision keywords
TARGET_PRECISION = 0
QUERY = ''
BING_API_KEY = 'mz6wWvhFVxhgbqlz+aDPIa/V1uaygzWZreeE3L3+7CA'
CREDENTIAL = 'Basic ' + (':%s' % BING_API_KEY).encode('base64')[:-1]
RESULT_NUM = 10


if len(sys.argv) == 3:
	TARGET_PRECISION = float(sys.argv[1])
	QUERY = sys.argv[2]
	precision = 0
	searchString = QUERY.split(' ')
	searchString = '+'.join(searchString)
	searchString = '%27'+searchString+'%27'
	# skip = 0
	round_cnt = 0
	while precision<TARGET_PRECISION:

		relevantCount = 0
		url = 'https://api.datamarket.azure.com/Bing/Search/Web?' + \
		'Query=%s&$top=%d&$format=json' % (searchString, RESULT_NUM)
		print("The url: "+url)
		request = urllib2.Request(url)
		request.add_header('Authorization', CREDENTIAL)
		requestOpener = urllib2.build_opener()
		response = requestOpener.open(request)
		results = json.load(response)['d']['results']
		# use some data structure to collect the user feedback
		idx = 1
		for result in results:
			print(idx)
			print("\tTitle: "+result['Title'])
			print("\tSummary: "+result['Description'])
			print("\tUrl: "+result['DisplayUrl'])
			# pprint(result)
			while True:
				userFeedback = raw_input("Relevant (Y/N)?")
				if len(userFeedback) > 1:
					print("Wrong input. ")
					continue
				elif userFeedback == 'Y' or userFeedback == 'y':
					# This is a positive example
					relevantCount += 1
					break
				elif userFeedback == 'N' or userFeedback == 'n':
					# This is a negative example
					break
			idx += 1
		precision = float(relevantCount)/RESULT_NUM
		if precision<TARGET_PRECISION:
			print('Precision of this round: %.4f' % precision)
			new_keyword = raw_input('This is for testing, please input ONE new keyword: ')# For Testing
			precision += 0.2# For Testing
			searchString = searchString[:-3]+'+'+new_keyword+'%27'
		round_cnt += 1
	print("Succeeded after "+str(round_cnt)+(" rounds of feedback. Final precision: %.4f" % precision)+"." )
else:
	print('show usage')
	print("Take 3 Parameters")


			
# Reference
#http://www.guguncube.com/2771/python-using-the-bing-search-api