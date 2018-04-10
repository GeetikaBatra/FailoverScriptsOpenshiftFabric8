#Assuming the deployment is up and running on devcluster.
import requests
import os
import subprocess
import json
import time
import sys

def oc_scale(deployment):
    subprocess.check_output("oc scale dc/{} --replicas=0".format(deployment),shell=True)
    subprocess.check_output("oc scale dc/{} --replicas=1".format(deployment),shell=True)

def request_stack_analyses():
	manifest_files = {}
	with open('/Users/gbatra/test/multi-maven-test-repo/pom.xml', 'rb') as f:
		manifest_files["manifest[]"] = f.read()
	url = "http://bayesian-api-gbatra-fabric8-analytics.dev.rdu2c.fabric8.io/api/v1/stack-analyses"
	auth_key = os.environ.get("auth_token")
	if auth_key is None:
		print("Auth is None")
		sys.exit()
	headers = { "Authorization" : auth_key}
	data = {"filePath[]" : "/Users/gbatra/test/maven-multi-module-example-2"}

	req_data = requests.post(url, headers=headers, files=manifest_files, data=data)
	import pdb
	pdb.set_trace()
	stack_id = req_data.get("id")
	oc_scale("bayesian-api")

	time.sleep(30)
	count = 1
	while True:
		if stack_id is not None:
			poll_stack = requests.get(url + "/" + stack_id)
			if poll_stack.status==202:
				time.sleep(10)
				count = count + 1
			if count>=5:
				print("Analyses still in progress")
				break
			else:
				print("Analyses finished")
				print(poll_data.json)
				break


if __name__ == "__main__":
	request_stack_analyses()
