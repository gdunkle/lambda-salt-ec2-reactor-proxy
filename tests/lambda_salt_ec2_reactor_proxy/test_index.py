##############################################################################
#  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.   #
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License").           #
#  You may not use this file except in compliance                            #
#  with the License. A copy of the License is located at                     #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  or in the "license" file accompanying this file. This file is             #
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  #
#  KIND, express or implied. See the License for the specific language       #
#  governing permissions  and limitations under the License.                 #
##############################################################################
from moto import (
    mock_s3
)
import json
import os
import boto3
from requests_mock import (
    Mocker
)
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["SALT_MASTER_ENDPOINT"] = "http://salt-master.onprem-awsgalen.com:8080/hook/ec2/autoscale"

@mock_s3
def test_lambda_handler():
    with Mocker() as mock:
        mock.post('http://salt-master.onprem-awsgalen.com:8080/hook/ec2/autoscale', text='success: true')
        session = boto3.session.Session()
        event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0',
                              'EventSubscriptionArn': 'arn:aws:sns:us-east-2:123456789012:ec2-autoscale-notification:6645e6f3-2efc-41c2-a42c-88bd5779718b',
                              'Sns': {'Type': 'Notification', 'MessageId': 'cd2c0a69-7ce2-5d89-b586-523e741e14bf',
                                      'TopicArn': 'arn:aws:sns:us-east-2:123456789012:ec2-autoscale-notification',
                                      'Subject': 'Auto Scaling: launch for group "Test"',
                                      'Message': '{"Progress":50,"AccountId":"123456789012","Description":"Launching a new EC2 instance: i-03cfd6816e40bf9a9","RequestId":"f7a5d9dd-8760-bea7-4791-40188ec73279","EndTime":"2020-12-18T19:45:00.886Z","AutoScalingGroupARN":"arn:aws:autoscaling:us-east-2:123456789012:autoScalingGroup:ab007579-3d71-4cdb-ba01-7459f8ddf514:autoScalingGroupName/Test","ActivityId":"f7a5d9dd-8760-bea7-4791-40188ec73279","StartTime":"2020-12-18T19:44:29.743Z","Service":"AWS Auto Scaling","Time":"2020-12-18T19:45:00.886Z","EC2InstanceId":"i-03cfd6816e40bf9a9","StatusCode":"InProgress","StatusMessage":"","Details":{"Subnet ID":"subnet-0ea442a34acb3f730","Availability Zone":"us-east-2b"},"AutoScalingGroupName":"Test","Cause":"At 2020-12-18T19:44:21Z a user request update of AutoScalingGroup constraints to min: 1, max: 5, desired: 3 changing the desired capacity from 2 to 3.  At 2020-12-18T19:44:27Z an instance was started in response to a difference between desired and actual capacity, increasing the capacity from 2 to 3.","Event":"autoscaling:EC2_INSTANCE_LAUNCH"}',
                                      'Timestamp': '2020-12-18T19:45:00.926Z', 'SignatureVersion': '1',
                                      'Signature': 'utwj+1nWl21Ny3IO0F+OO1IHEWW1BFk9IUPzJj1VUeJwhpn5x6QQ4y9oLNZaeDEE6M5b3y1PbPZAYo0b55QOuzedzhb8EzE6zUBtgaD/DUbJnkTU6H/ocESvtV+0CUBK4JyC5ajtMhIy/sErhzWzxu2fGTIYj9RPlKo0aaPlLNQ3qBFiisnm6meCt2VaTRcFTlDx3M1lUFOd99PK9lLL5pK0RAjbx2f+u0qIe65TAkkjWxW+KXG/GVaU8rMVqIRQLKU3wEDVVCv7z8YA6eboBUR4zkgMXByZfnsUyCyym4XzA8CMKFboVd8fFUbtHLV22/jfychocmr63o02AepwCw==',
                                      'SigningCertUrl': 'https://sns.us-east-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem',
                                      'UnsubscribeUrl': 'https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:123456789012:ec2-autoscale-notification:6645e6f3-2efc-41c2-a42c-88bd5779718b',
                                      'MessageAttributes': {}}}]}
        from lambda_salt_ec2_reactor_proxy import (
            index
        )
        resp_data = index.lambda_handler(event, {})
        expected_resp = "{\"status_code\": 200, \"body\": {\"results\": [{\"status_code\": 200, \"text\": \"success: true\"}]}}"
        assert json.dumps(resp_data) == json.dumps(expected_resp)
