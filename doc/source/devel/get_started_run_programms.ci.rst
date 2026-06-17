The Certificat Sign Request Creation
#########################################




.. SECTION - Setup
>>> test_data_pre= "data-server"

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)
>>> env.clean_home()

.. !SECTION - Setup
.. SECTION - Prepare

>>> from pathlib import Path

>>> conf_file = env.copy2cwd(f"{test_data_pre}/M-V-HH-Members.toml", "M-V-HH-Members.toml")

>>> def stub_exception(*args,**kwargs):
...     raise Exception("This is a testexception")

>>> cmd_line="--conf-file M-V-HH-Members.toml  "
>>> cmd_line += " -k mem-serv"
>>> cmd_line += " -dns www.secure.example.org"
>>> cmd_line += " www-admin@example.org"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf-file', 
    'M-V-HH-Members.toml',
    '-k', 'mem-serv',
    '-dns', 'www.secure.example.org',
    'www-admin@example.org']

>>> import ftwpki.baselibs.workflows as testing

.. !SECTION - Prepare

>>> from ftwpki.server.programms import prog_server_csr

>>> prog_server_csr(sys_argv)
0

>>> cmd_line = " -k mem-serv"
>>> cmd_line += " -dns www.secure.example.org"
>>> cmd_line += " www-admin@example.org"

>>> sys_argv= shlex.split(cmd_line) 

>>> prog_server_csr(sys_argv)
Error: the following arguments are required: --conf-file
1

>>> cmd_line="--conf-file M-V-HH-Members.toml  "
>>> cmd_line += " -k mem-serv"
>>> cmd_line += " -dns www.secure.example.org"
>>> cmd_line += " www-admin@example.org"

>>> sys_argv= shlex.split(cmd_line) 


>>> conf_file = env.copy2cwd(f"{test_data_pre}/M-V-HH-Members.toml", "M-V-HH-Members.toml")

>>> testing.generate_rsa_key_pair = stub_exception

>> testing.generate_rsa_key_pair

>>> prog_server_csr(sys_argv)
Error: This is a testexception
1

.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()


.. !SECTION - Teardown
