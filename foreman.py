'''
Created on 04.03.2015

@author: tkrah
'''

import json
import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth

FOREMAN_REQUEST_HEADERS = 'Content-Type:application/json'
FOREMAN_API_VERSION = 'v2'

class Foreman:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.url = 'https://' + self.hostname + ':' + self.port + '/api/' + FOREMAN_API_VERSION
        
    def get_resource(self, resource):
        try:
            r = requests.get(self.url + '/' + resource , auth=(self.username, self.password), verify=False)
            if r.status_code == 200:
                return json.loads(r.text)['results']
            r.raise_for_status(); 
        except:
            raise

    def put_resource(self, resource, data):
        try:
            r = requests.post(self.url + '/' + resource , data=json.dumps(data), auth=(self.username, self.password), verify=False)
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
        return self.get_resource(resource='architectures')

    def get_architecture_by_id(self, id):
        return self.get_resource(resource='architectures/' + id)
        
    def get_architecture_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_architectures())

    def set_architecture(self, data):
        self.put_resource(resource='architectures', data=data)

    def get_compute_resources(self):
        return self.get_resource(resource='compute_resources')

    def get_compute_resource_by_id(self, id):
        return self.get_resource(resource='compute_resources/' + id)
        
    def get_compute_resource_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_compute_resources())

    def set_compute_resource(self, data):
        self.put_resource(resource='compute_resources', data=data)

    def get_compute_profiles(self):
        return self.get_resource(resource='compute_profiles')

    def get_compute_profile_by_id(self, id):
        return self.get_resource(resource='compute_profiles/' + id)

    def get_compute_profile_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_compute_profiles())

    def set_compute_profile(self, data):
        self.put_resource(name='compute_profiles', data=data)

    def get_domains(self):
        return self.get_resource(resource='domains')

    def get_domain_by_id(self, id):
        return self.get_resource(resouce='domains/' + id)

    def get_domain_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_domains())

    def set_domain(self, data):
        self.put_resource(resource='domains', data=data)

    def get_environments(self):
        return self.get_resource(resource='environments')

    def get_environment_by_id(self, id):
        return self.get_resource(resouce='environments/' + id)

    def get_environment_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_environments())

    def set_environment(self, name):
        self.put_resource(resource='environments', data={'environment': {'name':name}})

    def get_hosts(self):
        return self.get_resource(resource='hosts')

    def get_host_by_id(self, id):
        return self.get_resource(resouce='hosts/' + id)

    def get_host_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_hosts())

    def set_host(self, data):
        self.put_resource(resource='hosts', data=data)

    def get_hostgroups(self):
        return self.get_resource(resource='hostgroups')

    def get_hostgroup_by_id(self, id):
        return self.get_resource(resouce='hostgroups/' + id)

    def get_hostgroup_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_hostgroups())

    def set_hostgroup(self, data):
        self.put_resource(resource='hostgroups', data=data)

    def get_locations(self):
        return self.get_resource(resource='locations')

    def get_location_by_id(self, id):
        return self.get_resource(resouce='locations/' + id)

    def get_location_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_locations())

    def set_location(self, data):
        self.put_resource(resource='locations', data=data)

    def get_medias(self):
        return self.get_resource(resource='media')

    def get_media_by_id(self, id):
        return self.get_resource(resouce='media/' + id)

    def get_media_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_medias())

    def set_media(self, data):
        self.put_resource(resource='media', data=data)

    def get_organizations(self):
        return self.get_resource(resource='organizations')

    def get_organization_by_id(self, id):
        return self.get_resource(resouce='organizations/' + id)

    def get_organization_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_organizations())

    def set_organization(self, data):
        self.put_resource(resource='organizations', data=data)

    def get_operatingsystems(self):
        return self.get_resource(resource='operatingsystems')

    def get_operatingsystem_by_id(self, id):
        return self.get_resource(resouce='operatingsystems/' + id)

    def get_operatingsystem_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_operatingsystems())

    def set_operatingsystem(self, data):
        self.put_resource(resource='operatingsystems', data=data)

    def get_partition_tables(self):
        return self.get_resource(resource='ptables')

    def get_partition_table_by_id(self, id):
        return self.get_resource(resouce='ptables/' + id)

    def get_partition_table_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_partition_tables())

    def set_partition_table(self, data):
        self.put_resource(resource='ptables', data=data)

    def get_smart_proxies(self):
        return self.get_resource(resource='smart_proxies')

    def get_smart_proxy_by_id(self, id):
        return self.get_resource(resouce='smart_proxies/' + id)

    def get_smart_proxy_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_smart_proxies())

    def set_smart_proxy(self, data):
        self.put_resource(resource='smart_proxies', data=data)
