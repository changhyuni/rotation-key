import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def diff_dates(date1, date2):
    return abs(date2 - date1).days

resource = boto3.resource('iam')
client = boto3.client("iam")

KEY = 'LastUsedDate'
AFTER_DAYS = 3

OldkeyList = []
email_text = f"""
To learn how to rotate your AWS Access Key, please read the official guide at https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_RotateAccessKey
If you have any question, please don't hesitate to contact the Support Team at changhyun.kim@example.com.

This automatic reminder will be sent again in {AFTER_DAYS} days, if the key(s) will not be rotated.

Regards,
Product Engineering DevOps Team
"""


def get_old_access_key():
    for user in resource.users.all():
        Metadata = client.list_access_keys(UserName=user.user_name)
        if Metadata['AccessKeyMetadata']:
            for key in user.access_keys.all():
                
                AccessId = key.access_key_id
                Status = key.status
                CreatedDate = key.create_date
                

                numOfDays = diff_dates(utc_to_local(datetime.utcnow()), utc_to_local(CreatedDate))
                LastUsed = client.get_access_key_last_used(AccessKeyId=AccessId)

                if (numOfDays >= AFTER_DAYS  and (Status == "Active")) and (KEY in LastUsed['AccessKeyLastUsed']):
                        OldkeyList.append(user.user_name+AccessId)
                # print(user.user_name, numOfDays)


get_old_access_key()

def disable_key(access_key, username):
    # try:
    client.update_access_key(UserName=username, AccessKeyId=access_key, Status="Inactive")
    # print(access_key + " has been disabled.")
    # except ClientError as e:
        # print("The access key with id %s cannot be found" % access_key)

def delete_key(access_key, username):
    # try:
    delete = client.delete_access_key(UserName=username, AccessKeyId=access_key)
    # except ClientError as e:
    #     print("The access key with id %s cannot be found" % access_key)

def create_key(username):
    access_key_metadata = client.create_access_key(UserName=username)
    access_key = access_key_metadata['AccessKey']['AccessKeyId']
    secret_key = access_key_metadata['AccessKey']['SecretAccessKey']
    print(access_key, secret_key)


for i in OldkeyList:
    disable_key(i[-20:],i[:-20])
    delete_key(i[-20:],i[:-20])
    create_key(i[:-20])



    
# print(OldkeyList[1][-20:])
# print(OldkeyList[1][:-20])
# print(client.delete_access_key(UserName='bhs9610@naver.com'))

# print(OldkeyList)
