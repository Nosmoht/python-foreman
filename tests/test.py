#!/usr/bin/env python

import sys, getopt
import os
import yaml
import json
from foreman import Foreman

def show_help():
    print 'foreman.py -f <foreman_host> -p <port> -u <username> -s <secret>'

def main(argv):
    foreman_host = os.environ.get('FOREMAN_HOST', '127.0.0.1')
    foreman_port = os.environ.get('FOREMAN_PORT', '443')
    foreman_username = os.environ.get('FOREMAN_USERNAME', 'foreman')
    foreman_password = os.environ.get('FOREMAN_PASSWORD', 'changme')    
    config_file = None
    config = {}
    try:
        opts, args = getopt.getopt(argv, "c:f:hu:p:s:", ["config=", "foreman=", "username=", "port=", "secret="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-c', '--config'):
            config_file = arg
        elif opt in ('-f', '--foreman'):
            foreman_host = arg
        elif opt == '-h':
            show_help()
            sys.exit()
        elif opt in ('-u', '--username'):
            foreman_username = arg
        elif opt in ('-p', '--port'):
            foreman_port = arg
        elif opt in ('-s', '--secret'):
            foreman_password = arg

    f = Foreman(foreman_host, foreman_port, foreman_username, foreman_password)
    if config_file:
        with open(config_file, 'r') as cfgfile:
            config = yaml.load(cfgfile)
    
    # Test Architectures
    for item in config.get('architectures'):
        obj = f.get_architecture_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_architecture(data=item)
        print "Architecture: %s" % (json.dumps(obj))
    
    # Test Compute Resources
    for item in config.get('compute_resources'):
        obj = f.get_compute_resource_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_compute_resource(data=item)
        print "Compute Resource: %s" % (json.dumps(obj))
    
    # Test Domains
    for item in config.get('domains'):
        obj = f.get_domain_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_domain(data=item)
        print "Domain: %s" % (json.dumps(obj))
    
    # Test Environments
    for item in config.get('environments'):
        obj = f.get_environment_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_environment(data=item)
        print "Environment: %s" % (json.dumps(obj))
    
    # Test Locations
    for item in config.get('locations'):
        obj = f.get_location_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_location(data=item)
        print "Location: %s" % (json.dumps(obj))
            
    # Test Media
    for item in config.get('medias'):
        obj = f.get_media_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_media(data=item)
        else:
            print "Media exist: %s" % (json.dumps(obj))

    # Test Operatingsystems
    for item in config.get('operatingsystems'):
        obj = f.get_operatingsystem_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_operatingsystem(data=item)
        print "Operatingsystem exist: %s" % (json.dumps(obj))
            
    # Test Organizations
    for item in config.get('organizations'):
        obj = f.get_organization_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_organization(data=item)
        print "Organization exist: %s" % (json.dumps(obj))
            
    # Test Partition Tables
    for item in config.get('partition_tables'):
        obj = f.get_partition_table_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_partition_table(data=item)
        print "Partition Table exist: %s" % (json.dumps(obj))
            
    # Test Smart Proxies
    for item in config.get('smart_proxies'):
        obj = f.get_smart_proxy_by_name(name=item.get('name'))
        if not obj:
            obj = f.set_smart_proxy(data=item)
        print "Smart Proxy exist: %s" % (json.dumps(obj))
            
if __name__ == '__main__':
    main(sys.argv[1:])
