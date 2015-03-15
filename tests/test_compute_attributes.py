#!/usr/bin/env python

from foreman import Foreman
from foreman.foreman import ForemanError

import yaml

f=Foreman('hhov-sat01.esailors.net', '443', 'tbade', 'tipp24')

compute_resource = f.get_compute_resource(data={'name': 'ZOE_VSphere_SpitalerHof'})
print('------------- Resource ------------- ')
print yaml.safe_dump(compute_resource, default_flow_style=False)

compute_attributes = compute_resource.get('compute_attributes', None)
print('------------- Attributes ------------- ')
print yaml.safe_dump(compute_attributes, default_flow_style = False)

compute_profile = f.get_compute_profile(data={'name': '1-Small'})
print('------------- Profile ------------- ')
print yaml.safe_dump(compute_profile, default_flow_style=False)

print('------------- Final ------------- ')
try:
    result = f.get_compute_attributes(data={'compute_resource': 'ZOE_VSphere_SpitalerHof', 'compute_profile': '2-Medium'})
    print yaml.safe_dump(result)
except ForemanError as e:
    print('Error: ' + e.message)
