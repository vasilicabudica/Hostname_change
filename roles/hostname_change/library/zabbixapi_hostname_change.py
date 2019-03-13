
from ansible.module_utils.basic import *
import json
import request

def HostnameChange(Changing hostname using zabbix api):

if __name__ == '__main__':
    main()

fileds = {
    "api_url" : {"required": "True", "type": "str"},
    "username": {"required": "True", "type": "str"},
    "password": {"required": "True", "type": "str"},
    "oldhost": {"required": "True", "type": "str"},
    "newhostname": {"required": "True", "type": "str"}
    }
}

# Reguest login to retrive auth
out_auth = requests.get(api_url,
                 headers={'Content-Type': 'application/json'},
                 data=json.dumps({
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": username,
        "password": password
    },
    "id": 1
}))
auth = out_auth.json()['result']

# Retrieve oldhostid by cluster api using auth id obtained
x = requests.get(api_url,
                 headers={'Content-Type': 'application/json'},
                 data=json.dumps({
                         "jsonrpc": "2.0",
                         "method": "host.get",
                         "params": {
                                    "output": "extend",
                                    "filter": {
                                         "oldhost": oldhost
                                              }
                                   },
                         "auth": auth,
                         "id": 1
                 }))
hostid = json.loads(json.dumps(x.json()['result'][0]))['hostid']
tls_psk_identity = json.loads(json.dumps(x.json()['result'][0]))['tls_psk_identity'].split('_')[1]

# Post a api request to change the name of the server
z = requests.post('https://monitor.seinternal.com/api_jsonrpc.php',
                 headers={'Content-Type': 'application/json'},
                 data=json.dumps({
                         "jsonrpc": "2.0",
                         "method": "host.update",
                         "params": {
                             "hostid": hostid,
                             "host": new_hostname,
                             "name": newhostname,
                             "tls_psk_identity": newhostname+ '_' + tls_psk_identity
                         "auth": auth,
                         "id": 1
                 }))
