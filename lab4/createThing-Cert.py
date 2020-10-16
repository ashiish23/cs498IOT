################################################### Connecting to AWS
import boto3
import json
################################################### Create random name for things
import random
import string
################################################### Parameters for Thing
thingClient = boto3.client('iot')
thingArn = ''
thingId = ''
defaultPolicyName = 'My_Iot_Policy'
###################################################
import os
import sys

def createThing(device_id, thingName):
	global thingClient
	thingResponse = thingClient.create_thing(thingName = thingName)
	data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
	for element in data:
		if element == 'thingArn':
			thingArn = data['thingArn']
		elif element == 'thingId':
			thingId = data['thingId']
	createCertificate(device_id, thingName)

def createCertificate(device_id, thingName):
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(
		setAsActive = True
	)
	data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
	for element in data: 
		if element == 'certificateArn':
			certificateArn = data['certificateArn']
		elif element == 'keyPair':
			PublicKey = data['keyPair']['PublicKey']
			PrivateKey = data['keyPair']['PrivateKey']
		elif element == 'certificatePem':
			certificatePem = data['certificatePem']
		elif element == 'certificateId':
			certificateId = data['certificateId']

	# Create directories and files for Thing certificates
	f1 = "./certificates/device_{}/device_{}.public.pem".format(device_id,device_id)
	f2 = "./certificates/device_{}/device_{}.private.pem".format(device_id,device_id)
	f3 = "./certificates/device_{}/device_{}.certificate.pem".format(device_id,device_id)
	for f, content in [(f1,PublicKey),(f2,PrivateKey),(f3,certificatePem)]:
		os.makedirs(os.path.dirname(f), exist_ok=True)					
		with open(f, 'w') as outfile:
			outfile.write(content)

	response = thingClient.attach_policy(
		policyName = defaultPolicyName,
		target = certificateArn
	)
	response = thingClient.attach_thing_principal(
		thingName = thingName,
		principal = certificateArn
	)

if __name__ == "__main__":
	num_devices = int(sys.argv[1]) if sys.argv[1] else 10
	for i in range(num_devices):
		thingName = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
		createThing(i, thingName)