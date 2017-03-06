Python script to send SSH command to Mikrotik device.

usage: mikrotik_ssh.py [-h] -a ADDRESS [--port PORT] [-u USERNAME] [-p PASSWORD] -c COMMAND [COMMAND ...]

optional arguments:
    -h, --help                show this help message and exit
    -a ADDRESS, --address     Hostname or IP address of device
    --port                    Port to connect to on the remote host (default: 22)
    -u USERNAME, --username   User to connect to on the remote host (default: admin)
    -p PASSWORD, --password   Password. Special characters must be escaped. (default: blank)
    -c COMMAND [COMMAND ...], --command COMMAND [COMMAND ...]

example:

    python mikrotik_ssh.py -a 10.10.10.1 -p passw0RD\! -c 'system identity print'
    python mikrotik_ssh.py --address 10.10.10.1 --username admin --password passw0RD\! --command 'system identity print'

output:
    name: RT-01
