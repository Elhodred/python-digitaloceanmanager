# Digital Ocean Manager
Quick and dirty CLI wrapper around python-digitalocean to manage droplets from the command line

### How to use it
./doma.py -h is your friend

First time you execute doma.py it will ask a few questions: API token, username, password and sshd port.
This settings are stored in doma.cfg file
API token is your Digital Ocean token to connect and manage droplets with your account
The other parameters are used with scripts and will be provisioned into the droplets as user_data field. The purpose is to do a basic provisioning for the droplets:
- Disable root login
- Create a user with a password and give him sudo powers
- Change sshd port
- Configure iptables to allow only access to ssh port

Scripts for ubuntu and centos 7 are provided but you can add your own provisioning scripts.
The scripts provided use another git repository containing a puppet module to do all the dirty work.
The original module was created by my colleague @giavac. Kudos to him.

```
| => ./doma.py -h
usage: doma.py [-h] {droplet,images,regions,ssh_keys} ...

optional arguments:
  -h, --help            show this help message and exit

commands:
  list of available actions

  {droplet,images,regions,ssh_keys}
                        commands help
    droplet             manage droplets
    images              list all images
    regions             list all regions available
    ssh_keys            list all ssh keys
```

### How to create a droplet
```
./doma.py droplet create --name test-droplet --region lon1 --image ubuntu-14-04-x64 --size 1gb --ssh_key 123456 --user_data hardening_ubuntu.sh
```
ssh_key is the id in Digital Ocean of the ssh key you want to use. For now you can only list the keys with ssh_keys command.
region is the slug of the region where you want to create the droplet. You can check them with regions command.
image is the slug of the image you want to use for the droplet. You can check them with images command.
user_data is the script you want to use to provision the droplet. You can use one of the provided or create your own.

### Notice
This was done as a quick and dirty solution to provision.
You are welcome to report any bug, issue or reasonable request. As reasonable is subjective, I will decide what is reasonable and what is not :)
Pull request are MORE than welcome :)
