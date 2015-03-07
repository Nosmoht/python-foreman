'''
Created on 04.03.2015

@author: tkrah
'''

import json
import requests
# from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

FOREMAN_REQUEST_HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}
FOREMAN_API_VERSION = 'v2'

class ForemanError(Exception):
    """ForemanError Class

    Simple class to handle exceptions while communicating to Foreman API
    """
    pass

class Foreman:
    """Foreman Class

    Communicate with Foreman via API v2

    """
    def __init__(self, hostname, port, username, password):
        """Init
        """
        self.__auth = (username, password)
        self.hostname = hostname
        self.port = port
        self.url = 'https://' + self.hostname + ':' + self.port + '/api/' + FOREMAN_API_VERSION

    def get_resource_url(self, resource_type, resource_id=None, component=None, component_id=None):
        """Create API URL path

        Args:
          resource_type (str): Name of resource to request
          resource_id (str): Resource identifier
          component (str): Component of a resource (e.g. images in /host/host01.example.com/images)
          component_id (str): Component identifier (e.g. nic01 in /host/host01.example.com/interfaces/nic1)
        """
        url = self.url + '/' + resource_type
        if resource_id:
            url = url + '/' + str(resource_id)
            if component:
                url = url + '/' + component
                if component_id:
                    url = url + '/' + str(component_id)
        return url

    def get_resource(self, resource_type, resource_id=None, component=None, component_id=None, data=None):
        """Execute a GET request agains Foreman API

        Args:
          resource_type (str): Name of resource to get
          component (str): Name of resource components to get
          component_id (str): Name of resource component to get
          data (dict): Dictionary to specify detailed data
        Returns:
          Dict
        """
        req = requests.get(url=self.get_resource_url(resource_type=resource_type,
                                                     resource_id=resource_id,
                                                     component=component,
                                                     component_id=component_id),
                           data=data,
                           auth=self.__auth,
                           verify=False)
        if req.status_code == 200:
            return json.loads(req.text)
        if req.status_code == 404 and resource_id:
            return {}
        raise ForemanError({'request_url': req.url,
                            'request_code': req.status_code,
                            'request': req.json()})

    def post_resource(self, resource_type, resource, data):
        """Execute a POST request agains Foreman API

        Args:
          resource_type (str): Name of resource type to post
          component (str): Name of resource to post
          data (dict): Dictionary containing component details
        Returns:
          Dict
        """
        req = requests.post(url=self.get_resource_url(resource_type=resource_type),
                            data=json.dumps({resource: data}),
                            headers=FOREMAN_REQUEST_HEADERS,
                            auth=self.__auth,
                            verify=False)
        if req.status_code in [200, 201]:
            return json.loads(req.text)
        raise ForemanError({'request_url': req.url,
                            'request_code': req.status_code,
                            'request_data': json.dumps(data),
                            'request': req.json()})

    def put_resource(self, resource_type, resource_id, data, action=None):
        """Execute a PUT request agains Foreman API

        Args:
          resource_type (str): Name of resource type to post
          resource_id (str): Resource identified
          data (dict): Dictionary of details
        Returns:
          Dict
        """
        req = requests.put(url=self.get_resource_url(resource_type=resource_type,
                                                     resource_id=resource_id,
                                                     component=action),
                           data=json.dumps(data),
                           headers=FOREMAN_REQUEST_HEADERS,
                           auth=self.__auth,
                           verify=False)
        if req.status_code == 200:
            return json.loads(req.text)
        raise ForemanError({'request_url': req.url,
                            'request_code': req.status_code,
                            'request_data': json.dumps(data),
                            'request': req.json()})

    def delete_resource(self, resource_type, data):
        """Execute a DELETE request agains Foreman API

        Args:
          resource_type (str): Name of resource type to post
          resource_id (str): Resource identified
        Returns:
          Dict
        """
        req = requests.delete(url=self.get_resource_url(resource_type=resource_type,
                                                        resource_id=str(data.get('id'))),
                              headers=FOREMAN_REQUEST_HEADERS,
                              auth=self.__auth,
                              verify=False)
        if req.status_code == 200:
            return json.loads(req.text)
        raise ForemanError({'request_url': req.url,
                            'request_code': req.status_code,
                            'request': req.json()})

    def get_resources(self, resource_type):
        return self.get_resource(resource_type=resource_type).get('results')

    def search_resource(self, resource_type, search_data={}):
        data = {}
        data['search'] = ''
        for key in search_data:
            if data['search']:
                data['search'] = data['search'] + ' AND '
            data['search'] = data['search'] + key + '==' + '"' + search_data[key] + '"'
        result = self.get_resource(resource_type=resource_type, data=data).get('results')
        if len(result) == 1:
            return result[0]
        return result

    def get_architectures(self):
        return self.get_resources(resource_type='architectures')

    def get_architecture(self, data):
        return self.search_resource(resource_type='architectures', search_data=data)

    def set_architecture(self, data):
        return self.post_resource(resource_type='architectures', resource='architecture', data=data)

    def create_architecture(self, data):
        return self.set_architecture(data=data)

    def delete_architecture(self, data):
        return self.delete_resource(resource_type='architectures', data=data)

    def get_compute_profiles(self):
        return self.get_resources(resource_type='compute_profiles')

    def get_compute_profile(self, data):
        return self.search_resource(resource_type='compute_profiles', search_data=data)

    def set_compute_profile(self, data):
        return self.post_resource(resource_type='compute_profiles', resource='compute_profile', data=data)

    def create_compute_profile(self, data):
        return self.set_compute_profile(data=data)

    def delete_compute_profile(self, data):
        return self.delete_resource(resource_type='compute_profiles', data=data)

    def get_compute_resources(self):
        return self.get_resources(resource_type='compute_resources')

    def get_compute_resource(self, data):
        return self.search_resource(resource_type='compute_resources', search_data=data)

    def set_compute_resource(self, data):
        return self.post_resource(resource_type='compute_resources', resource='compute_resource', data=data)

    def create_compute_resource(self, data):
        return self.set_compute_resource(data=data)

    def delete_compute_resource(self, data):
        return self.delete_resource(resource_type='compute_resources', data=data)

    def get_compute_resource_images(self, name):
        return self.get_compute_resource(name=name, component='images').get('results')

    def get_domains(self):
        return self.get_resources(resource_type='domains')

    def get_domain(self, data):
        return self.search_resource(resource_type='domains', search_data=data)

    def set_domain(self, data):
        return self.post_resource(resource_type='domains', resource='domain', data=data)

    def create_domain(self, data):
        return self.set_domain(data=data)

    def delete_domain(self, data):
        return self.delete_resource(resource_type='domains', data=data)

    def get_environments(self):
        return self.get_resources(resource_type='environments')

    def get_environment(self, data):
        return self.search_resource(resource_type='environments', search_data=data)

    def set_environment(self, data):
        return self.post_resource(resource_type='environments', resource='environment', data=data)

    def create_environment(self, data):
        return self.set_environment(data=data)

    def delete_environment(self, data):
        return self.delete_resource(resource_type='environments', data=data)

    def get_hosts(self):
        return self.get_resources(resource_type='hosts')

    def get_host(self, data):
        return self.search_resource(resource_type='hosts', search_data=data)

    def set_host(self, data):
        return self.post_resource(resource_type='hosts', resource='host', data=data)

    def create_host(self, data):
        return self.set_host(data=data)

    def delete_host(self, data):
        return self.delete_resource(resource_type='hosts', data=data)

    def get_host_power(self, host_id):
        return self.put_resource(resource_type='hosts',
                                 resource_id=host_id,
                                 action='power',
                                 data={'power_action': 'state', 'host': {}})

    def poweron_host(self, host_id):
        return self.set_host_power(host_id=host_id, action='start')

    def poweroff_host(self, host_id):
        return self.set_host_power(host_id=host_id, action='stop')

    def reboot_host(self, host_id):
        return self.set_host_power(host_id=host_id, action='reboot')

    def get_host_component(self, name, component, component_id=None):
        return self.get_host(name=name, component=component, component_id=component_id)

    def get_host_interfaces(self, name):
        return self.get_host_component(name=name,
                                       component='interfaces')

    def get_host_interface(self, name, interface_id):
        return self.get_host_component(name=name,
                                       component='interfaces',
                                       component_id=interface_id)

    def set_host_power(self, host_id, action):
        return self.put_resource(resource_type='hosts',
                                 resource_id=host_id,
                                 action='power',
                                 data={'power_action': action, 'host': {}})

    def get_hostgroups(self):
        return self.get_resources(resource_type='hostgroups')

    def get_hostgroup(self, data):
        return self.search_resource(resource_type='hostgroups', search_data=data)

    def set_hostgroup(self, data):
        return self.post_resource(resource_type='hostgroups', resource='hostgroup', data=data)

    def create_hostgroup(self, data):
        return self.set_hostgroup(data=data)

    def delete_hostgroup(self, data):
        return self.delete_resource(resource_type='hostgroups', data=data)

    def get_locations(self):
        return self.get_resources(resource_type='locations')

    def get_location(self, data):
        return self.search_resource(resource_type='locations', search_data=data)

    def set_location(self, data):
        return self.post_resource(resource_type='locations', resource='location', data=data)

    def create_location(self, data):
        return self.set_location(data=data)

    def get_media(self):
        return self.get_resources(resource_type='media')

    def get_medium(self, data):
        return self.search_resource(resource_type='media', search_data=data)

    def set_medium(self, data):
        return self.post_resource(resource_type='media', resource='medium', data=data)

    def create_medium(self, data):
        return self.set_medium(data=data)

    def delete_medium(self, data):
        return self.delete_resource(resource_type='media', data=data)

    def get_organizations(self):
        return self.get_resources(resource_type='organizations')

    def get_organization(self, data):
        return self.search_resource(resource_type='organizations', search_data=data)

    def set_organization(self, data):
        return self.post_resource(resource_type='organizations', resource='organization', data=data)

    def create_organization(self, data):
        return self.set_organization(data=data)

    def delete_organization(self, data):
        return self.delete_resource(resource_type='organizations', data=data)

    def get_operatingsystems(self):
        return self.get_resources(resource_type='operatingsystems')

    def get_operatingsystem(self, data):
        return self.search_resource(resource_type='operatingsystems', search_data=data)

    def set_operatingsystem(self, data):
        return self.post_resource(resource_type='operatingsystems', resource='operatingsystem', data=data)

    def create_operatingsystem(self, data):
        return self.set_operatingsystem(data=data)

    def delete_operatingsystem(self, data):
        return self.delete_resource(resource_type='operatingsystems', data=data)

    def get_partition_tables(self):
        return self.get_resources(resource_type='ptables')

    def get_partition_table(self, data):
        return self.search_resource(resource_type='ptables', search_data=data)

    def set_partition_table(self, data):
        return self.post_resource(resource_type='ptables', resource='ptable', data=data)

    def create_partition_table(self, data):
        return self.set_partition_table(data=data)

    def delete_partition_table(self, data):
        return self.delete_resource(resource_type='ptables', data=data)

    def get_smart_proxies(self):
        return self.get_resources(resource_type='smart_proxies')

    def get_smart_proxy(self, data):
        return self.search_resource(resource_type='smart_proxies', search_data=data)

    def set_smart_proxy(self, data):
        return self.post_resource(resource_type='smart_proxies', resource='smart_proxy', data=data)

    def create_smart_proxy(self, data):
        return self.set_smart_proxy(data=data)

    def delete_smart_proxy(self, data):
        return self.delete_resource(resource_type='smart_proxies', data=data)

    def get_subnets(self):
        return self.get_resources(resource_type='subnets')

    def get_subnet(self, data):
        return self.search_resource(resource_type='subnets', search_data=data)

    def set_subnet(self, data):
        return self.post_resource(resource_type='subnets', resource='subnet', data=data)

    def create_subnet(self, data):
        return self.set_subnet(data=data)

    def delete_subnet(self, data):
        return self.delete_resource(resource_type='subnets', data=data)
