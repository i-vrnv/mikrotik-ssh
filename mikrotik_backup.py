# coding=utf-8
import ConfigParser
import mikrotik_ssh
import time
from ftplib import FTP

config = ConfigParser.ConfigParser()
# TODO Написать проверку для чтения файла конфигурации
config.read('config.ini')

ftp_host = config.get('ftp', 'host')
ftp_port = config.get('ftp', 'port')
ftp_username = config.get('ftp', 'username')
ftp_password = config.get('ftp', 'password')

ftp = FTP(host=ftp_host, user=ftp_username, passwd=ftp_password)


class Config(object):

    ftp_host = None
    ftp_port = None
    ftp_username = None
    ftp_password = None

    def __init__(self, ):
        self.parse()

    def parse(self):
        config = ConfigParser.ConfigParser()
        # TODO Написать проверку для чтения файла конфигурации
        config.read('config.ini')

        self.ftp_host = config.get('ftp', 'host')
        self.ftp_port = config.get('ftp', 'port')
        self.ftp_username = config.get('ftp', 'username')
        self.ftp_password = config.get('ftp', 'password')


def ftp_check_directory(directory): #TODO Работает, офоромить код правильно. Избавиться от дублирования кода
    """
    Checking backup directory. Creating it, if does not exist
    :param directory: /Example/input/directory
    :return:
    """

    if directory != "":
        try:
            ftp.cwd(directory)
        except Exception: #TODO Вписать нужное исключение или переписать на if else
            ftp_check_directory("/".join(directory.split("/")[:-1]))
            ftp.mkd(directory)
            ftp.cwd(directory)


def backup():
    #walk thru all sections
    for section in config.sections():
        if section != 'general' and section != 'ftp':
            mt_host = config.get(section, 'host')
            mt_port = int(config.get(section, 'port'))
            mt_username = config.get(section, 'username')
            mt_password = config.get(section, 'password')
            ftp_path = config.get(section, 'path')

            with mikrotik_ssh.MtControl(mt_host, mt_port, mt_username, mt_password) as rt:
                rt_name = rt.get_name()
                now_time = time.strftime("%d-%m-%Y");
                full_name = "{0}-{1}".format(rt_name, now_time)

                rt.execute("/system backup save dont-encrypt=yes name={0}".format(full_name))

                rt.execute(
                    '/tool fetch address={0} port={1} user={2} password={3} '
                    'mode=ftp src-path={5}.backup dst-path={4}/{5}.backup upload=yes'.format(
                        ftp_host, ftp_port, ftp_username, ftp_password, ftp_path, full_name))

                rt.execute("/file remove {0}".format(full_name))


if __name__ == '__main__':
    backup()
