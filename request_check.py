import argparse
import sys
import requests
import os
import re

current_path = os.getcwd()

parser = argparse.ArgumentParser(description='This script is used to check availability of target and can optionally download. Target is a list of URLs and could include both domain and IP addresses. ')
parser.add_argument("-t", "--target", help="Target list to check. 1 URL per line, prefixed with http:// ")
parser.add_argument("-m", "--method", help="get or port or head. Default check HTTP method is head.", default="head")
parser.add_argument("-o", "--output", help="Output file. Existing file will be overwrite. Default is output.txt", default="output.txt")
parser.add_argument("--download", help="Download the file after check", action='store_true')
parser.add_argument("--proxy", help="http://proxy:port", default='')
args = parser.parse_args()

if args.proxy:
	proxies = {
	  'http': args.proxy,
	  'https': args.proxy,
	}
else:
	proxies = args.proxy

if not args.target:
    sys.exit("input file needed")
else:
	file = args.target
	output = args.output
	http_method = args.method
	output_file = open(output, "w")
	print "target response_code"
	with open(file) as list:
		count = 1
		for url in list:
			output_text = ""
			url = url.rstrip()
			try:
				if http_method =='get':
					r = requests.get(url,proxies=proxies)
				elif http_method =='post':
					r = requests.post(url,proxies=proxies)
				else:
					r = requests.head(url,proxies=proxies)
				output_text = str(url) + " " + str(r.status_code) + "\r\n"
				print output_text.strip()
				output_file.write(output_text)
				if (args.download and r.status_code != 404):
					if not os.path.exists('downloads'):
						os.makedirs('downloads')
					local_filename = "downloads\\" + re.sub('[^0-9a-zA-Z]+', '_', url) 
					r = requests.get(url, stream=True)
					with open(local_filename, 'wb') as f:
						for chunk in r.iter_content(chunk_size=1024): 
							if chunk: 
								f.write(chunk)
			except requests.exceptions.RequestException as e:
				output_text = str(url) + " Check failed.\r\n"
				print output_text.strip()
				output_file.write(output_text)
			count += 1
	print "\nCompleted",str(count),"target. Check",str(current_path) + "\\" + str(output)

