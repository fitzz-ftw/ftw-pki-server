The Certificat Sign Request Creation
#########################################




.. SECTION - Setup
>>> test_data_pre= "data-server"

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"),
...     appname="ftwpki", appauthor="FitzzTeXnikWelt")

>>> env.setup(True)
>>> env.clean_home()

.. !SECTION - Setup
.. SECTION - Prepare

>>> from pathlib import Path

>>> conf_file = env.copy2cwd(f"{test_data_pre}/M-V-HH-Members.toml", "M-V-HH-Members.toml")

>> def stub_getpass(prompt:str)->str:
...     print(prompt)
...     return "strenggeheim"

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



.. !SECTION - Prepare


>>> from ftwpki.baselibs.workflows import CSRWorkflow
>>> from ftwpki.baselibs.policies import BasePolicy, ServerPolicy


.. SECTION - Start programm


.. SECTION - Configuration
>>> csr_creator = CSRWorkflow()
>>> csr_creator.policy = ServerPolicy()
>>> csr_creator.mandantory_san = True
>>> csr_creator.configuration(sys_argv)


.. !SECTION - Configuration

.. SECTION - CSR Creation

>>> csr_creator.csr_creation()

.. !SECTION - CSR Creation

.. SECTION - Keypair Creation

>>> csr_creator.key_pair_creation()

.. !SECTION - Keypair Creation


.. SECTION - Save private Key
>>> csr_creator.save_keys()

.. !SECTION - Save private Key

.. SECTION - Save CSR
>>> csr_creator.save_csr()


.. !SECTION - Save CSR


.. SECTION - pki- Container
>>> csr_creator.process_pki_container()


.. !SECTION - pki- Container

.. SECTION - Cleanup

>>> csr_creator.cleanup()

.. !SECTION - Cleanup


.. !SECTION - Stop programm

.. SECTION - Test existing keys

>>> conf_path:Path = env.config_dir
>>> public_path:Path = env.data_dir


>>> (conf_path/ ".private" / "mem-serv.key.pem").is_file()
True


>>> (public_path / "M-V-HH-Members" ).with_suffix(".pki").is_file()
True


.. !SECTION - Test existing keys

.. SECTION - Load and read CSR

>>> from ftwpki.baselibs.core import load_csr_from_pem

>>> pki_name = "M-V-HH-Members"

>>> csr_obj = load_csr_from_pem(Path(f"{pki_name + '.csr'}").read_bytes()) 

>>> csr_obj #doctest: +ELLIPSIS
<cryptography.hazmat.bindings._rust.x509.CertificateSigningRequest object at ...>

>>> from ftwpki.baselibs.core import get_subject_dict

>>> get_subject_dict(csr_obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{'countryName': 'DE', 
 'stateOrProvinceName': '', 
 'localityName': 'Hamburg', 
 'organizationName': 'Muster-Verband e.V.', 
 'organizationalUnitName': 'Infrastruktur und Dienste', 
 'commonName': 'intern.example.org'}

.. !SECTION - Load and read CSR



.. SECTION - Teardown

>> env.clean_home()
>>> env.teardown()


.. !SECTION - Teardown
