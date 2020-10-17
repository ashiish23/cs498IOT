################################################### Connecting to AWS
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import json
################################################### Create random name for things
import random
import string
################################################### Parameters for Thing
thingArn = ''
thingId = ''
thingTypeName = 'wearable'
defaultPolicyName = 'openIOTpolicy' # 'arn:aws:iam::876612415673:policy/openIOTpolicy'
defaultGroupName = 'CS498' # 'arn:aws:iot:us-west-2:876612415673:thinggroup/CS498'
myRoleName = 'IoThing'
myRoleARN = 'arn:aws:iam::876612415673:role/IoThing' # needs write access to CloudWatch logs
loggingLevel = 'DEBUG' #|'INFO'|'ERROR'|'WARN'|'DISABLED'

my_config = Config(
    region_name = 'us-west-2',
    # signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

thingClient = boto3.client('iot', config=my_config)
# set logging to debug
response = thingClient.set_v2_logging_options(
    roleArn=myRoleARN, # needs access to CloudWatch
    defaultLogLevel=loggingLevel
    # disableAllLogs=True|False # defaults to false
)
response = thingClient.set_v2_logging_level(
    logTarget={
        'targetType': 'THING_GROUP',
        'targetName': defaultGroupName
    },
    logLevel='DEBUG'
)

 # if policy above does not exist, could create it with boto3 equivalent of
 # aws iot create-policy --policy-name defaultPolicyName --policy-document "./policy.json"
###################################################
import os
import sys

def createThing(device_id, thingName):
	global thingClient
	thingResponse = thingClient.create_thing(thingName = thingName, thingTypeName = thingTypeName)
	data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
	for element in data:
		if element == 'thingArn':
			thingArn = data['thingArn']
		elif element == 'thingId':
			thingId = data['thingId']
			
	thingClient.add_thing_to_thing_group(thingName = thingName, thingGroupName = defaultGroupName)
	createCertificate(device_id, thingName)

def createCertificate(device_id, thingName):
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(
		setAsActive = True
	)
	data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
	# print(data.values)
	for element in data: 
		if element == 'certificateArn':
			# print('Certificate ARN: '+data['certificateArn'])
			certificateArn = data['certificateArn']
		elif element == 'keyPair':
			# print('PublicKey'+data['keyPair']['PublicKey'])
			PublicKey = data['keyPair']['PublicKey']
			# print('Private Key: '+data['keyPair']['PrivateKey'])
			PrivateKey = data['keyPair']['PrivateKey']
		elif element == 'certificatePem':
			# print('Certificate Pem: '+data['certificatePem'])
			certificatePem = data['certificatePem']
		elif element == 'certificateId':
			# print('Certificate ID: '+data['certificateId'])
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
		#groupName = defaultGroupName,
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
		thingName = defaultGroupName+'_'+''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
		createThing(i, thingName)