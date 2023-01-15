![Logo](/images/netbox_giftwrap.png)
# netbox_giftwrap
Transform NetBox APIs into Business Ready formats

## Installing netbox_giftwrap
To install netbox_giftwrap there are a few simple steps:
#### Ubuntu Linux 
##### The following instructions are based on Windows WSL2 and Ubuntu however any flavour of Linux will work with possibly slightly different commands.

##### Confirm Python 3 is installed

#####
```console

$ python3 -V
Python 3.9.10

```

##### Create and activate a virtual environment

######
```console

$ sudo apt install python3-venv
$ python3 -m venv netbox_giftwrap
$ source netbox_giftwrap/bin/activate
(netbox_giftwrap)$

```
##### Install the netbox_giftwrap
```console

(netbox_giftwrap)$pip install netbox_giftwrap

```

##### Create an output folder
```console

(netbox_giftwrap)$mkdir output

```
### Windows

#### [Download Python](https://python.org)
#### Create and activate a virtual environment
#####
```console

C:\>python3 -m venv netbox_giftwrap
C:\>netbox_giftwrap\Scripts\activate
(netbox_giftwrap) C:\>

```
#### Install netbox_giftwrap
```console

(message_room)$pip install netbox_giftwrap

```

##### Create an output folder
```console

(netbox_giftwrap)$mkdir output

```
## Using the bot
### Run the bot as an interactive session
```console

(netbox_giftwrap)$ cd output
(netbox_giftwrap)$~/output/netbox_giftwrap.py

```

### The form questions:

##### Question 1 - NetBox URL:

Enter the URL of your NetBox instance (e.g. https://demo.netbox.dev):

This can be set as an environment variable

##### Question 2 - NetBox API Token: 

Enter your NetBox API Token - you can create / retrieve one from https://URL/user/api-tokens/

This can be set as an environment variable

#### Current API Covera

aggregates

asns

cables

circuit-terminations

circuit-types

circuits

cluster-groups

cluster-types

clusters

console-port-templates

console-ports

contact-assignments

contact-groups

contact-roles

contacts

device-bay-templates

device-bays

device-roles

device-types

devices

front-port-templates

front-ports

groups

interface-templates

interfaces

inventory-items

ip-addresses

ip-ranges

locations

manufacturers

module-bay-templates

module-bays

module-types

modules

platforms

power-feeds

power-outlet-templates

power-outlets

power-panels

power-port-templates

power-ports

prefixes

provider-networks

providers

rack-reservations

rack-roles

racks

rear-port-templates

rear-ports

regions

rirs

roles

route-targets

service-templates

services

site-groups

sites

status

tenant-groups

tenants

tokens

users

virtual-chassis

virtual-interfaces

virtual-machines

vlan-groups

vlans