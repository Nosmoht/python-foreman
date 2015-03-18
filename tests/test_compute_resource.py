#!/usr/bin/env python

from foreman import Foreman
from foreman.foreman import ForemanError

import yaml

f=Foreman('hhov-sat01.esailors.net', '443', 'tbade', 'tipp24')

data = {}
data['name'] = "TestComputeResource"

try:
    result = f.get_compute_resource(data=data)
    print yaml.safe_dump(result)

    if not result:
#{"name": "TestComputeResource", "password": "secret", "provider": "VMWare", "server": "compute01.example.com", "state": "present", "url": "compute01.example.com", "user": "ansible"}

      data['password'] = "secret"
      data["provider"] = "VMWare"
      data["datacenter"] = "dc01"
      data["server"] = "compute01.example.com"
      data["url"] = "compute01.example.com"
      data["user"] = "ansible"
    
      f.create_compute_resource(data=data)
except ForemanError as e:
    print("Error(" + str(e.status_code) + "): " + e.message)
