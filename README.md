# netbox-status-update
This script is a modified version of [jamesb2147/netbox-status-loader](https://github.com/jamesb2147/netbox-status-loader/). This script was created to my needs, although could be easily forked for others. <br><br>
This script updates the status of IP objects in [Netbox](http://github.com/netbox-community/netbox/). This script should be ran by cron on an automated schedule. 

## Installation
### Prerequisits
There are a few prerequisits required for this to work:
- A server running [Netbox](http://github.com/netbox-community/netbox/)
- Python3
- pip3
- An API token for Netbox

### Python Virtual Enviornment 
```
# installing Python3 venv
sudo pip3 install venv

# clone the git repo
git clone https://github.com/rml596/netbox-status-update.git

# creating/entering the virtual enviornment
cd netbox-status-update
python3 -m venv .
source bin/activate

# installing the python modules
sudo pip3 install -r requirements.txt
```

### Standard
```
# clone the git repo
git clone https://github.com/rml596/netbox-status-update.git
cd netbox-status-update

# installing the python modules
sudo pip3 install -r requirements.txt
```

### ENV File
This script runs from an `env.json` file. I have this script set such that live IPs are set `Active`, down IPs are set to `Deprecated`. The nameservers in `dnsList` should be servers that resolve your hostnames, so if you have split-horizon DNS, you need to use the servers that will resolve your Reverse DNS. If an object in the `env.json` file is not usable, the script will use default values for all. <br>
The `api_base_url` key is the url of your Netbox server API.
```json
{
"api_base_url":"https://FQDN/api/ipam",
"verifySSL": "False",
"apiToken" :"ABC123",
"dnsList": ["8.8.8.8","9.9.9.9"],
"deactiveIPid":3,
"activeIPid":1
}
```

## Usage
#### Modes
There are two modes in this script, `-i` or `--ip` and `-d` or `--dns`. <br>
The `-i` or `--ip` mode will update the status of IP addresses.<br>
The `-d` or `--dns` mode will update the FQDN entry in the IP object. This uses Reverse DNS entries, so if you don't have Reverse entries, this won't do anything.

##### Usage
To use `ip` or `dns` mode, add the argments to the end of the command. `python3 netbox-status-update -i`

### Python Virtual Enviornment
To use this in the Python Virtual Enviornment, you must enter the environment first, then run the code.
```
cd /PATH/TO/netbox-status-update

source bin/activate     #enters into the venv
sudo python3 netbox-status-update 

deactivate      #returns to regular shell
```

### Standard
```
cd /PATH/TO/netbox-status-update
sudo python3 netbox-status-update 
```


