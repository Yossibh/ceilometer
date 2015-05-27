__author__ = 'yb831g@att.com'
# list meters - client initialized with get_client
#imports
from ceilometerclient import client
from os import environ as env
from ceilometerclient.common import utils

from keystoneclient.auth.identity import v2
from keystoneclient import session
from ceilometerclient import client
import requests, json
from requests.auth import AuthBase

class OpenstackAuth(AuthBase):
    """Attaches HTTP Pizza Authentication to the given Request object."""
    def __init__(self, username):
        # setup any auth-related data here
        self.username = username

    def __call__(self, r):
        # modify and return the request
        r.headers['X-Auth-Token'] = self.username
        return r

auth=v2.Password(auth_url="http://10.252.21.11:5000/v2.0", username="hd7171", password="sil7ver", tenant_name="Breeze-Dev")

sess = session.Session(auth=auth,verify=False)     # verify=False may not be required for you
token = auth.get_token(sess)
type(token)

#ceilometer_url = 'http://192.168.33.2:8777/v2.0/meters'
#print ceilometer_url

payload = {'q.field' : 'timestamp', 'q.op' : 'gt', 'q.value' : '2015-05-19T00:34:17', 'q.field' : 'resource_id', 'q.op' : 'eq', 'q.value' : '8cd6d751-fda7-45f7-865f-53a307be8052'}
r = requests.get('http://10.252.21.11:8777/v2/meters/cpu_util', auth=OpenstackAuth(token), params=payload)
#print r.json()
#print json.dumps(r.json(), indent=2)

j = json.loads(r.text)
for i in j:
    print (i['counter_name'])
    print (i['timestamp'])
    print (i['counter_volume'])
    print '--------'
#getting the credentials
keystone = {}
keystone['os_username']='hd7171'
keystone['os_password']='sil7ver'
keystone['os_auth_url']='http://10.252.21.11:5000/v2.0'
keystone['os_tenant_name']='Breeze-Dev'

#creating an authenticated client
ceilometer_client = client.get_client(2,**keystone)

#now you should be able to use the API
#meters = ceilometer_client.meters.list()
#samples = ceilometer_client.samples.list(meter_name = 'cpu_util')

#print json.dumps(samples.to_dict, separators=(',',':'))
#print meters
#cpu_util_sample = ceilometer_client.samples.list('cpu_util')

#print cpu_util_sample

#for each in cpu_util_sample:
#    print each.timestamp, each.resource_id, each.counter_volume
#    print '------------'
#print samples
