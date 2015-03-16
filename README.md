[![Build Status](https://travis-ci.org/Nosmoht/python-foreman.png)](https://travis-ci.org/Nosmoht/python-foreman)
[![Coverage Status](https://coveralls.io/repos/Nosmoht/python-foreman/badge.svg)](https://coveralls.io/r/Nosmoht/python-foreman)
# python-foreman
Python Class to communicate with Foreman via [API] v2.

The use case behind this Class is to configure Foreman with Python. The class can be easily used in an Ansible module
so the complete infrastructure can be deployed with Ansible like done in my [Ansible Library].

# Documentation
Will come soon.

# Requirements
[Python-requests] is required but will be installed by setup.py.

# Installation
To install the latest version with pip from Github:
```
pip install https://github.com/Nosmoht/python-foreman.git#master
```

To install with python:
```
git clone https://github.com/Nosmoht/python-foreman.git
cd python-foreman
python setup.py install
```


# How to use

See test.py for examples.

```
$ bin/test.py -f foreman.example.com -p 443 -u admin -s p4ssw0rd -c test.yaml
```
or
```
$ bin/test.py --foreman foreman.example.com --port 443 --username admin --secret p4ssw0rd --config test.yaml
```

# License

BSD

# Author
[Thomas Krahn]

[API]: www.theforeman.org/api_v2.html
[Ansible Library]: https://github.com/Nosmoht/ansible-library-foreman
[Thomas Krahn]: mailto:ntbc@gmx.net
[Python-requests]: https://github.com/kennethreitz/requests
