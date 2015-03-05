'''
Created on 04.03.2015

@author: tkrah
'''

import json
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

FOREMAN_REQUEST_HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}
FOREMAN_API_VERSION = 'v2'

class Foreman:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.url = 'https://' + self.hostname + ':' + self.port + '/api/' + FOREMAN_API_VERSION

    def get_resource_url(self, resource_type, resoucre_id=None, action=None):
        url = self.url + '/' + resource_type
        if resoucre_id:
            url = url + '/' + resoucre_id
        if action:
            url = url + '/' + action
        return url

    def get_resource(self, resource_type, resource_id, action):
        r = requests.get(url=self.get_resource_url(resource_type=resource_type),
                         auth=(self.username, self.password),
                         verify=False)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        r.raise_for_status()

    def post_resource(self, resource_type, resource, data):
        payload = {}
        payload[resource] = data

        r = requests.post(url=self.get_resource_url(resource_type=resource_type) ,
                          data=json.dumps(payload),
                          headers=FOREMAN_REQUEST_HEADERS,
                          auth=(self.username, self.password),
                          verify=False)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        r.raise_for_status()

    def put_resource(self, resource_type, resource_id, data, action=None):
        r = requests.put(url=self.get_resource_url(resource_type=resource_type, resoucre_id=resource_id, action=action),
                         data=json.dumps(data),
                         headers=FOREMAN_REQUEST_HEADERS,
                         auth=(self.username, self.password),
                         verify=False)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        r.raise_for_status()

    def get_resource_by_name(self, name, list):
        for item in list:
            if item.get('name') == name:
                return item
        return {}

    def get_architectures(self):
        return self.get_resource(resource_type='architectures').get('results')

    def get_architecture_by_id(self, id):
        return self.get_resource(resource_type='architectures/' + id)
        
    def get_architecture_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_architectures())

    def set_architecture(self, data):
        return self.post_resource(resource_type='architectures', resource='architecture', data=data)

    def get_compute_resources(self):
        return self.get_resource(resource_type='compute_resources').get('results')

    def get_compute_resource_by_id(self, id):
        return self.get_resource(resource_type='compute_resources/' + id)
        
    def get_compute_resource_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_compute_resources())

    def set_compute_resource(self, data):
        return self.post_resource(resource_type='compute_resources', resource='compute_resource', data=data)

    def get_compute_profiles(self):
        return self.get_resource(resource_type='compute_profiles').get('results')

    def get_compute_profile_by_id(self, id):
        return self.get_resource(resource_type='compute_profiles/' + id)

    def get_compute_profile_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_compute_profiles())

    def set_compute_profile(self, data):
        return self.post_resource(resource_type='compute_profiles', resource='compute_profile', data=data)

    def get_domains(self):
        return self.get_resource(resource_type='domains').get('results')

    def get_domain_by_id(self, id):
        return self.get_resource(resouce_type='domains/' + id)

    def get_domain_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_domains())

    def set_domain(self, data):
        return self.post_resource(resource_type='domains', resource='domain', data=data)

    def get_environments(self):
        return self.get_resource(resource_type='environments').get('results')

    def get_environment_by_id(self, id):
        return self.get_resource(resouce_type='environments/' + id)

    def get_environment_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_environments())

    def set_environment(self, data):
        return self.post_resource(resource_type='environments', resource='environment', data=data)

    def get_hosts(self):
        return self.get_resource(resource_type='hosts').get('results')

    def get_host_by_id(self, id):
        return self.get_resource(resource_type='hosts/' + id)

    def get_host_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_hosts())

    def set_host(self, data):
        return self.post_resource(resource_type='hosts', resource='host', data=data)

    def set_host_power(self, host_id, action):
        return self.put_resource(resource_type='hosts', resource_id=host_id, action='power', data={'power_action': 'status', 'host': {}})

    def get_hostgroups(self):
        return self.get_resource(resource_type='hostgroups').get('results')

    def get_hostgroup_by_id(self, id):
        return self.get_resource(resouce_type='hostgroups/' + id)

    def get_hostgroup_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_hostgroups())

    def set_hostgroup(self, data):
        return self.post_resource(resource_type='hostgroups', resource='hostgroup', data=data)

    def get_locations(self):
        return self.get_resource(resource_type='locations').get('results')

    def get_location_by_id(self, id):
        return self.get_resource(resouce_type='locations/' + id)

    def get_location_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_locations())

    def set_location(self, data):
        return self.post_resource(resource_type='locations', resource='location', data=data)

    def get_medias(self):
        return self.get_resource(resource_type='media').get('results')

    def get_media_by_id(self, id):
        return self.get_resource(resouce_type='media/' + id)

    def get_media_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_medias())

    def set_media(self, data):
        return self.post_resource(resource_type='media', resource='medium', data=data)

    def get_organizations(self):
        return self.get_resource(resource_type='organizations').get('results')

    def get_organization_by_id(self, id):
        return self.get_resource(resouce_type='organizations/' + id)

    def get_organization_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_organizations())

    def set_organization(self, data):
        return self.post_resource(resource_type='organizations', resource='organization', data=data)

    def get_operatingsystems(self):
        return self.get_resource(resource_type='operatingsystems').get('results')

    def get_operatingsystem_by_id(self, id):
        return self.get_resource(resouce_type='operatingsystems/' + id)

    def get_operatingsystem_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_operatingsystems())

    def set_operatingsystem(self, data):
        return self.post_resource(resource_type='operatingsystems', resource='operatingsystem', data=data)

    def get_partition_tables(self):
        return self.get_resource(resource_type='ptables').get('results')

    def get_partition_table_by_id(self, id):
        return self.get_resource(resouce_type='ptables/' + id)

    def get_partition_table_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_partition_tables())

    def set_partition_table(self, data):
        return self.post_resource(resource_type='ptables', resource='ptable', data=data)

    def get_smart_proxies(self):
        return self.get_resource(resource_type='smart_proxies').get('results')

    def get_smart_proxy_by_id(self, id):
        return self.get_resource(resouce_type='smart_proxies/' + id)

    def get_smart_proxy_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_smart_proxies())

    def set_smart_proxy(self, data):
        return self.post_resource(resource_type='smart_proxies', resource='smart_proxy', data=data)

    def get_subnets(self):
        return self.get_resource(resource_type='subnets').get('results')

    def get_subnet_by_id(self, id):
        return self.get_resource(resouce_type='subnets/' + id)

    def get_subnet_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_subnets())

    def set_subnet(self, data):
        return self.post_resource(resource_type='subnets', resource='subnet', data=data)
