#!/usr/bin/env python

import argparse
import ConfigParser
import os.path
import digitaloceanmanager
import getpass
from passlib.hash import sha512_crypt

token = None
user = None
passwd = None
ssh_port = None

if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    if (os.path.isfile('doma.cfg')):
        config.read('doma.cfg')
        token = config.get('General', 'token')
        user = config.get('General', 'user')
        passwd = config.get('General', 'password')
        ssh_port = config.get('General', 'ssh_port')
    else :
        token = raw_input('Please insert your Digital Ocean API Token: ')
        user = raw_input('Please insert the user to create in the droplets: ')
        passwd = sha512_crypt.encrypt(getpass.getpass('Please insert the password for the user: '))
        ssh_port = raw_input('Please insert port where you want sshd to run: ')

        config.add_section('General')
        config.set('General', 'token', token)
        config.set('General', 'user', user)
        config.set('General', 'password', passwd)
        config.set('General', 'ssh_port', ssh_port)

        with open('doma.cfg','wb') as configfile:
            config.write(configfile)

    manager = digitaloceanmanager.DigitalOceanManager(token=token, user=user, passwd=passwd, ssh_port=ssh_port)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands', description='list of available actions', help='commands help')

    # Create a Droplet command
    parser_droplet = subparsers.add_parser('droplet', help='manage droplets')
    droplet_subparsers = parser_droplet.add_subparsers(title='droplet commands', description='list of available actions',
            help='droplet commands help')
    parser_create  = droplet_subparsers.add_parser('create', help='create a droplet')
    parser_create.add_argument('--name', required=True, help='droplet name')
    parser_create.add_argument('--region', required=True, help='region where to create droplet')
    parser_create.add_argument('--image', required=True, help='image to use for the droplet')
    parser_create.add_argument('--size', required=True, help='size of the droplet, tied to cost')
    parser_create.add_argument('--ssh_key', help='id of the ssh key to add to droplet')
    parser_create.add_argument('--backups', default=False, help='activate backups')
    parser_create.add_argument('--user_data', help='fills droplet metadata with file content')
    parser_create.set_defaults(func=manager.create_droplet)

    # Destroy a Droplet command
    parser_destroy = droplet_subparsers.add_parser('destroy', help='destroy a droplet')
    parser_destroy.add_argument('id', help='id of the droplet to destroy')
    parser_destroy.set_defaults(func=manager.destroy_droplet)

    # List all Droplets command
    parser_list = droplet_subparsers.add_parser('list', help='list all droplets')
    parser_list.set_defaults(func=manager.list_droplets)

    # Reboot a Droplet
    parser_reboot = droplet_subparsers.add_parser('reboot', help='reboot a droplet')
    parser_reboot.add_argument('id', help='id of the droplet to reboot')
    parser_reboot.set_defaults(func=manager.reboot_droplet)

    #Start a Droplet
    parser_start = droplet_subparsers.add_parser('start', help='start a droplet')
    parser_start.add_argument('id', help='id of the droplet to start')
    parser_start.set_defaults(func=manager.power_on_droplet)

    # Shutdown a Droplet
    parser_shutdown = droplet_subparsers.add_parser('shutdown', help='shutdown a droplet')
    parser_shutdown.add_argument('id', help='id of the droplet to shutdown')
    parser_shutdown.set_defaults(func=manager.shutdown_droplet)

    # List available images
    parser_images = subparsers.add_parser('images', help='list all images')
    parser_images.set_defaults(func=manager.list_images)

    # List available Regions
    parser_regions = subparsers.add_parser('regions', help='list all regions available')
    parser_regions.set_defaults(func=manager.list_regions)

    # List SSH keys
    parser_ssh_keys = subparsers.add_parser('ssh_keys', help='list all ssh keys')
    parser_ssh_keys.set_defaults(func=manager.list_ssh_keys)

    args = parser.parse_args()
    args.func(args)
