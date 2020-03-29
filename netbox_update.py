# Robert Lynch
# Based off of https://github.com/jamesb2147/netbox-status-loader/
#
#               ****NOTE: my deployment has a custom field for IPs called `Ignore from Automatic Status Update?`, if this is True, the script ignores the IP and continues.



# IDEA:
# Unregistered IPs, then if they don't ping and the description is 'Unregistered IP', delete them



import json, requests, dns.resolver, sys
from ping3 import ping

from multiprocessing import Pool

# Trys to open env.json file
try:
    with open('env.json') as env:
        envars=json.load(env)
    api_base_url=envars['api_base_url']
    verifySSL=bool(envars['verifySSL'])
    apiToken=envars['apiToken']
    dnsList=envars['dnsList']
    deactiveIPid=envars['deactiveIPid']
    activeIPid=envars['activeIPid']
except:
    # hard code env-vars here, either edit in the ENV.json file or below
    #
    #
    api_base_url="http://localhost/api/ipam"
    verifySSL=False
    apiToken='abcdefghigklmnopqrstuvwxyz123456790'
    dnsList=['192.168.1.1', '192.168.2.1']
    deactiveIPid=3
    activeIPid=1

# Replaces token with the valid header --> {'Authorization':'Token abcdefghigklmnopqrstuvwxyz123456790'}
apiToken={'Authorization':'Token {}'.format(apiToken)}

dnsServers=dns.resolver.Resolver()
dnsServers.nameservers=dnsList

apiSession=requests.Session()
#if verifySSL:
    #apiSession.verify=False

def checkStatus(address):
    ip=address['address'].split("/")[0]
    if 'Ignore from Automatic Status Update?' in address['custom_fields'] and address['custom_fields']['Ignore from Automatic Status Update?']==True:
        return("{}: ignored".format(ip))
    else:
        if ping(ip,timeout=10) is None:
            status=deactiveIPid
        else:
            status=activeIPid

        if address['status']['id']==status:
            return
        else: 
            address['status']=status
            url="{}/ip-addresses/{}/".format(api_base_url,address['id'])
            update={'id':address['id'],'status':status}
            if apiSession.patch(url,headers=apiToken, json=update).status_code==200:
                return("{}: updated successful".format(ip))
            else:
                return("{}: update failed".format(ip))

def checkDNS(address):
    ip = (address['address'].split("/"))[0]
    reverseQuery='.'.join(reversed(ip.split("."))) + ".in-addr.arpa"
    try:
        answer=dnsServers.query(reverseQuery, "PTR").response.answer
        for i in answer:
            for j in i.items:
                answer=j.to_text().rstrip('.')
    except:
        return
    if address['dns_name']=="" and answer!=None:
        url="{}/ip-addresses/{}/".format(api_base_url,address['id'])
        update={'id':address['id'],'dns_name':answer}
        if apiSession.patch(url,headers=apiToken, json=update).status_code==200:
            return("{}: updated successful".format(ip))
        else:
            return("{}: update failed".format(ip))
    elif address['dns_name']!="" and address['dns_name']!=answer and answer!=None:
        url="{}/ip-addresses/{}/".format(api_base_url,address['id'])
        address['custom_fields']['FQDN']=answer
        update={'id':address['id'],'custom_fields': address['custom_fields']}
        if apiSession.patch(url,headers=apiToken, json=update).status_code==200:
            return("{}: updated successful".format(ip))
        else:
            return("{}: update failed".format(ip))
    else:
        return
        

def getIPaddresses():
    return(json.loads(apiSession.get(api_base_url+"/ip-addresses?limit=0", headers=apiToken).text))

def getPrefixes():
    return(json.loads(apiSession.get(api_base_url+"/prefixes?limit=0", headers=apiToken).text))



if __name__=='__main__':
    pool = Pool(processes=45)
    if sys.argv[1]=='ip':
        result = pool.map(checkStatus, getIPaddresses()['results'])
    elif sys.argv[1]=='dns':
        result = pool.map(checkDNS, getIPaddresses()['results'])
    else:
        print("Specify OPTIONS \'ip\' or \'dns\'")
        sys.exit()
    for index in result:
            if index!=None:
                print(index)