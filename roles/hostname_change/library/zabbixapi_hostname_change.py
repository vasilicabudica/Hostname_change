
#!usr/bin/env python
# Author, Vasilica Budica (vasilica.budica@solarwinds.com)

import json
import request

def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_url=str(required=True),
            username=str(required=True),
            password=str(required=True),
            oldhost=str(required=True),
            newhostname=str(required=True)
        ),
        supports_check_mode=True
    )

    module.exit_json(changed=True)

api_url = module.params['api_url']
username = module.params['username']
password = module.params['password']
oldhost = module.params['oldhost']
newhostname = module.params['newhostname']

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
tls_psk_identity = newhostname + '_' + json.loads(json.dumps(x.json()['result'][0]))['tls_psk_identity'].split('_')[1]

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
                             "tls_psk_identity": tls_psk_identity,
                         "auth": auth,
                         "id": 1
                 }))

from ansible.module_utils.basic import *
main()
