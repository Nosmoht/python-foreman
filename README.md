[![Build Status](https://travis-ci.org/Nosmoht/python-foreman.png)](https://travis-ci.org/Nosmoht/python-foreman)
[![Coverage Status](https://coveralls.io/repos/Nosmoht/python-foreman/badge.svg)](https://coveralls.io/r/Nosmoht/python-foreman)
# python-foreman
Python Class to communicate with Foreman via [API] v2.

The use case behind this Class is to configure Foreman with Python. The class can be easily used in an Ansible module
so the complete infrastructure can be deployed with Ansible like done in my [Ansible Library].

# Requirements
Python-requests must be installed.

# Supported Functions
## Architectures
`get_architectures()`: Get a dict of all existing ones

`get_architecutre()`: Get a dict defining a specific architecture

`create_architecture()`: Create a new one

`delete_architecture()`: Delete existing architecture

## Compute Resources
`get_compute_resources()`: Get a dict of all existing ones

`create_compute_resource()`: Create a new one

`delete_compute_resource()` Delete existing one

## Compute Profiles
`get_compute_resources()`: Get a dict of all existing ones

`create_compute_resource()`: Create a new one

`delete_compute_resource()`: Delete existing one

## Domains
`get_domains()`: Get a dict of all existing ons

## Environments
`get_environments()`: Get a dict of all existing ones

## Hosts
`get_hosts()`: Get a dict of all existing ones

`create_host()`: Create a new one

`poweron_host()`: Power on

`poweroff_host()`: Power off

`delete_host()`: Delete host

## Hostsgroups
`get_hostgroups()`: Get a dict of all existing ones

## Locations
`get_locations()`: Get a dict of all existing ones

- Media: Get list of all existing and create a new one
- Operatingsystem: Get list of all existing and create a new one
- Organization: Get list of all existing and create a new one
- Partition Tables: Get list of all existing and create a new one
- Smart Proxies: Get list of all existing and create a new one

Update of any above listed resources not yet implemented !

# How to use
See test.py provides some examples.

```
$ bin/test.py -f foreman.example.com -p 443 -u admin -s p4ssw0rd -c test.yaml
```
or
```
$ bintest.py --foreman foreman.example.com --port 443 --username admin --secret p4ssw0rd --config test.yaml
```
# License

BSD

# Author
[Thomas Krahn]

[API]: www.theforeman.org/api_v2.html
[Ansible Library]: https://github.com/Nosmoht/ansible-library-foreman
[Thomas Krahn]: mailto:ntbc@gmx.net
