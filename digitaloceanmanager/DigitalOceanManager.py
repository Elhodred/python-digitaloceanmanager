# -*- coding: utf-8 -*-

import digitalocean
import time
import re

class DigitalOceanManager:
    """Class with wrappers for python-digitalocean"""

    def __init__(self, *args, **kwargs):
        self.token = None
        self.user = None
        self.passwd = None
        self.ssh_port = None

        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

        self.manager = digitalocean.Manager(token=self.token)

    def destroy_droplet(self, args):
        droplet = self.manager.get_droplet(args.id)
        droplet.destroy()

    def _get_file_contents(self, filename):
        with open (filename, 'r') as myfile:
            data = myfile.read()
        return data

    def create_droplet(self, args):
        ssh_keys = []
        if (args.ssh_key != None):
            key = self.manager.get_ssh_key(args.ssh_key)
            if (key!=None):
                ssh_keys.append(key.id)

        user_data = None
        if (args.user_data != None):
            user_data = self._get_file_contents(args.user_data)
            user_data = user_data.replace("{{{DEFAULT_USER}}}", self.user)
            user_data = user_data.replace("{{{DEFAULT_PASSWORD}}}", re.escape(self.passwd))
            user_data = user_data.replace("{{{SSHD_PORT}}}", self.ssh_port)

        droplet = digitalocean.Droplet( token=self.token,
                                        name=args.name,
                                        region=args.region,
                                        image=args.image,
                                        size_slug=args.size,
                                        ssh_keys=ssh_keys,
                                        backups=args.backups,
                                        user_data=user_data)
        droplet.create()

        # status='in-progress'
        # print status
        # while(status!='completed'):
            # actions = droplet.get_actions()
            # for action in actions:
                # action.load()
                # if (action.status!=status):
                    # print action.status
                    # time.sleep(10)
                # status = action.status

        # droplet = self.manager.get_droplet(droplet.id)
        # self._print_droplet_info(droplet)

    def power_on_droplet(self, args):
        droplet = self.manager.get_droplet(args.id)
        droplet.power_on()

    def shutdown_droplet(self, args):
        droplet = self.manager.get_droplet(args.id)
        droplet.shutdown()

    def reboot_droplet(self, args):
        droplet = self.manager.get_droplet(args.id)
        droplet.reboot()

    def list_droplets(self, args):
        my_droplets = self.manager.get_all_droplets()
        for droplet in my_droplets:
            self._print_droplet_info(droplet)

    def list_regions(self, args):
        regions = self.manager.get_all_regions()
        for region in regions:
            print("Region: %s\tId: %s" % (region.name, region.slug))

    def list_images(self, args):
        images = self.manager.get_all_images()
        for image in images:
            if(image.slug != None):
                print("Distribution: %s\tSlug: %s" % (image.distribution, image.slug))

    def list_ssh_keys(self, args):
        ssh_keys = self.manager.get_all_sshkeys()
        for ssh_key in ssh_keys:
            print("Name: %s\tId: %s" % (ssh_key.name, ssh_key.id))

    def _print_droplet_info(self, droplet):
        print("* Id: %s\tImage: %s\tName: %s\tStatus: %s\tIp Address: %s\tMemory: %s\tDisk: %s\tRegion: %s" %
                (droplet.id, droplet.image['distribution'], droplet.name, droplet.status, droplet.ip_address, droplet.memory,
                droplet.disk, droplet.region['slug']))

