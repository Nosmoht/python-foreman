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
            url = url + '/' + resource_id
            if component:
                url = url + '/' + component
                if component_id:
                    url = url + '/' + component_id
        return url

    def get_resource(self, resource_type, resource_id=None, component=None, component_id=None):
        """Execute a GET request agains Foreman API

        Args:
          resource_type (str): Name of resource to get
          component (str): Name of resource components to get
          component_id (str): Name of resource component to get
        Returns:
          Dict
        """
        req = requests.get(url=self.get_resource_url(resource_type=resource_type,
                                                     resource_id=resource_id,
                                                     component=component,
                                                     component_id=component_id),
                           auth=self.__auth,
                           verify=False)
        if req.status_code == 200:
            return json.loads(req.text)
        if req.status_code == 404 and component:
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
        if req.status_code == 200:
            return json.loads(req.text)
        raise ForemanError({'request_url': req.url,
                            'request_code': req.status_code,
                            'request_data': json.dumps(data),
                            'request': req.json()})

    def put_resource(self, resource_type, resource_id, data, action=None):
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

    def delete_resource(self, resource_type, resource_id):
        req = requests.delete(url=self.get_resource_url(resource_type=resource_type,
                                                        resource_id=resource_id),
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

    def get_architectures(self):
        return self.get_resources(resource_type='architectures')

    def get_architecture(self, name):
        return self.get_resource(resource_type='architectures', resource_id=name)

    def set_architecture(self, data):
        return self.post_resource(resource_type='architectures',
                                  resource='architecture',
                                  data=data)

    def create_architecture(self, name):
        return self.set_architecture(data={'name': name})

    def delete_architecture(self, name):
        return self.delete_resource(resource_type='architectures',
                                    resource_id=name)

    def get_compute_resources(self):
        return self.get_resources(resource_type='compute_resources')

    def get_compute_resource(self, name, component=None):
        return self.get_resource(resource_type='compute_resources',
                                 resource_id=name,
                                 component=component)

    def set_compute_resource(self, data):
        return self.post_resource(resource_type='compute_resources',
                                  resource='compute_resource',
                                  data=data)

    def create_compute_resource(self, name, user, password, provider, server, url):
        return self.set_compute_resource(data={'name': name,
                                               'user': user,
                                               'password': password,
                                               'provider':provider,
                                               'server': server,
                                               'url': url})

    def delete_compute_resource(self, name):
        return self.delete_resource(resource_type='compute_resources',
                                    resource_id=name)

    def get_compute_resource_images(self, name):
        return self.get_compute_resource(name=name,
                                         component='images').get('results')

    def get_compute_profiles(self):
        return self.get_resources(resource_type='compute_profiles')

    def get_compute_profile(self, name):
        return self.get_resource(resource_type='compute_profiles',
                                 resource_id=name)

    def set_compute_profile(self, data):
        return self.post_resource(resource_type='compute_profiles',
                                  resource='compute_profile',
                                  data=data)

    def create_compute_profile(self, name):
        return self.set_compute_profile(data={'name': name})

    def delete_compute_profile(self, name):
        return self.delete_resource(resource_type='compute_profiles',
                                    resource_id=name)

    def get_domains(self):
        return self.get_resources(resource_type='domains')

    def get_domain(self, name):
        return self.get_resource(resource_type='domains',
                                 resource_id=name)

    def set_domain(self, data):
        return self.post_resource(resource_type='domains',
                                  resource='domain',
                                  data=data)

    def create_domain(self, name):
        return self.set_domain(data={'name': name})

    def delete_domain(self, name):
        return self.delete_resource(resource_type='domains',
                                    resource_id=name)

    def get_environments(self):
        return self.get_resources(resource_type='environments')

    def get_environment(self, name):
        return self.get_resource(resource_type='environments',
                                 resource_id=name)

    def set_environment(self, data):
        return self.post_resource(resource_type='environments',
                                  resource='environment',
                                  data=data)

    def create_environment(self, name):
        return self.set_environment(data={'name': name})

    def delete_environment(self, name):
        return self.delete_resource(resource_type='environments',
                                    resource_id=name)

    def get_hosts(self):
        return self.get_resources(resource_type='hosts')

    def get_host(self, name, component=None, component_id=None):
        return self.get_resource(resource_type='hosts',
                                 resource_id=name,
                                 component=component,
                                 component_id=component_id)

    def set_host(self, data):
        return self.post_resource(resource_type='hosts',
                                  resource='host',
                                  data=data)

    def get_host_component(self, name, component, component_id=None):
        return self.get_host(name=name,
                             component=component,
                             component_id=component_id)

    def get_host_interfaces(self, name):
        return self.get_host_component(name=name,
                                       component='interfaces')

    def get_host_interface(self, name, interface_id):
        return self.get_host_component(name=name,
                                       component='interfaces',
                                       component_id=interface_id)

    def create_host(self, name, architecture, compute_profile, compute_resource,
                    domain, environment, hostgroup, location, medium, operatingsystem,
                    organization):
        data = {}
        data['architecture_id'] = self.get_architecture(name=architecture).get('id')
        data['name'] = name
        data['compute_profile_id'] = self.get_compute_profile(name=compute_profile).get('id')
        data['compute_resource_id'] = self.get_compute_resource(name=compute_resource).get('id')
        data['domain_id'] = self.get_domain(name=domain).get('id')
        data['environment_id'] = self.get_environment(name=environment).get('id')
        data['hostgroup_id'] = self.get_hostgroup(name=hostgroup).get('id')
        data['location_id'] = self.get_location(name=location).get('id')
        data['medium_id'] = self.get_medium(name=medium).get('id')
        data['organization_id'] = self.get_organization(name=organization).get('id')
        data['operatingsystem_id'] = self.get_operatingsystem(name=operatingsystem).get('id')
        return self.set_host(data=data)

    def set_host_power(self, name, action):
        return self.put_resource(resource_type='hosts',
                                 resource_id=name,
                                 action='power',
                                 data={'power_action': action, 'host': {}})

    def get_host_power(self, name):
        return self.put_resource(resource_type='hosts',
                                 resource_id=name,
                                 action='power',
                                 data={'power_action': 'state', 'host': {}})

    def poweron_host(self, name):
        return self.set_host_power(name=name, action='start')

    def poweroff_host(self, name):
        return self.set_host_power(name=name, action='stop')

    def reboot_host(self, name):
        return self.set_host_power(name=name, action='reboot')

    def get_hostgroups(self):
        return self.get_resources(resource_type='hostgroups')

    def get_hostgroup(self, name):
        return self.get_resource(resource_type='hostgroups', resource_id=name)

    def set_hostgroup(self, data):
        return self.post_resource(resource_type='hostgroups',
                                  resource='hostgroup',
                                  data=data)

    def create_hostgroup(self, name, architecture=None, domain=None,
                         environment=None, medium=None, operatingsystem=None,
                         partition_table=None, smart_proxy=None, subnet=None):
        data = {}
        data['name'] = name
        if architecture:
            data['architecture_id'] = self.get_architecture(name=architecture).get('id')
        if domain:
            data['domain_id'] = self.get_domain(name=domain).get('id')
        if environment:
            data['environment_id'] = self.get_environment(name=environment).get('id')
        if medium:
            data['medium_id'] = self.get_medium(name=medium)
        if operatingsystem:
            data['operatingsystem_id'] = self.get_operatingsystem(name=operatingsystem).get('id')
        if partition_table:
            data['ptable_id'] = self.get_partition_table(name=partition_table).get('id')
        if smart_proxy:
            data['puppet_proxy_id'] = self.get_smart_proxy(name=smart_proxy).get('id')
        if subnet:
            data['subnet_id'] = self.get_subnet(name=subnet).get('id')
        return self.set_hostgroup(data=data)

    def delete_hostgroup(self, name):
        return self.delete_resource(resource_type='hostgroups',
                                    resource_id=name)

    def get_locations(self):
        return self.get_resources(resource_type='locations')

    def get_location(self, name):
        return self.get_resource(resource_type='locations',
                                 resource_id=name)

    def set_location(self, data):
        return self.post_resource(resource_type='locations',
                                  resource='location',
                                  data=data)

    def get_media(self):
        return self.get_resources(resource_type='media')

    def get_medium(self, name):
        return self.get_resource(resource_type='media',
                                 resource_id=name)

    def set_medium(self, data):
        return self.post_resource(resource_type='media',
                                  resource='medium',
                                  data=data)

    def get_organizations(self):
        return self.get_resources(resource_type='organizations')

    def get_organization(self, name):
        return self.get_resource(resource_type='organizations',
                                 resource_id=name)

    def set_organization(self, data):
        return self.post_resource(resource_type='organizations',
                                  resource='organization', data=data)

    def get_operatingsystems(self):
        return self.get_resources(resource_type='operatingsystems')

    def get_operatingsystem(self, name):
        return self.get_resource(resource_type='operatingsystems',
                                 resource_id=name)

    def set_operatingsystem(self, data):
        return self.post_resource(resource_type='operatingsystems',
                                  resource='operatingsystem',
                                  data=data)

    def get_partition_tables(self):
        return self.get_resources(resource_type='ptables')

    def get_partition_table(self, name):
        return self.get_resource(resource_type='ptables',
                                 resource_id=name)

    def set_partition_table(self, data):
        return self.post_resource(resource_type='ptables',
                                  resource='ptable',
                                  data=data)

    def get_smart_proxies(self):
        return self.get_resources(resource_type='smart_proxies')

    def get_smart_proxy(self, name):
        return self.get_resource(resource_type='smart_proxies',
                                 resource_id=name)

    def set_smart_proxy(self, data):
        return self.post_resource(resource_type='smart_proxies',
                                  resource='smart_proxy',
                                  data=data)

    def get_subnets(self):
        return self.get_resources(resource_type='subnets')

    def get_subnet(self, name):
        return self.get_resource(resource_type='subnets',
                                 resource_id=name)

    def set_subnet(self, data):
        return self.post_resource(resource_type='subnets',
                                  resource='subnet',
                                  data=data)
