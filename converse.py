import json
import argparse
import sys
import logging
import urllib2

logging.basicConfig()

def process_issue(issue):
	ret = {
		'title': 'ERROR',
		'body': 'ERROR',
		'asignee': '=',
		'labels': ['ERROR'],
		'state': 'closed',
		'upload': False
	}
	return ret

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Upload OpenHatch format JSON issues to GitHub Issues')
	parser.add_argument('-k',
		metavar='OAuth Key',
		dest='oauth_key',
		action='store',
		required=1,
		help='OAuth key to use in communications with the GitHub API')
	parser.add_argument('-r',
		metavar='Username/Repo',
		dest='uname_repo',
		action='store',
		required=1,
		help='username/repository to upload to e.g. 602p/issuetest')
	parser.add_argument('-j',
		metavar='File',
		dest='json_path',
		action='store',
		required=1,
		help='path to JSON file to load issues from')

	args = parser.parse_args(sys.argv[1:])
	log = logging.getLogger("converse")
	log.setLevel(10)

	log.info("Loading Issues...")

	try:
		issues = []
		with open(args.json_path, 'r') as json_file:
			for line in json_file.readlines():
				issues.append(json.loads(line))
	except:
		log.exception(args.json_path + " is not valid, exiting!")
		sys.exit(1)

	log.debug("Loaded " + str(len(issues)) +" Issues")
	log.info("Uploading to GitHub...")

	c = 1
	l = str(len(issues))
	for issue in issues:
		result = process_issue(issue)
		if result['upload']:
			req = urllib2.Request('https://api.github.com/repos/' +
				args.uname_repo + '/issues?access_token=' + args.oauth_key,
				json.dumps({
						'title': result["title"],
						'body': result["body"],
						'asignee': result["asignee"],
						'labels': result["labels"]
					})
				)
			resp = json.load(urllib2.urlopen(req))
			req2 = urllib2.Request('https://api.github.com/repos/' + 
				args.uname_repo + '/issues/' +
				str(resp["number"]) + '?access_token=' + args.oauth_key,
					json.dumps({
						'state': result["state"]
					})
				)
			urllib2.urlopen(req2)
			log.debug("Uploaded Issue " + str(c) + " of " + l)
		else:
			log.warning("Issue " + str(c) + " was not uploaded!")
		c += 1