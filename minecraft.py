import boto
import otters.utils.credentials as uc
import otters.utils.slack as slack
import fabfile
import argparse
import time
import datetime
import pandas
import subprocess
import datetime
import dateutil.parser as dp

cred = uc.AuthTPT('AWS-aab')
ACCESS_KEY = cred.get_value('aws_access_key_id')
ACCESS_SECRET = cred.get_value('aws_secret_access_key')
INSTANCE_ID = 'i-e2eaab1b'
USERS = ['amit']

def notify_by_slack(msg, users=USERS):
    oSlack = slack.SlackMsg()

    channels = ["@%s" % u for u in users]
    return oSlack.send_msg(channels, msg)


def get_instance(boto_con, instance_id):
    """
    Synopsis: the get instance object for a EC2 instance given the id

    :param boto_con:
    :param instance_id:
    :return:
    """
    try:
        rsv = boto_con.get_all_instances(instance_ids=[instance_id]) # get reservations
        print rsv
        instance = rsv[0].instances[0] # get instance
        return instance
    except:
        return None


def instance_state(instance):
    return instance.state

def get_ec2_instance():
    boto_con = boto.connect_ec2(ACCESS_KEY, ACCESS_SECRET)
    instance = get_instance(boto_con, INSTANCE_ID)
    return instance

def get_minecraft_server_status(instance, port):

    # run this command to check if port is open
    # netcat -v -z -w 3 ec2-52-70-34-56.compute-1.amazonaws.com 25565

    command_str = """netcat -v -z -w 3 %s %d &> /dev/null && echo "running" || echo "stopped" """ % (instance.ip_address, port)
    command_str = """netcat -v -z -w 3 %s %d""" % (instance.ip_address, port)
    command = command_str.split(" ")

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output =  p.communicate()
    if 'open' in output[1]:
        return 'running'
    else:
        return 'stopped'

def get_minecraft_status():

    status_dict = dict()

    # check if instance is running
    instance = get_ec2_instance()
    instance_status = instance_state(instance)
    server_name = 'ec2 server on %s' % instance.ip_address
    status_dict[server_name] = dict()
    status_dict[server_name]['status'] =  instance_status

    if instance_status == 'running':
        uptime = ec2_uptime(instance)
        status_dict[server_name]['notes'] = 'running for %s' % uptime
    else:
        status_dict[server_name]['notes'] = ''

    # check which servers are running
    minecraft_port_list = [25565, 25566]
    notes_list = ['Aryana and Sabrina', 'Anika and Lea']

    for ii,port in enumerate(minecraft_port_list):
        if instance_status == 'running':

            server_status = get_minecraft_server_status(instance, port)
        else:
            server_status = 'stopped'
        server_name = 'minecraft on port %d' % port
        status_dict[server_name] = dict()
        status_dict[server_name]['status'] = server_status
        status_dict[server_name]['notes'] = notes_list[ii]

    df = pandas.DataFrame.from_dict(status_dict, 'index')
    df.sort_index(inplace=True)
    df.rename(columns={0: 'status'}, inplace=True)
    return df


def ec2_uptime(instance):

    launch_time = dp.parse(instance.launch_time)
    uptime = datetime.datetime.now(launch_time.tzinfo) - launch_time

    days = uptime.days
    hours = uptime.seconds / 60. / 60
    uptime_str = "%d day(s) and %.2f hours" % (days, hours)
    return(uptime_str)

def start_minecraft():
    print "starting minecraft ..."
    time.sleep(30)
    fabfile.start_minecraft()


def start_ec2():
    boto_con = boto.connect_ec2(ACCESS_KEY, ACCESS_SECRET)
    instance = get_instance(boto_con, INSTANCE_ID)

    if instance_state(instance) != "running":
        print "starting EC2 instance ..."
        instance = get_instance(boto_con, INSTANCE_ID)
        instance.start()

        while instance_state(instance) != "running":
            time.sleep(30) # wait 30 sec and test again
            instance.update()


def stop_ec2():
    print "stopping ec2 instance ..."
    boto_con = boto.connect_ec2(ACCESS_KEY, ACCESS_SECRET)
    instance = get_instance(boto_con, INSTANCE_ID)
    instance.stop()

    while instance_state(instance) != 'stopped':
        time.sleep(30)
        instance.update()


def stop_minecraft():
    pass



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--start", help="start ec2 instance and minecraft server", action='store_true')
    parser.add_argument("--stop", help="stop ec2 instance", action='store_true')
    parser.add_argument("--reboot", help="reboot ec2 instance and minecraft server", action='store_true')
    parser.add_argument("--restart", help="restart minecraft server", action='store_true')
    args = parser.parse_args()


    if args.start:
        start_ec2()
        start_minecraft()

        today = datetime.datetime.today()
        msg = "started ec2 and minecraft @ %s" % today
        notify_by_slack(msg)

    if args.stop:
        stop_ec2()

        today = datetime.datetime.today()
        msg = "stopped minecraft ec2 @ %s" % today
        notify_by_slack(msg)

    if args.reboot:
        stop_ec2()
        start_ec2()
        start_minecraft()

        today = datetime.datetime.today()
        msg = "rebooted minecraft ec2 @ %s" % today
        notify_by_slack(msg)

    if args.restart:
        stop_minecraft()
        start_minecraft()

        today = datetime.datetime.today()
        msg = "restarted minecraft @ %s" % today
        notify_by_slack(msg)







