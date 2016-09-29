import sys
import argparse
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', type=str, required=True)
parser.add_argument('-u', '--username', type=str, required=True,default='admin')
parser.add_argument('-p', '--password', type=str, required=True)
parser.add_argument('-c', '--command', type=str, required=True, nargs='+')

args = parser.parse_args()

port = 22

mtCli = SSHClient()
mtCli.set_missing_host_key_policy(AutoAddPolicy())

try:
    mtCli.connect(args.address, port, username=args.username, password=args.password)
    print('Connection successful!')

    try:
        cmd = ""
        cmd = " ".join(args.command)
    except TypeError:
        print('Something wrong with your command!')

    stdin, stdout, stderr = mtCli.exec_command(cmd)

    stdout = stdout.readlines()
    output = ""

    for line in stdout:
        output = output+line
    if output != "":
        print output
    else:
        print('Output is empty')

except NoValidConnectionsError:
    print('Connection error!')

except AuthenticationException:
    print('Authentication failed!')

finally:
    mtCli.close()
