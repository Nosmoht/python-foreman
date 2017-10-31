"""
Created on 04.03.2015

@author: tkrah
"""

import json

import requests

# from requests.auth import HTTPBasicAuth
try:
    requests.urllib3.disable_warnings()
except AttributeError:
    requests.packages.urllib3.disable_warnings()

FOREMAN_REQUEST_HEADERS = {
    'content-type': 'application/json',
    'accept': 'application/json'
}
FOREMAN_API_VERSION = 'v2'

ARCHITECTURES = 'architectures'
ARCHITECTURE = 'architecture'
COMMON_PARAMETERS = 'common_parameters'
COMMON_PARAMETER = 'common_parameter'
COMPUTE_ATTRIBUTES = 'compute_attributes'
COMPUTE_ATTRIBUTE = 'compute_attribute'
COMPUTE_PROFILES = 'compute_profiles'
COMPUTE_PROFILE = 'compute_profile'
COMPUTE_RESOURCES = 'compute_resources'
COMPUTE_RESOURCE = 'compute_resource'
CONFIG_TEMPLATES = 'config_templates'
CONFIG_TEMPLATE = 'config_template'
DOMAINS = 'domains'
DOMAIN = 'domain'
ENVIRONMENTS = 'environments'
ENVIRONMENT = 'environment'
EXTERNAL_USERGROUPS = 'external_usergroups'
EXTERNAL_USERGROUP = 'external_usergroup'
FILTERS = 'filters'
FILTER = 'filter'
HOSTS = 'hosts'
HOST = 'host'
HOSTGROUPS = 'hostgroups'
HOSTGROUP = 'hostgroup'
IMAGES = 'images'
IMAGE = 'image'
LOCATIONS = 'locations'
LOCATION = 'location'
AUTH_SOURCE_LDAPS = 'auth_source_ldaps'
AUTH_SOURCE_LDAP = 'auth_source_ldap'
MEDIA = 'media'
MEDIUM = 'medium'
OPERATINGSYSTEMS = 'operatingsystems'
OPERATINGSYSTEM = 'operatingsystem'
ORGANIZATIONS = 'organizations'
ORGANIZATION = 'organization'
OS_DEFAULT_TEMPLATES = 'os_default_templates'
OS_DEFAULT_TEMPLATE = 'os_default_template'
PARAMETERS = 'parameters'
PARAMETER = 'parameter'
PARTITION_TABLES = 'ptables'
PARTITION_TABLE = 'ptable'
PERMISSIONS = 'permissions'
PERMISSION = 'permission'
REALMS = 'realms'
REALM = 'realm'
ROLES = 'roles'
ROLE = 'role'
SETTING = 'setting'
SETTINGS = 'settings'
SMART_PROXIES = 'smart_proxies'
SMART_PROXY = 'smart_proxy'
SUBNETS = 'subnets'
SUBNET = 'subnet'
TEMPLATE_KINDS = 'template_kinds'
USERS = 'users'
USER = 'user'
USERGROUPS = 'usergroups'
USERGROUP = 'usergroup'


class ForemanError(Exception):
    """ForemanError Class

    Simple class to handle exceptions while communicating to Foreman API
    """

    def __init__(self, url, status_code, message):
        self.url = url
        self.status_code = status_code
        self.message = message
        super(ForemanError, self).__init__()


