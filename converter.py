import os, re
import json
import pdb
import collections
from bs4 import BeautifulSoup
from django.utils.text import slugify

sourceLink = 'http://www.gurbanifiles.org'
source = 'Gurbani Files'

works = [{
	'originalTitle': "ਗੁਰੂ ਗ੍ਰੰਥ ਸਾਹਿਬ ਜੀ",
	'englishTitle': "Guru Granth Sahib",
	'author': "Not available",
	'dirname': "guru_granth_sahib",
	'source': source,
	'sourceLink': sourceLink,
	'language': 'punjabi',
	'text': {},
}]

def jaggedListToDict(text):
	node = { str(i): t for i, t in enumerate(text) }
	node = collections.OrderedDict(sorted(node.items()))
	for child in node:
		if isinstance(node[child], list):
			node[child] = jaggedListToDict(node[child])
	return node

def main():
	if not os.path.exists('cltk_json'):
		os.makedirs('cltk_json')
	# Build json docs from txt files
	for root, dirs, files in os.walk("."):
		path = root.split('/')
		print((len(path) - 1) * '---', os.path.basename(root))
		for fname in files:
			if fname == 'complete_text.txt':
				print((len(path)) * '---', fname)

				for work in works:
					if work['dirname'] in path:
						with open(os.path.join(root, fname)) as f:
							lines = f.read().splitlines()

						text = []
						for line in lines:
							if len(line.strip()):
								text.append(line)

						work['text'] = jaggedListToDict(text)


	for work in works:
		fname = slugify(work['source']) + '__' + slugify(work['englishTitle'][0:100]) + '__' + slugify(work['language']) + '.json'
		fname = fname.replace(" ", "")
		with open('cltk_json/' + fname, 'w') as f:
			json.dump(work, f)

if __name__ == '__main__':
	main()
