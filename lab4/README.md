## Resources

### [IoT Lab 4 - Cloud Infrastructure](https://docs.google.com/document/d/1jGwZm8tqlL6oLWmkkgJBhWS2Dsp8oIEpZlACRNfJgug/edit#heading=h.soui4g3ymptg)

1. Get your [AmazonRootCA](https://www.amazontrust.com/repository/AmazonRootCA1.pem) and place it at the root of the project (AmazonRootCA1.pem)

2. Create a /data folder and /certificates folder (included in .gitignore)

3. Get the [data.zip](https://drive.google.com/file/d/13QEjW5uxVXCkY4VHR1stR8yEKpfc64fX/view?usp=sharing) from the [Kaggle heartbeat project](https://www.kaggle.com/shayanfazeli/heartbeat) and place in /data folder.

4. Get a python version running that has all the required libraries installed (via pip): `pip install pandas numpy boto3 json AWSIoTPythonSDK.MQTTLib`

5. Get your AWS credentials in order via `aws configure` CLI command. This puts aws_access_key_id and aws_secret_access_key into in `~/.aws/credentials`, which you download from the IAM service section (global creds)

6. Create a policy in the IoT service space and a Thing Group (region specific, such as US-EAST-1)

7. Update the code in createThing-Cert.py to match the region, policy name, group name, etc.

8. Run the above code with python and a parameter to create a number of devices, such as 30: `python createThing-Cert.py 30`. This should generate 30 device folders under ./certificates with all the associated .pem files. You can also see all these things in your [thing group](https://us-west-2.console.aws.amazon.com/iot/home?region=us-west-2#/thingGroup/CS498)

9. Update the code in emulator-client.py to match the number of devices generated and determining your IoT endpoint with: `aws iot describe-endpoint --endpoint-type iot:Data-ATS` (e.g. "a12nbrmsd21s59-ats.iot.us-west-2.amazonaws.com")

10. Run the emulator code. It will ask you so send now? which you respond with `s` once MQTT is configured.

11. TO BE CONTINUED
