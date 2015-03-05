#!/usr/bin/env python

import sys, getopt
import os 
import yaml
import json
from foreman import Foreman

def show_help():
    print 'foreman.py -f <foreman_host> -p <port> -u <username> -s <secret>'

def backup(backup_root_dir, resource, resource_function):
    # Backup Architectures
    backup_dir = backup_root_dir + '/' + resource

    if not os.path.exists(backup_dir): 
        os.makedirs(backup_dir)

    for item in resource_function:
        with open(backup_dir + '/' + item.get('name').replace('/', '_') + '.yaml', 'w') as backup_file:
            yaml.safe_dump(item, backup_file, default_flow_style=False)

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
    backup_root = '.'
        
    backup(backup_root_dir=backup_root, resource='architectures', resource_function=f.get_architectures())
    backup(backup_root_dir=backup_root, resource='compute_resources', resource_function=f.get_compute_resources())
    backup(backup_root_dir=backup_root, resource='compute_profiles', resource_function=f.get_compute_profiles())
    backup(backup_root_dir=backup_root, resource='domains', resource_function=f.get_domains())
    backup(backup_root_dir=backup_root, resource='environments', resource_function=f.get_environments())
    backup(backup_root_dir=backup_root, resource='hosts', resource_function=f.get_hosts())
    backup(backup_root_dir=backup_root, resource='hostgroups', resource_function=f.get_hostgroups())
    backup(backup_root_dir=backup_root, resource='locations', resource_function=f.get_locations())
    backup(backup_root_dir=backup_root, resource='medias', resource_function=f.get_medias())
    backup(backup_root_dir=backup_root, resource='organizations', resource_function=f.get_organizations())
    backup(backup_root_dir=backup_root, resource='operatingsystems', resource_function=f.get_operatingsystems())
    backup(backup_root_dir=backup_root, resource='smart_proxies', resource_function=f.get_smart_proxies())
    
if __name__ == '__main__':
    main(sys.argv[1:])
