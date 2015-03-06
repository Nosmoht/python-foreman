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

class ForemanError(Exception):
    pass

class Foreman:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.url = 'https://' + self.hostname + ':' + self.port + '/api/' + FOREMAN_API_VERSION

    def get_resource_url(self, resource_type, resource_id=None, component=None, component_id=None):
        url = self.url + '/' + resource_type
        if resource_id:
            url = url + '/' + resource_id
        if component:
            url = url + '/' + component
        if component_id:
            url = url + '/' + component_id
        return url

    def get_resource(self, resource_type, resource_id=None, component=None):
        r = requests.get(url=self.get_resource_url(resource_type=resource_type, resource_id=resource_id, component=component),
                         auth=(self.username, self.password),
                         verify=False)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        raise ForemanError({'request_url': r.url, 'request_code': r.status_code, 'request': r.json() })

    def post_resource(self, resource_type, resource, data):
        r = requests.post(url=self.get_resource_url(resource_type=resource_type) ,
                          data=json.dumps({resource: data}),
                          headers=FOREMAN_REQUEST_HEADERS,
                          auth=(self.username, self.password),
                          verify=False)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        raise ForemanError({'request_url': r.url, 'request_code': r.status_code, 'request_data': json.dumps(data), 'request': r.json() })

    def put_resource(self, resource_type, resource_id, data, action=None):
        r = requests.put(url=self.get_resource_url(resource_type=resource_type, resource_id=resource_id, component=action),
                         data=json.dumps(data),
                         headers=FOREMAN_REQUEST_HEADERS,
                         auth=(self.username, self.password),
                         verify=False)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        raise ForemanError({'request_url': r.url, 'request_code': r.status_code, 'request_data': json.dumps(data), 'request': r.json() })

    def delete_resource(self, resource_type, resource_id):
        r = requests.delete(url=self.get_resource_url(resource_type=resource_type, resource_id=resource_id),
                            headers=FOREMAN_REQUEST_HEADERS,
                            auth=(self.username, self.password),
                            verify=False)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        raise ForemanError({'request_url': r.url, 'request_code': r.status_code, 'request': r.json() })

    def get_resources(self, resource_type):
        return self.get_resource(resource_type=resource_type).get('results')

    def get_resource_by_name(self, name, list):
        for item in list:
            if item.get('name') == name:
                return item
        return {}

    def get_architectures(self):
        return self.get_resources(resource_type='architectures')

    def get_architecture_by_id(self, id):
        return self.get_resource(resource_type='architectures', resource_id=id)
        
    def get_architecture_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_architectures())

    def set_architecture(self, data):
        return self.post_resource(resource_type='architectures', resource='architecture', data=data)

    def create_architecture(self, name):
        return self.set_architecture(data={'name': name})

    def delete_architecture(self, name):
        return self.delete_resource(resource_type='architectures', resource_id=name)

    def get_compute_resources(self):
        return self.get_resources(resource_type='compute_resources')

    def get_compute_resource_by_id(self, id, component=None):
        return self.get_resource(resource_type='compute_resources', resource_id=id, component=component)
        
    def get_compute_resource_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_compute_resources())

    def set_compute_resource(self, data):
        return self.post_resource(resource_type='compute_resources', resource='compute_resource', data=data)

    def create_compute_resource(self, name, user, password, provider, server, url):
        return self.set_compute_resource(data={'name': name, 'user': user, 'password': password, 'provider':provider, 'server': server, 'url': url})

    def delete_compute_resource(self, name):
        return self.delete_resource(resource_type='compute_resources', resource_id=name)

    def get_compute_resource_images(self, compute_resource_id):
        return self.get_compute_resource_by_id(id=compute_resource_id, component='images').get('results')

    def get_compute_profiles(self):
        return self.get_resources(resource_type='compute_profiles')

    def get_compute_profile_by_id(self, id):
        return self.get_resource(resource_type='compute_profiles', resource_id=id)

    def get_compute_profile_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_compute_profiles())

    def set_compute_profile(self, data):
        return self.post_resource(resource_type='compute_profiles', resource='compute_profile', data=data)

    def create_compute_profile(self, name):
        return self.set_compute_profile(data={'name': name})

    def delete_compute_profile(self, name):
        return self.delete_resource(resource_type='compute_profiles', resource_id=name)

    def get_domains(self):
        return self.get_resources(resource_type='domains')

    def get_domain_by_id(self, id):
        return self.get_resource(resouce_type='domains', resource_id=id)

    def get_domain_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_domains())

    def set_domain(self, data):
        return self.post_resource(resource_type='domains', resource='domain', data=data)

    def create_domain(self, name):
        return self.set_domain(data={'name': name})

    def delete_domain(self, name):
        return self.delete_resource(resource_type='domains', resource_id=name)

    def get_environments(self):
        return self.get_resources(resource_type='environments')

    def get_environment_by_id(self, id):
        return self.get_resource(resouce_type='environments', resource_id=id)

    def get_environment_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_environments())

    def set_environment(self, data):
        return self.post_resource(resource_type='environments', resource='environment', data=data)

    def get_hosts(self):
        return self.get_resources(resource_type='hosts')

    def get_host_by_id(self, id, component=None, component_id=None):
        return self.get_resource(resource_type='hosts', resource_id=id, component=component)

    def get_host_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_hosts())

    def set_host(self, data):
        return self.post_resource(resource_type='hosts', resource='host', data=data)

    def get_host_component(self, id, component, component_id):
        return self.get_host_by_id(id, component=component, component_id=component_id)

    def get_host_interfaces(self, host_id):
        return self.get_host_component(id=host_id, component='interfaces')

    def get_host_interface(self, host_id, interface_id):
        return self.get_host_component(id=host_id, component='interfaces', component_id=interface_id)

    def create_host(self, name, architecture, compute_profile, compute_resource, domain, environment, hostgroup, location, medium, operatingsystem, organization):
        data = {}
        data['architecture_id'] = self.get_architecture_by_name(name=architecture).get('id')
        data['name'] = name
        data['compute_profile_id'] = self.get_compute_profile_by_name(name=compute_profile).get('id')
        data['compute_resource_id'] = self.get_compute_resource_by_name(name=compute_resource).get('id')
        data['domain_id'] = self.get_domain_by_name(name=domain).get('id')
        data['environment_id'] = self.get_environment_by_name(name=environment).get('id')
        data['hostgroup_id'] = self.get_hostgroup_by_name(name=hostgroup).get('id')
        data['location_id'] = self.get_location_by_name(name=location).get('id')
        data['medium_id'] = self.get_medium_by_name(name=medium).get('id')
        data['organization_id'] = self.get_organization_by_name(name=organization).get('id')
        data['operatingsystem_id'] = self.get_operatingsystem_by_name(name=operatingsystem).get('id')
        return self.set_host(data=data)

    def set_host_power(self, host_id, action):
        return self.put_resource(resource_type='hosts', resource_id=host_id, action='power', data={'power_action': action, 'host': {}})

    def get_host_power(self, host_id):
        return self.put_resource(resource_type='hosts', resource_id=host_id, action='power', data={'power_action': 'state', 'host': {}})

    def poweron_host(self, host_id):
        return self.set_host_power(host_id=host_id, action='start')

    def poweroff_host(self, host_id):
        return self.set_host_power(host_id=host_id, action='stop')

    def reboot_host(self, host_id):
        return self.set_host_power(host_id=host_id, action='reboot')

    def get_hostgroups(self):
        return self.get_resources(resource_type='hostgroups')

    def get_hostgroup_by_id(self, id):
        return self.get_resource(resouce_type='hostgroups', resource_id=id)

    def get_hostgroup_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_hostgroups())

    def set_hostgroup(self, data):
        return self.post_resource(resource_type='hostgroups', resource='hostgroup', data=data)

    def create_hostgroup(self, name, architecture=None, domain=None, environment=None, medium=None,
                         operatingsystem=None, partition_table=None, smart_proxy=None, subnet=None):
        data = {}
        data['name'] = name
        if architecture:
            data['architecture_id'] = self.get_architecture_by_name(name=architecture).get('id')
        if domain:
            data['domain_id'] = self.get_domain_by_name(name=domain).get('id')
        if environment:
            data['environment_id'] = self.get_environment_by_name(name=environment).get('id')
        if medium:
            data['medium_id'] = self.get_medium_by_name(name=medium)
        if operatingsystem:
            data['operatingsystem_id'] = self.get_operatingsystem_by_name(name=operatingsystem).get('id')
        if partition_table:
            data['ptable_id'] = self.get_partition_table_by_name(name=partition_table).get('id')
        if smart_proxy:
            data['puppet_proxy_id'] = self.get_smart_proxy_by_name(name=smart_proxy).get('id')
        if subnet:
            data['subnet_id'] = self.get_subnet_by_name(name=subnet).get('id')
        return self.set_hostgroup(data=data)

    def delete_hostgroup(self, name):
        return self.delete_resource(resource_type='hostgroups', resource_id=name)

    def get_locations(self):
        return self.get_resources(resource_type='locations')

    def get_location_by_id(self, id):
        return self.get_resource(resouce_type='locations', resource_id=id)

    def get_location_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_locations())

    def set_location(self, data):
        return self.post_resource(resource_type='locations', resource='location', data=data)

    def get_media(self):
        return self.get_resources(resource_type='media')

    def get_medium_by_id(self, id):
        return self.get_resource(resouce_type='media', resource_id=id)

    def get_medium_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_media())

    def set_medium(self, data):
        return self.post_resource(resource_type='media', resource='medium', data=data)

    def get_organizations(self):
        return self.get_resources(resource_type='organizations')

    def get_organization_by_id(self, id):
        return self.get_resource(resouce_type='organizations', resource_id=id)

    def get_organization_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_organizations())

    def set_organization(self, data):
        return self.post_resource(resource_type='organizations', resource='organization', data=data)

    def get_operatingsystems(self):
        return self.get_resources(resource_type='operatingsystems')

    def get_operatingsystem_by_id(self, id):
        return self.get_resource(resouce_type='operatingsystems', resource_id=id)

    def get_operatingsystem_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_operatingsystems())

    def set_operatingsystem(self, data):
        return self.post_resource(resource_type='operatingsystems', resource='operatingsystem', data=data)

    def get_partition_tables(self):
        return self.get_resources(resource_type='ptables')

    def get_partition_table_by_id(self, id):
        return self.get_resource(resouce_type='ptables', resource_id=id)

    def get_partition_table_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_partition_tables())

    def set_partition_table(self, data):
        return self.post_resource(resource_type='ptables', resource='ptable', data=data)

    def get_smart_proxies(self):
        return self.get_resources(resource_type='smart_proxies')

    def get_smart_proxy_by_id(self, id):
        return self.get_resource(resouce_type='smart_proxies', resource_id=id)

    def get_smart_proxy_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_smart_proxies())

    def set_smart_proxy(self, data):
        return self.post_resource(resource_type='smart_proxies', resource='smart_proxy', data=data)

    def get_subnets(self):
        return self.get_resources(resource_type='subnets')

    def get_subnet_by_id(self, id):
        return self.get_resource(resouce_type='subnets', resource_id=id)

    def get_subnet_by_name(self, name):
        return self.get_resource_by_name(name=name, list=self.get_subnets())

    def set_subnet(self, data):
        return self.post_resource(resource_type='subnets', resource='subnet', data=data)
