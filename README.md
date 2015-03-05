# python-foreman
Python Class to communicate with Foreman via API v2.

The use case behind this Class is to configure Foreman with Python. The class can be easily used in an Ansible module
so the complete infrastructure can be deployed with Ansible.

# Requirements
Python-requests must be installed.

# Supported Functions
- Architectures: Get list of all existing and create a new one
- Compute Resources: Get list of all existing and create a new one
- Compute Profiles: Get list of all existing and create a new one
- Domains: Get list of all existing and create a new one
- Environments: Get list of all existing and create a new one
- Hosts: Get list of all existing and create a new one
- Hostsgroups: Get list of all existing and create a new one
- Locations: Get list of all existing and create a new one
- Media: Get list of all existing and create a new one
- Operatingsystem: Get list of all existing and create a new one
- Organization: Get list of all existing and create a new one
- Partition Tables: Get list of all existing and create a new one
- Smart Proxies: Get list of all existing and create a new one

Update of any above listed resources not yet implemented !

# How to use
See test.py provides some examples.

```
$ test.py -f foreman.example.com -p 443 -u admin -s p4ssw0rd -c test.yaml
```
or
```
$ test.py --foreman foreman.example.com --port 443 --username admin --secret p4ssw0rd --config test.yaml
```
# License

BSD

# Author
Thomas Krahn
Mail: ntbc@gmx.net
