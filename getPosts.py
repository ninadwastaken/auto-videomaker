"""
./getPost <subreddit>
output: urls
"""
client_id="igvNsz7UvomjacrasRXFPA"
secret_key="HK9ivn3H_GodvOq79g4qhii8VvUA1A"
import requests
auth=requests.auth.HTTPBasicAuth(client_id,secret_key)
data={"grant_type":"password",
      "username":"Denviser",
      "password":"hello1234"}
headers={'User-Agent':'MyAPI/0.0.1'}
res=requests.post('https://www.reddit.com/api/v1/access_token',auth=auth,data=data,headers=headers)
TOKEN=res.json()['access_token']
headers={**headers,**{'Authorization':f'bearer {TOKEN}'}}
#print(headers)
subreddit=input("Enter subreddit:")
res=requests.get('https://oauth.reddit.com/r/{subreddit}/hot'.format(subreddit=subreddit),headers=headers).json()
import pandas as pd
df=pd.DataFrame()
outaa_list=[]
print(res)
for post in res['data']['children']:
    output_dict={}
    output_dict['subreddit']=post['data']['subreddit']
    output_dict['text']=post['data']['selftext']
    outaa_list.append(output_dict)
import json
file=open("test.json",'w')
json.dump(outaa_list[5],file)
