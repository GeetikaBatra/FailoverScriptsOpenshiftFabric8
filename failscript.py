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
	manifest_files = {"manifest[]": open( "/Users/gbatra/test/maven-multi-module-example-2/pom.xml", 'rb')}
	req_data = requests.post(url, headers=headers, files=manifest_files, data=data)
	stack_id = req_data.json().get("id")
	oc_scale("bayesian-api")

	status = 500
	while status>=500:
		
		try:
			time.sleep(10)
			print(stack_id)
			poll_stack = requests.get(url + "/" + stack_id, headers=headers)
			print(poll_stack)
			status = poll_stack.status_code	
		except Exception:
			status = 500
			continue

	count = 1
	while True:
		if stack_id is not None:
			poll_stack = requests.get(url + "/" + stack_id, headers=headers)
			if poll_stack.status_code==202:
				time.sleep(10)
				count = count + 1
			if count>=5:
				print("Analyses still in progress")
				break
			if  poll_stack.status_code>=500:
				raise ValueError('Internal Server Error')
			elif(poll_stack.status_code==200):
				print("Analyses finished")
				print(poll_stack.json)
				break


if __name__ == "__main__":
	request_stack_analyses()
