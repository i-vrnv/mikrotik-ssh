import sys
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException

host = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
cmd = ""

for args in sys.argv[4:]:
    cmd=cmd + str(args) + " "

port = 22

mtCli = SSHClient()
mtCli.set_missing_host_key_policy(AutoAddPolicy())

try:
    mtCli.connect(str(host), port, username=str(user), password=str(password))
    stdin, stdout, stderr = mtCli.exec_command(cmd)

    stdout = stdout.readlines()
    output = ""

    for line in stdout:
        output=output+line
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