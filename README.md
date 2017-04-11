# Microtik SSH
Python script to send SSH command to Mikrotik device.

## Usage
mikrotik_ssh.py [-h] -a ADDRESS [--port PORT] [-u USERNAME] [-p PASSWORD] -c COMMAND [COMMAND ...]

optional arguments:

| Argument | Discription |
| ------ | ------ |
| -h, --help | show this help message and exit |
| -a, --address | Hostname or IP address of device |
| --port | Port to connect to on the remote host (default: 22) |
| -u, --username | User to connect to on the remote host (default: admin) |
|-p, --password | Password. Special characters must be escaped. (default: blank) |
| -c, --command | Command for execute |

example:
```sh
$python mikrotik_ssh.py -a 10.10.10.1 -p passw0RD\! -c 'system identity print'
```
or
```sh
$python mikrotik_ssh.py --address 10.10.10.1 --username admin --password passw0RD\! --command 'system identity print'
```
output:
```sh
$name: RT-01
```
