# coding=utf-8

import argparse
import re
import socket
try:
    from paramiko import SSHClient
    from paramiko import AutoAddPolicy
    from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException, SSHException
except ImportError:
    from paramiko import SSHClient
    print "Import error. Chech paramiko module."


class MtControl(object): #TODO разобраться с закрытием переданного инстанса

    def __init__(self, address, port, username, password):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.connection = self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    # def __del__(self):
    #     self.close()

    def connect(self):
        """
        If connection establish, return SSHClient instance
        :return SSHClient instance:
        """
        mt_ssh = SSHClient()
        mt_ssh.set_missing_host_key_policy(AutoAddPolicy())

        try:
            mt_ssh.connect(self.address, self.port, username=self.username, password=self.password, timeout=1)

        except NoValidConnectionsError:
            print('Connection error!')

        except AuthenticationException:
            print('Authentication failed!')

        except SSHException:
            print('Error reading SSH protocol banner')

        except socket.timeout:
            print('Connection timeout')

        else:
            return mt_ssh

    def execute(self, command):

        try:
            if isinstance(command, list):
                command = " ".join(command)  # TODO Попоравить конкатенацию

        except TypeError:
            print('Something wrong with your command!')

        stdin, stdout, stderr = self.connection.exec_command(command)

        stdout = stdout.readlines()
        output = ""

        for line in stdout:
            output = output + line

        if output != "":
            # rstrip() for remove /r and /n
            return output.rstrip()
        else:
            return None

    def get_name(self):
        """
        Get router name
        :return: Router name (string)
        """
        if self.connection is not None:
            rt_name = self.execute("/system identity print")
            rt_name = "".join(re.findall(r': (.+)', rt_name))
            return rt_name

    def close(self):
        if self.connection is not None:
            self.connection.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', type=str, required=True)
    parser.add_argument('--port', type=int, required=False, default=22)
    parser.add_argument('-u', '--username', type=str, required=False, default='admin')
    parser.add_argument('-p', '--password', type=str, required=False, default='')
    parser.add_argument('-c', '--command', type=str, required=True, nargs='+')

    args = parser.parse_args()

    with MtControl(args.address, args.port, args.username, args.password) as mt_ssh:
        try:
            mt_ssh.execute(args.command)
        except Exception:
            pass

if __name__ == '__main__':
    main()
