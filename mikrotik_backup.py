from mikrotik_ssh import MtConnection;
import re
import time


def main():
    mtConn = MtConnection('10.10.10.1', 22, 'admin', '!T3aM$28485569')
    name = mtConn.get_name()


if __name__ == '__main__':
    main()
