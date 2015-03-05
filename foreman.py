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
        return None

    def get_architectures(self):
        return self.get_resource(resource='architectures')

    def get_architecture_by_id(self, id):
        return self.get_resource(resource='architecture/' + id)
        
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

    def get_domains(self):
        return self.get_resource(resource='domains')
    
    def get_domain_by_id(self, id):
        return self.get_resource(resouce='domain/' + id)
    
    def get_domain_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_domains())

    def set_domain(self, data):
        self.put_resource(resource='domains', data=data)
    
    def get_environments(self):
        return self.get_resource(resource='environments')
    
    def get_environment_by_id(self, id):
        return self.get_resource(resouce='environment/' + id)
    
    def get_environment_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_environments())

    def set_environment(self, name):
        self.put_resource(resource='environments', data={'environment': {'name':name}})

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
        return self.get_resource(resouce='ptable/' + id)
    
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
    
    def get_hosts(self):
        return self.get_resource(resource='hosts')
    
    def get_host_by_id(self, id):
        return self.get_resource(resouce='host/' + id)
    
    def get_host_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_hosts())

    def set_host(self, name, environment, domain, ip, mac, partition_table, medium, architecture, os, puppet_proxy, compute_resource, root_pass, location, organization):
        architecture_id = self.get_architecture_by_name(name=architecture).get('id')
        compute_resource_id = self.get_compute_resource_by_name(name=compute_resource).get('id')
        domain_id = self.get_domain_by_name(name=domain).get('id')
        environment_id = self.get_environment_by_name(name=environment).get('id')
        media_id = self.get_media_by_name(name=medium).get('id')
        partition_table_id = self.get_partition_table_by_name(name=partition_table).get('id')
        operatingsystem_id = self.get_operatingsystem_by_name(name=os).get('id')        
        puppet_proxy_id = self.get_smart_proxy_by_name(name=puppet_proxy).get('id')
        location_id = self.get_location_by_name(name=location).get('id')
        organization_id = self.get_organization_by_name(name=organization).get('id')
        data_dict = {'host' : {'name': name, 'environment_id': environment_id, 'domain_id': domain_id, 'ip': ip, 'mac': mac, 'ptable_id': partition_table_id, 'medium_id': media_id, 'architecture_id': architecture_id, 'operatingsystem_id': operatingsystem_id, 'puppet_proxy_id': puppet_proxy_id, 'compute_resource_id': compute_resource_id, 'root_pass': root_pass, 'location_id': location_id, 'organization_id': organization_id}}
        self.put_resource(resource='hosts', data=json.dumps(data_dict))
