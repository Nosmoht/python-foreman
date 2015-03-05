'''
Created on 04.03.2015

@author: tkrah
'''

import json
import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth

FOREMAN_REQUEST_HEADERS = {'content-type': 'application/json'}
FOREMAN_API_VERSION = 'v2'

class Foreman:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.url = 'https://' + self.hostname + ':' + self.port + '/api/' + FOREMAN_API_VERSION
        
    def get_resource(self, resource_type):
        try:
            r = requests.get(url=self.url + '/' + resource_type ,
                             auth=(self.username, self.password),
                             verify=False)
            if r.status_code == 200:
                return json.loads(r.text)['results']
            r.raise_for_status(); 
        except:
            raise

    def put_resource(self, resource_type, resource, data):
        try:
            payload = {}
            payload[resource] = data

            r = requests.post(url=self.url + '/' + resource_type ,
                              data=json.dumps(payload),
                              headers=FOREMAN_REQUEST_HEADERS,
                              auth=(self.username, self.password),
                              verify=False)
            if r.status_code == 200:
                return json.loads(r.text)            
            r.raise_for_status()
        except:
            raise

    def get_resource_by_name(self, name, list):
        for item in list:
            if item.get('name') == name:
                return item
        return {}

    def get_architectures(self):
        return self.get_resource(resource_type='architectures')

    def get_architecture_by_id(self, id):
        return self.get_resource(resource_type='architectures/' + id)
        
    def get_architecture_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_architectures())

    def set_architecture(self, data):
        self.put_resource(resource_type='architectures', resource='architecture', data=data)

    def get_compute_resources(self):
        return self.get_resource(resource_type='compute_resources')

    def get_compute_resource_by_id(self, id):
        return self.get_resource(resource_type='compute_resources/' + id)
        
    def get_compute_resource_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_compute_resources())

    def set_compute_resource(self, data):
        self.put_resource(resource_type='compute_resources', resource='compute_resource', data=data)

    def get_compute_profiles(self):
        return self.get_resource(resource_type='compute_profiles')

    def get_compute_profile_by_id(self, id):
        return self.get_resource(resource_type='compute_profiles/' + id)

    def get_compute_profile_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_compute_profiles())

    def set_compute_profile(self, data):
        self.put_resource(resource_type='compute_profiles', resource='compute_profile', data=data)

    def get_domains(self):
        return self.get_resource(resource_type='domains')

    def get_domain_by_id(self, id):
        return self.get_resource(resouce_type='domains/' + id)

    def get_domain_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_domains())

    def set_domain(self, data):
        self.put_resource(resource_type='domains', resource='domain', data=data)

    def get_environments(self):
        return self.get_resource(resource_type='environments')

    def get_environment_by_id(self, id):
        return self.get_resource(resouce_type='environments/' + id)

    def get_environment_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_environments())

    def set_environment(self, data):
        self.put_resource(resource_type='environments', resource='environment', data=data)

    def get_hosts(self):
        return self.get_resource(resource_type='hosts')

    def get_host_by_id(self, id):
        return self.get_resource(resouce_type='hosts/' + id)

    def get_host_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_hosts())

    def set_host(self, data):
        self.put_resource(resource_type='hosts', resource='host', data=data)

    def get_hostgroups(self):
        return self.get_resource(resource_type='hostgroups')

    def get_hostgroup_by_id(self, id):
        return self.get_resource(resouce_type='hostgroups/' + id)

    def get_hostgroup_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_hostgroups())

    def set_hostgroup(self, data):
        self.put_resource(resource_type='hostgroups', resource='hostgroup', data=data)

    def get_locations(self):
        return self.get_resource(resource_type='locations')

    def get_location_by_id(self, id):
        return self.get_resource(resouce_type='locations/' + id)

    def get_location_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_locations())

    def set_location(self, data):
        self.put_resource(resource_type='locations', resource='location', data=data)

    def get_medias(self):
        return self.get_resource(resource_type='media')

    def get_media_by_id(self, id):
        return self.get_resource(resouce_type='media/' + id)

    def get_media_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_medias())

    def set_media(self, data):
        self.put_resource(resource_type='media', resource='medium', data=data)

    def get_organizations(self):
        return self.get_resource(resource_type='organizations')

    def get_organization_by_id(self, id):
        return self.get_resource(resouce_type='organizations/' + id)

    def get_organization_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_organizations())

    def set_organization(self, data):
        self.put_resource(resource_type='organizations', resource='organization', data=data)

    def get_operatingsystems(self):
        return self.get_resource(resource_type='operatingsystems')

    def get_operatingsystem_by_id(self, id):
        return self.get_resource(resouce_type='operatingsystems/' + id)

    def get_operatingsystem_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_operatingsystems())

    def set_operatingsystem(self, data):
        self.put_resource(resource_type='operatingsystems', resource='operatingsystem', data=data)

    def get_partition_tables(self):
        return self.get_resource(resource_type='ptables')

    def get_partition_table_by_id(self, id):
        return self.get_resource(resouce_type='ptables/' + id)

    def get_partition_table_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_partition_tables())

    def set_partition_table(self, data):
        self.put_resource(resource_type='ptables', resource='ptable', data=data)

    def get_smart_proxies(self):
        return self.get_resource(resource_type='smart_proxies')

    def get_smart_proxy_by_id(self, id):
        return self.get_resource(resouce_type='smart_proxies/' + id)

    def get_smart_proxy_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_smart_proxies())

    def set_smart_proxy(self, data):
        self.put_resource(resource_type='smart_proxies', resource='smart_proxy', data=data)

    def get_subnets(self):
        return self.get_resource(resource_type='subnets')

    def get_subnet_by_id(self, id):
        return self.get_resource(resouce_type='subnets/' + id)

    def get_subnet_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_subnets())

    def set_subnet(self, data):
        self.put_resource(resource_type='subnets', resource='subnet', data=data)
