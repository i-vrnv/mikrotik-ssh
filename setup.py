from setuptools import setup

setup(
   name='mikrotik-ssh',
   version='0.1',
   description='Python script to send SSH command to Mikrotik device.',
   author='Ignatiy Voronov',
   author_email='ignatiy.voronov@gmail.com',
   url='https://github.com/voronovim/mikrotik-ssh',
   packages=['mikrotik-ssh'],
   install_requires=['paramiko'],
)