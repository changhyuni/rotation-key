import boto3
from datetime import datetime, timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def diff_dates(date1, date2):
    return abs(date2 - date1).days

resource = boto3.resource('iam')
client = boto3.client("iam")

KEY = 'LastUsedDate'
OldkeyList = []

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

                if numOfDays <= 6:
                    OldkeyList.append(user.user_name+AccessId)
                # print(user.user_name, numOfDays)

                # if (Status == "Active"):
                #     if KEY in LastUsed['AccessKeyLastUsed']:
                #         print("User:", user.user_name, numOfDays)

get_old_access_key()

def delete_key(access_key, username):
    delete = client.delete_access_key(UserName=username, AccessKeyId=access_key)
    return print(delete)

for i in OldkeyList:
    delete_key(i[-20:],i[:-20])
    
# print(OldkeyList[1][-20:])
# print(OldkeyList[1][:-20])
# print(client.delete_access_key(UserName='bhs9610@naver.com'))

# print(OldkeyList)