class Foreman:
    """Foreman Class

    Communicate with Foreman via API v2

    """

    def __init__(self, hostname, port, username, password, ssl=True):
        """Init
        """
        self.__auth = (username, password)
        self.hostname = hostname
        self.port = port
        self.url_scheme = ("http", "https")[ssl]
        self.url = "{0}://{1}:{2}/api/{3}".format(
            self.url_scheme,
            self.hostname,
            self.port,
            FOREMAN_API_VERSION,
        )

    def _get_resource_url(self, resource_type, resource_id=None, component=None, component_id=None):
        """Create API URL path

        Args:
          resource_type (str): Name of resource to request
          resource_id (str): Resource identifier
          component (str): Component of a resource (e.g. images in
              /host/host01.example.com/images)
          component_id (str): Component identifier (e.g. nic01 in
              /host/host01.example.com/interfaces/nic1)
        """
        url = self.url + '/' + resource_type
        if resource_id:
            url = url + '/' + str(resource_id)
            if component:
                url = url + '/' + component
                if component_id:
                    url = url + '/' + str(component_id)
        return url

    def _get_request_error_message(self, data):
        request_json = data.json()
        if 'error' in request_json:
            request_error = data.json().get('error')
        elif 'errors' in request_json:
            request_error = data.json().get('errors')

        if 'message' in request_error:
            error_message = request_error.get('message')
        elif 'full_messages' in request_error:
            error_message = ', '.join(request_error.get('full_messages'))
        else:
            error_message = str(request_error)

        return error_message

    def _handle_request(self, req):
        if req.status_code in [200, 201]:
            return json.loads(req.text)
        elif req.status_code == 404:
            error_message = 'Not found'
        else:
            error_message = self._get_request_error_message(data=req)

        raise ForemanError(url=req.url,
                           status_code=req.status_code,
                           message=error_message)

    def _get_request(self, url, data=None):
        """Execute a GET request agains Foreman API

        Args:
          resource_type (str): Name of resource to get
          component (str): Name of resource components to get
          component_id (str): Name of resource component to get
          data (dict): Dictionary to specify detailed data
        Returns:
          Dict
        """
        req = requests.get(url=url,
                           data=data,
                           auth=self.__auth,
                           verify=False)
        return self._handle_request(req)

    def _post_request(self, url, data):
        """Execute a POST request against Foreman API

        Args:
          resource_type (str): Name of resource type to post
          component (str): Name of resource to post
          data (dict): Dictionary containing component details
        Returns:
          Dict
        """
        req = requests.post(url=url,
                            data=json.dumps(data),
                            headers=FOREMAN_REQUEST_HEADERS,
                            auth=self.__auth,
                            verify=False)
        return self._handle_request(req)

    def _put_request(self, url, data):
        """Execute a PUT request against Foreman API

        Args:
          resource_type (str): Name of resource type to post
          resource_id (str): Resource identified
          data (dict): Dictionary of details
        Returns:
          Dict
        """
        req = requests.put(url=url,
                           data=json.dumps(data),
                           headers=FOREMAN_REQUEST_HEADERS,
                           auth=self.__auth,
                           verify=False)
        return self._handle_request(req)

    def _delete_request(self, url):
        """Execute a DELETE request against Foreman API

        Args:
          resource_type (str): Name of resource type to post
          resource_id (str): Resource identified
        Returns:
          Dict
        """
        req = requests.delete(url=url,
                              headers=FOREMAN_REQUEST_HEADERS,
                              auth=self.__auth,
                              verify=False)
        return self._handle_request(req)

    def get_resources(self, resource_type, resource_id=None, component=None):
        """ Return a list of all resources of the defined resource type

        Args:
           resource_type: Type of resources to get
           resource_id (str): Resource identified
           component (str): Component name to request
           component_id (int): Component id to request
        Returns:
           list of dict
        """
        url = self._get_resource_url(resource_type=resource_type,
                                     resource_id=resource_id,
                                     component=component)
        request_result = self._get_request(url=url,
                                           data={'page': '1', 'per_page': 99999})
        return request_result.get('results')

    def get_resource(self, resource_type, resource_id, component=None, component_id=None):
        """ Get information about a resource

        If data contains id the resource will be get directly from the API.
        If id is not specified but name the resource will be searched within
        the database.
        If found the id of the research will be used. If not found None will
        be returned.

        :rtype : object
        Args:
           resource_type (str): Resource type
           resource_id (str): Resource identified
           component (str): Component name to request
           component_id (int): Component id to request
        Returns:
           dict
        """
        url = self._get_resource_url(resource_type=resource_type,
                                     resource_id=resource_id,
                                     component=component,
                                     component_id=component_id)
        return self._get_request(url=url)

    def create_resource(self, resource_type, resource, data,
                        resource_id=None, component=None, additional_data=None):
        """ Create a resource by executing a post request to Foreman

        Execute a post request to create one <resource> of a <resource type>.
        Foreman expects usually the following content:

        {
          "<resource>": {
            "param1": "value",
            "param2": "value",
            ...
            "paramN": "value"
          }
        }

        <data> has to contain all parameters and values of the resource to be
        created. They are passed as {<resource>: data}.

        As not all resource types can be handled in this way <additional_data>
        can be used to pass more data in. All key/values pairs will be passed
        directly and not passed inside '{<resource>: data}.

        Args:
           data(dict): Hash containing parameter/value pairs
        """
        url = self._get_resource_url(resource_type=resource_type,
                                     resource_id=resource_id,
                                     component=component)
        resource_data = {}
        if additional_data:
            for key in additional_data.keys():
                resource_data[key] = additional_data[key]
        resource_data[resource] = data
        return self._post_request(url=url, data=resource_data)

    def update_resource(self, resource_type, resource_id, data, component=None, component_id=None):
        url = self._get_resource_url(resource_type=resource_type, resource_id=resource_id,
                                     component=component, component_id=component_id)
        return self._put_request(url=url, data=data)

    def delete_resource(self, resource_type, resource_id, component=None, component_id=None):
        url = self._get_resource_url(resource_type=resource_type, resource_id=resource_id,
                                     component=component, component_id=component_id)
        return self._delete_request(url=url)

    def search_resource(self, resource_type, data):
        search_data = {'search': '', 'per_page': 1000 }

        for key, value in data.items():
            if search_data['search']:
                search_data['search'] += ' AND '
            search_data['search'] += (key + ' == ')

            if isinstance(value, int):
                search_data['search'] += str(value)
            elif isinstance(value, str):
                search_data['search'] += ('"' + value + '"')
            else:
                TypeError("Type {0} of search key {1} not supported".format(type(value), key))

        url = self._get_resource_url(resource_type=resource_type)
        results = self._get_request(url=url, data=search_data)
        result = results.get('results')

        if len(result) == 1:
            return result[0]

        return result

    def get_architectures(self):
        return self.get_resources(resource_type=ARCHITECTURES)

    def get_architecture(self, id):
        return self.get_resource(resource_type=ARCHITECTURES, resource_id=id)

    def search_architecture(self, data):
        return self.search_resource(resource_type=ARCHITECTURES, data=data)

    def create_architecture(self, data):
        return self.create_resource(resource_type=ARCHITECTURES, resource=ARCHITECTURE, data=data)

    def delete_architecture(self, id):
        return self.delete_resource(resource_type=ARCHITECTURES, resource_id=id)

    def get_auth_source_ldaps(self):
        return self.get_resources(resource_type=AUTH_SOURCE_LDAPS)

    def get_auth_source_ldap(self, id):
        return self.get_resource(resource_type=AUTH_SOURCE_LDAPS, resource_id=id)

    def search_auth_source_ldap(self, data):
        return self.search_resource(resource_type=AUTH_SOURCE_LDAPS, data=data)

    def create_auth_source_ldap(self, data):
        return self.create_resource(resource_type=AUTH_SOURCE_LDAPS, resource=AUTH_SOURCE_LDAP, data=data)

    def delete_auth_source_ldap(self, id):
        return self.delete_resource(resource_type=AUTH_SOURCE_LDAPS, resource_id=id)

    def update_auth_source_ldap(self, id, data):
        return self.update_resource(resource_type=AUTH_SOURCE_LDAPS, resource_id=id, data=data)

    def get_common_parameters(self):
        return self.get_resources(resource_type=COMMON_PARAMETERS)

    def get_common_parameter(self, id):
        return self.get_resource(resource_type=COMMON_PARAMETERS, resource_id=id)

    def search_common_parameter(self, data):
        return self.search_resource(resource_type=COMMON_PARAMETERS, data=data)

    def create_common_parameter(self, data):
        return self.create_resource(resource_type=COMMON_PARAMETERS,
                                    resource=COMMON_PARAMETER,
                                    data=data)

    def delete_common_parameter(self, id):
        return self.delete_resource(resource_type=COMMON_PARAMETERS, resource_id=id)

    def get_compute_attribute(self, compute_resource_id, compute_profile_id):
        """
        Return the compute attributes of a compute profile assigned to a compute resource.

        Args:
           compute_resource_id (int): Compute resource identifier
           compute_profile_id (int): Compute profile identifier
        Returns:
           dict
        """
        compute_resource = self.get_compute_resource(id=compute_resource_id)
        compute_attributes = compute_resource.get(COMPUTE_ATTRIBUTES)

        return filter(lambda item: item.get('compute_profile_id') == compute_profile_id, compute_attributes)

    def create_compute_attribute(self, compute_resource_id, compute_profile_id, data):
        """ Create compute attributes for a compute profile in a compute resource

        Args:
           data(dict): Dict containing attributes
        """
        addition_data = {'compute_resource_id': compute_resource_id, 'compute_profile_id': compute_profile_id}

        return self.create_resource(resource_type=COMPUTE_ATTRIBUTES,
                                    resource=COMPUTE_ATTRIBUTE,
                                    data=data,
                                    additional_data=addition_data)

    def update_compute_attribute(self, id, data):
        return self.update_resource(resource_type=COMPUTE_ATTRIBUTES,
                                    resource_id=id,
                                    data={'vm_attrs': data})

    def get_compute_profiles(self):
        return self.get_resources(resource_type=COMPUTE_PROFILES)

    def get_compute_profile(self, id):
        return self.get_resource(resource_type=COMPUTE_PROFILES, resource_id=id)

    def search_compute_profile(self, data):
        return self.search_resource(resource_type=COMPUTE_PROFILES, data=data)

    def create_compute_profile(self, data):
        return self.create_resource(resource_type=COMPUTE_PROFILES,
                                    resource=COMPUTE_PROFILE,
                                    data=data)

    def delete_compute_profile(self, id):
        return self.delete_resource(resource_type=COMPUTE_PROFILES, resource_id=id)

    def get_compute_resources(self):
        return self.get_resources(resource_type=COMPUTE_RESOURCES)

    def get_compute_resource(self, id):
        return self.get_resource(resource_type=COMPUTE_RESOURCES, resource_id=id)

    def search_compute_resource(self, data):
        return self.search_resource(resource_type=COMPUTE_RESOURCES, data=data)

    def create_compute_resource(self, data):
        return self.create_resource(resource_type=COMPUTE_RESOURCES,
                                    resource=COMPUTE_RESOURCE,
                                    data=data)

    def update_compute_resource(self, id, data):
        """Update the parameters of a compute resources"""
        return self.update_resource(resource_type=COMPUTE_RESOURCES,
                                    data=data,
                                    resource_id=id)

    def delete_compute_resource(self, id):
        return self.delete_resource(resource_type=COMPUTE_RESOURCES, resource_id=id)

    def get_compute_resource_images(self, compute_resource_id):
        """Get images registered on a given compute resource"""
        return self.get_resources(resource_type=COMPUTE_RESOURCES,
                                  resource_id=compute_resource_id,
                                  component=IMAGES)

    def create_compute_resource_image(self, compute_resource_id, data):
        """Add an image to a compute resource"""
        return self.create_resource(resource_type=COMPUTE_RESOURCES,
                                    data=data,
                                    resource_id=compute_resource_id,
                                    resource=IMAGE,
                                    component=IMAGES)

    def delete_compute_resource_image(self, compute_resource_id, image_id):
        """Delete an image on a given compute resource"""
        return self.delete_resource(resource_type=COMPUTE_RESOURCES,
                                    resource_id=compute_resource_id,
                                    component=IMAGES,
                                    component_id=image_id)

    def update_compute_resource_image(self, compute_resource_id, data):
        """Update the parameters of an image on a given compute resource"""
        return self.update_resource(resource_type=COMPUTE_RESOURCES,
                                    data=data,
                                    resource_id=compute_resource_id,
                                    component=IMAGES,
                                    component_id=data['id'])

    def get_config_templates(self):
        return self.get_resources(resource_type=CONFIG_TEMPLATES)

    def get_config_template(self, id):
        return self.get_resource(resource_type=CONFIG_TEMPLATES, resource_id=id)

    def search_config_template(self, data):
        return self.search_resource(resource_type=CONFIG_TEMPLATES, data=data)

    def create_config_template(self, data):
        return self.create_resource(resource_type=CONFIG_TEMPLATES,
                                    resource=CONFIG_TEMPLATE,
                                    data=data)

    def update_config_template(self, id, data):
        return self.update_resource(resource_type=CONFIG_TEMPLATES, resource_id=id, data=data)

    def delete_config_template(self, id):
        return self.delete_resource(resource_type=CONFIG_TEMPLATES, resource_id=id)

    def get_domains(self):
        return self.get_resources(resource_type=DOMAINS)

    def get_domain(self, id):
        return self.get_resource(resource_type=DOMAINS, resource_id=id)

    def search_domain(self, data):
        return self.search_resource(resource_type=DOMAINS, data=data)

    def create_domain(self, data):
        return self.create_resource(resource_type=DOMAINS, resource=DOMAIN, data=data)

    def update_domain(self, id, data):
        return self.update_resource(resource_type=DOMAINS, resource_id=id, data=data)

    def delete_domain(self, id):
        return self.delete_resource(resource_type=DOMAINS, resource_id=id)

    def get_environments(self):
        return self.get_resources(resource_type=ENVIRONMENTS)

    def get_environment(self, id):
        return self.get_resource(resource_type=ENVIRONMENTS, resource_id=id)

    def search_environment(self, data):
        return self.search_resource(resource_type=ENVIRONMENTS, data=data)

    def create_environment(self, data):
        return self.create_resource(resource_type=ENVIRONMENTS, resource=ENVIRONMENT, data=data)

    def delete_environment(self, id):
        return self.delete_resource(resource_type=ENVIRONMENTS, resource_id=id)

    def get_external_usergroups(self, id):
        return self.get_resources(resource_type=USERGROUPS, resource_id=id, component=EXTERNAL_USERGROUPS)

    def create_external_usergroup(self, usergroup_id, data):
        return self.create_resource(resource_type=USERGROUPS,
                                    resource=EXTERNAL_USERGROUP,
                                    resource_id=usergroup_id,
                                    component=EXTERNAL_USERGROUPS,
                                    data=data)

    def delete_external_usergroup(self, group_id, ext_group_id):
        return self.delete_resource(resource_type=USERGROUPS,
                                    resource_id=group_id,
                                    component=EXTERNAL_USERGROUPS,
                                    component_id=ext_group_id)

    def get_filters(self):
        return self.get_resources(resource_type=FILTERS)

    def get_filter(self, id):
        return self.get_resource(resource_type=FILTERS, resource_id=id)

    def get_filters(self):
        return self.get_resources(resource_type=FILTERS)

    def search_filter(self, data):
        return self.search_resource(resource_type=FILTERS, data=data)

    def create_filter(self, data):
        return self.create_resource(resource_type=FILTERS, resource=FILTER, data=data)

    def delete_filter(self, id):
        return self.delete_resource(resource_type=FILTERS, resource_id=id)

    def get_hosts(self):
        return self.get_resources(resource_type=HOSTS)

    def get_host(self, id):
        return self.get_resource(resource_type=HOSTS, resource_id=id)

    def search_host(self, data):
        return self.search_resource(resource_type=HOSTS, data=data)

    def create_host(self, data):
        return self.create_resource(resource_type=HOSTS, resource=HOST, data=data)

    def update_host(self, id, data):
        return self.update_resource(resource_type=HOSTS, resource_id=id, data=data)

    def delete_host(self, id):
        return self.delete_resource(resource_type=HOSTS, resource_id=id)

    def set_host_power(self, host_id, action):
        return self.update_resource(resource_type=HOSTS,
                                    resource_id=host_id,
                                    component='power',
                                    data={'power_action': action, HOST: {}})

    def get_host_power(self, host_id):
        return self.set_host_power(host_id=host_id, action='state')

    def poweron_host(self, host_id):
        return self.set_host_power(host_id=host_id, action='start')

    def poweroff_host(self, host_id):
        return self.set_host_power(host_id=host_id, action='stop')

    def reboot_host(self, host_id):
        return self.set_host_power(host_id=host_id, action='reboot')

    # def get_host_component(self, name, component, component_id=None):
    # return self.get_host(name=name, component=component, component_id=component_id)

    # def get_host_interfaces(self, name):
    # return self.get_host_component(name=name, component='interfaces')

    # def get_host_interface(self, name, interface_id):
    # return self.get_host_component(name=name, component='interfaces', component_id=interface_id)

    def get_host_parameters(self, host_id):
        parameters = self.get_resource(resource_type=HOSTS, resource_id=host_id, component=PARAMETERS)
        if parameters and 'results' in parameters:
            return parameters.get('results')
        return None

    def create_host_parameter(self, host_id, data):
        return self.create_resource(resource_type=HOSTS,
                                    resource_id=host_id,
                                    resource=PARAMETER,
                                    data=data,
                                    component=PARAMETERS)

    def update_host_parameter(self, host_id, parameter_id, data):
        return self.update_resource(resource_type=HOSTS,
                                    resource_id=host_id,
                                    component=PARAMETERS,
                                    component_id=parameter_id,
                                    data=data)

    def delete_host_parameter(self, host_id, parameter_id):
        return self.delete_resource(resource_type=HOSTS,
                                    resource_id=host_id,
                                    component=PARAMETERS,
                                    component_id=parameter_id)

    def get_hostgroups(self):
        return self.get_resources(resource_type=HOSTGROUPS)

    def get_hostgroup(self, id):
        return self.get_resource(resource_type=HOSTGROUPS, resource_id=id)

    def search_hostgroup(self, data):
        return self.search_resource(resource_type=HOSTGROUPS, data=data)

    def create_hostgroup(self, data):
        return self.create_resource(resource_type=HOSTGROUPS, resource=HOSTGROUP, data=data)

    def update_hostgroup(self, id, data):
        return self.update_resource(resource_type=HOSTGROUPS, resource_id=id, data=data)

    def delete_hostgroup(self, id):
        return self.delete_resource(resource_type=HOSTGROUPS, resource_id=id)

    def get_hostgroup_parameters(self, hostgroup_id):
        parameters = self.get_resource(resource_type=HOSTGROUPS, resource_id=hostgroup_id, component=PARAMETERS)
        if parameters and 'results' in parameters:
            return parameters.get('results')
        return None

    def create_hostgroup_parameter(self, hostgroup_id, data):
        return self.create_resource(resource_type=HOSTGROUPS,
                                    resource_id=hostgroup_id,
                                    resource=PARAMETER,
                                    data=data,
                                    component=PARAMETERS)

    def update_hostgroup_parameter(self, hostgroup_id, parameter_id, data):
        return self.update_resource(resource_type=HOSTGROUPS,
                                    resource_id=hostgroup_id,
                                    component=PARAMETERS,
                                    component_id=parameter_id,
                                    data=data)

    def delete_hostgroup_parameter(self, hostgroup_id, parameter_id):
        return self.delete_resource(resource_type=HOSTGROUPS,
                                    resource_id=hostgroup_id,
                                    component=PARAMETERS,
                                    component_id=parameter_id)

    def get_locations(self):
        return self.get_resources(resource_type=LOCATIONS)

    def get_location(self, id):
        return self.get_resource(resource_type=LOCATIONS, resource_id=id)

    def search_location(self, data):
        return self.search_resource(resource_type=LOCATIONS, data=data)

    def create_location(self, data):
        return self.create_resource(resource_type=LOCATIONS, resource=LOCATION, data=data)

    def delete_location(self, id):
        return self.delete_resource(resource_type=LOCATIONS, resource_id=id)

    def get_media(self):
        return self.get_resources(resource_type=MEDIA)

    def get_medium(self, id):
        return self.get_resource(resource_type=MEDIA, resource_id=id)

    def search_medium(self, data):
        return self.search_resource(resource_type=MEDIA, data=data)

    def create_medium(self, data):
        return self.create_resource(resource_type=MEDIA, resource=MEDIUM, data=data)

    def delete_medium(self, id):
        return self.delete_resource(resource_type=MEDIA, resource_id=id)

    def update_medium(self, id, data):
        return self.update_resource(resource_type=MEDIA, resource_id=id, data=data)

    def get_organizations(self):
        return self.get_resources(resource_type=ORGANIZATIONS)

    def get_organization(self, id):
        return self.get_resource(resource_type=ORGANIZATIONS, resource_id=id)

    def search_organization(self, data):
        return self.search_resource(resource_type=ORGANIZATIONS, data=data)

    def create_organization(self, data):
        return self.create_resource(resource_type=ORGANIZATIONS, resource=ORGANIZATION, data=data)

    def delete_organization(self, id):
        return self.delete_resource(resource_type=ORGANIZATIONS, resource_id=id)

    def get_operatingsystems(self):
        return self.get_resources(resource_type=OPERATINGSYSTEMS)

    def get_operatingsystem(self, id):
        return self.get_resource(resource_type=OPERATINGSYSTEMS, resource_id=id)

    def search_operatingsystem(self, data):
        return self.search_resource(resource_type=OPERATINGSYSTEMS, data=data)

    def create_operatingsystem(self, data):
        return self.create_resource(resource_type=OPERATINGSYSTEMS, resource=OPERATINGSYSTEM, data=data)

    def update_operatingsystem(self, id, data):
        return self.update_resource(resource_type=OPERATINGSYSTEMS, resource_id=id, data=data)

    def delete_operatingsystem(self, id):
        return self.delete_resource(resource_type=OPERATINGSYSTEMS, resource_id=id)

    def get_operatingsystem_default_templates(self, id):
        return self.get_resources(resource_type=OPERATINGSYSTEMS, resource_id=id, component=OS_DEFAULT_TEMPLATES)

    def get_operatingsystem_default_template(self, id, template_id):
        return self.get_resource(resource_type=OPERATINGSYSTEMS, resource_id=id,
                                 component=OS_DEFAULT_TEMPLATES, component_id=template_id)

    def create_operatingsystem_default_template(self, id, data):
        return self.create_resource(resource_type=OPERATINGSYSTEMS, resource=OS_DEFAULT_TEMPLATE, data=data,
                                    resource_id=id, component=OS_DEFAULT_TEMPLATES)

    def update_operatingsystem_default_template(self, id, template_id, data):
        return self.update_resource(resource_type=OPERATINGSYSTEMS, resource_id=id,
                                    component=OS_DEFAULT_TEMPLATES, component_id=template_id,
                                    resource=OS_DEFAULT_TEMPLATE, data=data)

    def delete_operatingsystem_default_template(self, id, template_id):
        return self.delete_resource(resource_type=OPERATINGSYSTEMS, resource_id=id,
                                    component=OS_DEFAULT_TEMPLATES, component_id=template_id)

    def get_partition_tables(self):
        return self.get_resources(resource_type=PARTITION_TABLES)

    def get_partition_table(self, id):
        return self.get_resource(resource_type=PARTITION_TABLES, resource_id=id)

    def search_partition_table(self, data):
        return self.search_resource(resource_type=PARTITION_TABLES, data=data)

    def create_partition_table(self, data):
        return self.create_resource(resource_type=PARTITION_TABLES, resource=PARTITION_TABLE, data=data)

    def update_partition_table(self, id, data):
        return self.update_resource(resource_type=PARTITION_TABLES, resource_id=id, data=data)

    def delete_partition_table(self, id):
        return self.delete_resource(resource_type=PARTITION_TABLES, resource_id=id)

    def get_permissions(self):
        return self.get_resources(resource_type=PERMISSIONS)

    def get_permission(self, id):
        return self.get_resource(resource_type=PERMISSIONS, resource_id=id)

    def search_permission(self, data):
        return self.search_resource(resource_type=PERMISSIONS, data=data)

    def get_realms(self):
        return self.get_resources(resource_type=REALMS)

    def get_realm(self, id):
        return self.get_resource(resource_type=REALMS, resource_id=id)

    def search_realm(self, data):
        return self.search_resource(resource_type=REALMS, data=data)

    def create_realm(self, data):
        return self.create_resource(resource_type=REALMS, resource=REALM, data=data)

    def delete_realm(self, id):
        return self.delete_resource(resource_type=REALMS, resource_id=id)

    def update_realm(self, id, data):
        return self.update_resource(resource_type=REALMS, resource_id=id, data=data)

    def get_roles(self):
        return self.get_resources(resource_type=ROLES)

    def get_role(self, id):
        return self.get_resource(resource_type=ROLES, resource_id=id)

    def search_role(self, data):
        return self.search_resource(resource_type=ROLES, data=data)

    def create_role(self, data):
        return self.create_resource(resource_type=ROLES, resource=ROLE, data=data)

    def delete_role(self, id):
        return self.delete_resource(resource_type=ROLES, resource_id=id)

    def get_setting(self, id):
        return self.get_resource(resource_type=SETTINGS, resource_id=id)

    def search_setting(self, data):
        return self.search_resource(resource_type=SETTINGS, data=data)

    def update_setting(self, id, data):
        return self.update_resource(resource_type=SETTINGS, resource_id=id, data=data)

    def get_smart_proxies(self):
        return self.get_resources(resource_type=SMART_PROXIES)

    def get_smart_proxy(self, id):
        return self.get_resource(resource_type=SMART_PROXIES, resource_id=id)

    def search_smart_proxy(self, data):
        return self.search_resource(resource_type=SMART_PROXIES, data=data)

    def create_smart_proxy(self, data):
        return self.create_resource(resource_type=SMART_PROXIES, resource=SMART_PROXY, data=data)

    def update_smart_proxy(self, id, data):
        return self.update_resource(resource_type=SMART_PROXIES, resource_id=id, data=data)

    def delete_smart_proxy(self, id):
        return self.delete_resource(resource_type=SMART_PROXIES, resource_id=id)

    def get_subnets(self):
        return self.get_resources(resource_type=SUBNETS)

    def get_subnet(self, id):
        return self.get_resource(resource_type=SUBNETS, resource_id=id)

    def search_subnet(self, data):
        return self.search_resource(resource_type=SUBNETS, data=data)

    def create_subnet(self, data):
        return self.create_resource(resource_type=SUBNETS, resource=SUBNET, data=data)

    def update_subnet(self, id, data):
        return self.update_resource(resource_type=SUBNETS, resource_id=id, data=data)

    def delete_subnet(self, id):
        return self.delete_resource(resource_type=SUBNETS, resource_id=id)

    def get_template_kinds(self):
        return self.get_resources(resource_type=TEMPLATE_KINDS)

    def get_users(self):
        return self.get_resources(resource_type=USERS)

    def get_user(self, id):
        return self.get_resource(resource_type=USERS, resource_id=id)

    def search_user(self, data):
        return self.search_resource(resource_type=USERS, data=data)

    def create_user(self, data):
        return self.create_resource(resource_type=USERS, resource=USER, data=data)

    def update_user(self, id, data):
        return self.update_resource(resource_type=USERS, resource_id=id, data=data)

    def delete_user(self, id):
        return self.delete_resource(resource_type=USERS, resource_id=id)

    def get_usergroups(self):
        return self.get_resources(resource_type=USERGROUPS)

    def get_usergroup(self, id):
        return self.get_resource(resource_type=USERGROUPS, resource_id=id)

    def search_usergroup(self, data):
        return self.search_resource(resource_type=USERGROUPS, data=data)

    def create_usergroup(self, data):
        return self.create_resource(resource_type=USERGROUPS, resource=USERGROUP, data=data)

    def update_usergroup(self, id, data):
        return self.update_resource(resource_type=USERGROUPS, resource_id=id, data=data)

    def delete_usergroup(self, id):
        return self.delete_resource(resource_type=USERGROUPS, resource_id=id)

    def search_template_kind(self, data):
        return self.search_resource(resource_type=TEMPLATE_KINDS, data=data)
