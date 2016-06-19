import boto, urllib2
from   boto.ec2 import connect_to_region
from   fabric.api import env, run, cd, settings, sudo
from   fabric.api import parallel
import os
import sys

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
    with cd('/home/ubuntu/minecraft10'):
        run('screen -S aryana -d -m java -Xmx1024M -Xms1024M -jar minecraft_server.1.10.jar nogui', pty=False)
    with cd('/home/ubuntu/minecraft'):
        run('screen -S anika -d -m java -Xmx1024M -Xms1024M -jar minecraft_server.1.10.jar nogui', pty=False)


