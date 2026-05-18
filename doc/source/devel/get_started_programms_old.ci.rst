:orphan:

The Certificat Sign Request Creation
#########################################




.. SECTION - Setup

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)

.. !SECTION
.. SECTION - Prepare

>>> from pathlib import Path
>>> private_dir:Path = Path("privat")
>>> private_dir.mkdir(parents=True, exist_ok=True)

>> test_paswd_path = env.copy2cwd("privat/testpasswd")
>>> conf_file = env.copy2cwd("csr_server_conf.toml")

>> def getpasswd(prompt:str)->str:
...     print(prompt)
...     return "strenggeheim"

>>> cmd_line="--conf_file csr_server_conf.toml  "
>>> cmd_line += " --private-dir privat"
>>> cmd_line += " -hn www.secure.example.org"
>>> cmd_line += " www-admin@example.org"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf_file', 
    'csr_server_conf.toml', 
    '--private-dir', 'privat', 
    '-hn', 'www.secure.example.org',
    'www-admin@example.org']

.. !SECTION

.. SECTION - Start programm

.. SECTION - Configuration

>>> from ftwpki.baselibs.toml_utils import toml2dn

>>> from ftwpki.baselibs.cli_parser import ServerClientCSRParser, ServerClientCSRProtocol

>>> from argparse import Namespace

>>> default_namespace:Namespace=Namespace()
>>> default_namespace.password = None

>>> ca_parser: ServerClientCSRParser = ServerClientCSRParser()
>>> ca_parser.set_defaults(**toml2dn(sys_argv))
>>> args: ServerClientCSRProtocol = ca_parser.parse_args(sys_argv,default_namespace)
>>> args #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS 
Namespace(password=None, 
    countryName='DE', 
    stateOrProvinceName='', 
    localityName='Somewherecity', 
    organizationName='Fitzz TeXnik Welt', 
    organizationalUnitName='IT-Security', 
    commonName='IT-Security Server', 
    dnsubject={'countryName': 'DE', 
        'organizationName': 'Fitzz TeXnik Welt', 
        'commonName': 'IT-Security Server', 
        'localityName': 'Somewherecity', 
        'organizationalUnitName': 'IT-Security'}, 
    conf_file=...Path('csr_server_conf.toml'), 
    private_key='', 
    public_key='', 
    privatdir='privat', 
    email='www-admin@example.org', 
    ip_addresses=[], 
    host_names=['www.secure.example.org'])

.. !SECTION - Configuration

.. SECTION - Passwordhandling


>> from ftwpki.baselibs.passwd import PasswordManager
>> pwd_man = PasswordManager(private_dir=args.privatdir)
>> pwd_man
PasswordManager(private_dir='privat')

.. !SECTION - Passwordhandling

.. SECTION - CSR Creation

>>> from ftwpki.baselibs.cert_request import CertificateRequest
>>> from ftwpki.baselibs.policies import ServerPolicy
>>> from ftwpki.baselibs.core import (
...         create_distinguished_name,
...         load_private_key_from_pem, 
...         generate_rsa_key_pair,
...         )

>>> from cryptography import x509

>>> subject: x509.Name = create_distinguished_name(
...     country=args.countryName,
...     state=args.stateOrProvinceName,
...     location=args.localityName,
...     organization=args.organizationName,
...     common_name=args.commonName,
...     organizational_unit=args.organizationalUnitName,
... )

>>> subject #doctest: +ELLIPSIS
<Name(...)>

<Name(C=DE,ST=,L=Somewherecity,O=Fitzz TeXnik Welt,OU=IT-Security,CN=IT-Security Server)>

>>> from ftwpki.baselibs.core import create_csr_name

>>> csr_file_name: str = create_csr_name(args.commonName)

>>> csr_file_name
'IT-Security-Server.csr'


>>> server_csr: CertificateRequest = CertificateRequest(
...     subject = subject,
...     policy = ServerPolicy(),
... )

>>> server_csr #doctest: +NORMALIZE_WHITESPACE
CertificateRequest(subject=<Name(CN=IT-Security Server,OU=IT-Security,O=Fitzz TeXnik Welt,L=Somewherecity,ST=,C=DE)>)


.. !SECTION - CSR Creation

.. SECTION - Keypair Creation

>>> priv, pub = generate_rsa_key_pair(passphrase=args.password, key_size=4096)


>>> priv #doctest: +ELLIPSIS
b'-----BEGIN PRIVATE KEY-...

>>> pub #doctest: +ELLIPSIS
b'-----BEGIN PUBLIC KEY---...

>>> args.private_key = args.private_key if args.private_key else str(Path(csr_file_name).with_suffix(".key"))

>>> args.public_key = args.public_key if args.public_key else str(Path(csr_file_name).with_suffix(".pub"))

.. !SECTION - Keypair Creation

.. SECTION - Save Keys and CSR

>>> from ftwpki.baselibs.core import save_pem
>>> save_pem(priv, 
...     Path(f"{args.privatdir}/{args.private_key}"), 
...     is_private=True)
>>> save_pem(pub, Path(f"{args.public_key}"), is_private=False)

>>> san_args={"ip_addresses": args.ip_addresses, "dns_names": args.host_names}

>>> save_pem(server_csr.build(load_private_key_from_pem(pem_data=priv, passphrase= args.password
... ),**san_args).get_pem(), 
... Path(csr_file_name), is_private=False)

.. !SECTION - Save Keys and CSR

.. !SECTION - Stop programm

.. SECTION - Load and read CSR

>>> from ftwpki.baselibs.core import load_csr_from_pem

>>> csr_obj = load_csr_from_pem(Path(csr_file_name).read_bytes()) 

>>> csr_obj #doctest: +ELLIPSIS
<cryptography.hazmat.bindings._rust.x509.CertificateSigningRequest object at ...>

>>> from ftwpki.baselibs.core import get_subject_dict

>>> get_subject_dict(csr_obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{'countryName': 'DE', 
 'stateOrProvinceName': '', 
 'localityName': 'Somewherecity', 
 'organizationName': 'Fitzz TeXnik Welt', 
 'organizationalUnitName': 'IT-Security', 
 'commonName': 'IT-Security Server'}

.. !SECTION - Load and read CSR


.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION - Teardown
