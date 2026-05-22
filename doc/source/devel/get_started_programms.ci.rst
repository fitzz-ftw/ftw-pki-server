The Certificat Sign Request Creation
#########################################




.. SECTION - Setup

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)
>>> env.clean_home()

.. !SECTION
.. SECTION - Prepare

>>> from pathlib import Path

>> test_paswd_path = env.copy2cwd("privat/testpasswd")
>>> conf_file = env.copy2cwd("csr_server_conf.toml")

>> def getpasswd(prompt:str)->str:
...     print(prompt)
...     return "strenggeheim"

>>> cmd_line="--conf-file csr_server_conf.toml  "
>>> cmd_line += " -hn www.secure.example.org"
>>> cmd_line += " www-admin@example.org"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf-file', 
    'csr_server_conf.toml', 
    '-hn', 'www.secure.example.org',
    'www-admin@example.org']



.. !SECTION

.. SECTION - Start programm

.. SECTION - Configuration

>>> from ftwpki.baselibs.toml_utils import toml2_dn

>>> from ftwpki.baselibs.cli_parser import ServerClientCSRParser, ServerClientCSRProtocol

>>> from ftwpki.baselibs.configuration import LeafPKIConfig

>>> from argparse import Namespace

>>> config:LeafPKIConfig = LeafPKIConfig()
>>> config.set_config("server")

>>> from typing import Any
>>> file_conf:dict[str,Any]={"privatdir":config.private_keys.relative_to(config.config_path).as_posix(),}

>>> default_namespace:Namespace=Namespace()
>>> default_namespace.password = None

>>> ca_parser: ServerClientCSRParser = ServerClientCSRParser()

>>> ca_parser.set_defaults(**toml2_dn(sys_argv))
>>> ca_parser.set_defaults(**file_conf)

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
    key_name='', 
    privatdir='.private', 
    email='www-admin@example.org', 
    ip_addresses=[], 
    host_names=['www.secure.example.org'], 
    private_key='', 
    public_key='')

.. !SECTION - Configuration

.. SECTION - Passwordhandling

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

>>> args.private_key = args.private_key if args.private_key else str(Path(csr_file_name).with_suffix(".key.pem"))

>>> args.public_key = args.public_key if args.public_key else str(Path(csr_file_name).with_suffix(config.ext_public))

.. !SECTION - Keypair Creation

.. SECTION - Save Keys and CSR

>>> from ftwpki.baselibs.core import save_pem
>>> save_pem(priv, 
...     config.config_path / f"{args.privatdir}/{args.private_key}", 
...     is_private=True)
>>> save_pem(pub, config.data_path /f"{args.public_key}", is_private=False)

>>> san_args={"ip_addresses": args.ip_addresses, "dns_names": args.host_names}

>>> save_pem(server_csr.build(load_private_key_from_pem(pem_data=priv, passphrase= args.password
... ),**san_args).get_pem(), 
... Path(csr_file_name), is_private=False)

.. !SECTION - Save Keys and CSR

.. !SECTION - Stop programm

.. SECTION - Test existing keys

>>> conf_path:Path = config.config_path
>>> public_path:Path = config.data_path

>>> (conf_path / ".private"/ "IT-Security-Server.key.pem").is_file()
True

>>> (public_path / "IT-Security-Server.pub.pem").is_file()
True


.. !SECTION - Test existing keys

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

>> env.clean_home()
>>> env.teardown()

.. !SECTION - Teardown
