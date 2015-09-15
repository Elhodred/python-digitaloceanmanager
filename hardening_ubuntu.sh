#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
apt-get -q -y install puppet git iptables-persistent
puppet module install puppetlabs-firewall
puppet module install saz-sudo

mkdir /root/git
cd /root/git
git clone https://github.com/Elhodred/linux_basic_setup.git
cd linux_basic_setup
sed -i 's/^profiles::basic_setup::sshd_port:.*$/profiles::basic_setup::sshd_port: {{{SSHD_PORT}}}/' hieradata/common.yaml
sed -i 's/^profiles::basic_setup::default_user:.*$/profiles::basic_setup::default_user: {{{DEFAULT_USER}}}/' hieradata/common.yaml
sed -i 's/^profiles::basic_setup::default_pwd:.*$/profiles::basic_setup::default_pwd: {{{DEFAULT_PASSWORD}}}/' hieradata/common.yaml
sed -i 's/^profiles::basic_setup::sshd_service:.*$/profiles::basic_setup::sshd_service: ssh/' hieradata/common.yaml

puppet apply -v --hiera_config=hiera.yaml -e "include roles::basic_setup" --modulepath=modules/:/etc/puppet/modules

