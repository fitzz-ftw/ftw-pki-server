The Certificat Sign Request Creation
#########################################




.. SECTION - Setup
>>> test_data_pre= "test_ok_data"

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)
>>> env.clean_home()

.. !SECTION - Setup
.. SECTION - Prepare

>>> from pathlib import Path

>>> conf_file = env.copy2cwd(f"{test_data_pre}/leaf_server_members_conf.toml", "member_server.toml")

>>> def stub_exception(*args):
...     raise Exception("This is a testexception")

>>> cmd_line="--conf-file member_server.toml  "
>>> cmd_line += " -k mem-serv"
>>> cmd_line += " -hn www.secure.example.org"
>>> cmd_line += " www-admin@example.org"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf-file', 
    'member_server.toml',
    '-k', 'mem-serv',
    '-hn', 'www.secure.example.org',
    'www-admin@example.org']

>>> import ftwpki.server.programms_DEV as testing

.. !SECTION - Prepare

>>> from ftwpki.server.programms_DEV import prog_server_csr

>>> prog_server_csr(sys_argv)
0

>>> conf_file = env.copy2cwd(f"{test_data_pre}/leaf_server_members_conf.toml", "member_server.toml")

>>> testing.toml2dn = stub_exception

>>> prog_server_csr(sys_argv)
Error: This is a testexception
1

.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()


.. !SECTION - Teardown
