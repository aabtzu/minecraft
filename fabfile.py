import boto, urllib2
from   boto.ec2 import connect_to_region
from   fabric.api import env, run, cd, settings, sudo
from   fabric.api import parallel
import os
import sys
import pandas

SERVER_CONTROL_FILE = 'servers.csv'
df_servers = pandas.read_csv(SERVER_CONTROL_FILE)

HOME =  os.environ['HOME']

EC2_MINECRAFT = "ec2-52-70-34-56.compute-1.amazonaws.com"
#env.hosts = [EC2_MINECRAFT]
#env.user = 'ubuntu'
env.host_string="ubuntu@%s" % EC2_MINECRAFT
env.key_filename = HOME + '/.ssh/aryana13.pem'


def hello():
    print("Hello world!")

def test():
	run ('ls')

def start_minecraft():
	for ii, row in df_servers.iterrows():
		print ii, row['port'], row['desc']
		with cd('/home/ubuntu/%s' % row['path']):
			run('screen -S %s -d -m java -Xmx1024M -Xms1024M -jar minecraft_server.1.10.jar nogui & sleep 5;' % row['name'], pty=False)

def show_servers():
	for ii, row in df_servers.iterrows():
		print ii, row['port'], row['desc']


