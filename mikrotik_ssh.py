# coding=utf-8

import argparse
import re
import socket
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException, SSHException


class MtControl(object): #TODO разобраться с закрытием переданного инстанса

    def __init__(self, address, port, username, password):
        self.address = address

        if port:
            self.port = port

        self.username = username
        self.password = password
        self.connection = self.connect()

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
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

        except SSHClient as e:
            return e

        # except NoValidConnectionsError:
        #     print('Connection error!')
        #
        # except AuthenticationException as e:
        #     raise e
        #     print('Authentication failed!')
        #
        # except SSHException:
        #     print('Error reading SSH protocol banner')

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
            # remove /r and /n
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
    parser.add_argument('-u', '--username', type=str, required=True, default='admin')
    parser.add_argument('-p', '--password', type=str, required=True)
    parser.add_argument('-c', '--command', type=str, required=True, nargs='+')

    args = parser.parse_args()

    port = 22

    mt_ssh = MtControl(args.address, port, args.username, args.password)
    mt_ssh.execute(args.command)
    mt_ssh.close()


if __name__ == '__main__':
    main()
