# coding=utf-8

import argparse
import re
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException


class MtConnection:
    def __init__(self, address, port, username, password):
        self.address = address
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        mt_ssh = SSHClient()
        mt_ssh.set_missing_host_key_policy(AutoAddPolicy())

        try:
            mt_ssh.connect(self.address, self.port, username=self.username, password=self.password)

        except NoValidConnectionsError:
            print('Connection error!')

        except AuthenticationException:
            print('Authentication failed!')

        return mt_ssh

    def send(self, command):

        mt_ssh = self.connect()
        mt_ssh.exec_command(command)

        try:
            if isinstance(command, list):
                command = " ".join(command)  # TODO Попоравить конкатенацию

        except TypeError:
            print('Something wrong with your command!')

        stdin, stdout, stderr = mt_ssh.exec_command(command)

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
        :return: string
        """
        command = "/system identity print"
        rt_name = self.send(command)
        rt_name = "".join(re.findall(r': (.+)', rt_name))

        return rt_name


def send_cmd(address, port, username, password, command):
    # TODO Сделать нормальный обработчик port

    mtCli = MtConnection(address, port, username, password)
    mtCli.set_missing_host_key_policy(AutoAddPolicy())

    try:
        mtCli.connect(address, port, username=username, password=password)
        # print('Connection successful!')

        # TODO Проверить, работает ли try catch
        try:
            if isinstance(command, list):
                command = " ".join(command)  # TODO Попоравить конкатенацию

        except TypeError:
            print('Something wrong with your command!')

        stdin, stdout, stderr = mtCli.exec_command(command)

        stdout = stdout.readlines()

        output = ""

        for line in stdout:
            output = output + line

        if output != "":
            # remove /r and /n
            return output.rstrip()

        else:
            print('Output is empty')

    except NoValidConnectionsError:
        print('Connection error!')

    except AuthenticationException:
        print('Authentication failed!')

    finally:
        mtCli.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', type=str, required=True)
    parser.add_argument('-u', '--username', type=str, required=True, default='admin')
    parser.add_argument('-p', '--password', type=str, required=True)
    parser.add_argument('-c', '--command', type=str, required=True, nargs='+')

    args = parser.parse_args()

    port = 22

    send_cmd(args.address, port, args.username, args.password, args.command)


if __name__ == '__main__':
    main()
