#!/usr/bin/env python

from foreman import Foreman
from foreman.foreman import ForemanError

import yaml

f=Foreman('hhov-sat01.esailors.net', '443', 'tbade', 'tipp24')

data = {}
data['name'] = 'TestArch'

try:
    result = f.get_architecture(data=data)
    print yaml.safe_dump(result)
except ForemanError as e:
    print('Error: ' + e.message)
