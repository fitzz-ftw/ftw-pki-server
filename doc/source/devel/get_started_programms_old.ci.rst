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

>> def stub_getpass(prompt:str)->str:
...     print(prompt)
...     return "strenggeheim"

>>> cmd_line="--conf-file member_server.toml  "
>>> cmd_line += " -k mem-serv"
>>> cmd_line += " -dns www.secure.example.org"
>>> cmd_line += " www-admin@example.org"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf-file', 
    'member_server.toml',
    '-k', 'mem-serv',
    '-dns', 'www.secure.example.org',
    'www-admin@example.org']



.. !SECTION - Prepare

.. SECTION - Start programm

.. SECTION - Configuration

>>> from ftwpki.baselibs.toml_utils import toml2dn

>>> from ftwpki.baselibs.cli_parser import ServerClientCSRParser, ServerClientCSRProtocol

>>> from ftwpki.baselibs.configuration import BasePKIConfig

>>> from argparse import Namespace

>>> pre_parser = ServerClientCSRParser(add_help=False, allow_abbrev=False)
>>> pre_args , _ = pre_parser.parse_known_args(sys_argv)

>>> pki_name = Path(pre_args.conf_file).stem

>>> pre_conf = toml2dn(Path(pre_args.conf_file).read_text())
>>> pre_conf["pki_name"] = pki_name

>>> ca_parser: ServerClientCSRParser = ServerClientCSRParser()
>>> ca_parser.set_defaults(**pre_conf)

>>> args: ServerClientCSRProtocol = ca_parser.parse_args(sys_argv)
>>> args #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Namespace(countryName='DE', 
    stateOrProvinceName='', 
    localityName='Hamburg', 
    organizationName='Muster-Verband e.V.', 
    organizationalUnitName='Infrastruktur und Dienste', 
    commonName='intern.example.org', 
    dnsubject={'countryName': 'DE', 
        'organizationName': 'Muster-Verband e.V.', 
        'commonName': 'intern.example.org', 
        'localityName': 'Hamburg', 
        'organizationalUnitName': 'Infrastruktur und Dienste'}, 
    conf_file=...Path('member_server.toml'), 
    key_name='mem-serv', 
    pki_name='member_server', 
    privatdir='', 
    email='www-admin@example.org', 
    ip_addresses=[], 
    host_names=['www.secure.example.org'],
    password=None, 
    private_key='mem-serv.key.pem', 
    public_key='mem-serv.pub.pem')

>>> config:BasePKIConfig = BasePKIConfig(args.conf_file)
>>> config.set_config("server")

>>> config.current_configfile_entries #doctest: +NORMALIZE_WHITESPACE
{'private_keys': '#config#.private', 
 'zip': '#data#', 
 'certs': '#zip#', 
 'chains': '#zip#', 
 'config_path': '#config#', 
 'data_path': '#data#'}


.. !SECTION - Configuration

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
<Name(...CN=intern.example.org...)>


<Name(C=DE,ST=,L=Somewherecity,O=Fitzz TeXnik Welt,OU=IT-Security,CN=IT-Security Server)>

>>> from ftwpki.baselibs.core import create_csr_name


>>> server_csr: CertificateRequest = CertificateRequest(
...     subject = subject,
...     policy = ServerPolicy(),
... )

>>> server_csr #doctest: +NORMALIZE_WHITESPACE
CertificateRequest(subject=<Name(CN=intern.example.org,OU=Infrastruktur und Dienste,O=Muster-Verband e.V.,L=Hamburg,ST=,C=DE)>)




.. !SECTION - CSR Creation

.. SECTION - Keypair Creation

>>> priv, pub = generate_rsa_key_pair(passphrase=args.password, key_size=4096)


>>> priv #doctest: +ELLIPSIS
b'-----BEGIN PRIVATE KEY-...

>>> pub #doctest: +ELLIPSIS
b'-----BEGIN PUBLIC KEY---...

.. !SECTION - Keypair Creation


.. SECTION - Save private Key

>>> from ftwpki.baselibs.core import save_pem
>>> save_pem(priv, 
...     config.private_keys / args.private_key, 
...     is_private=True)

>> save_pem(pub, config.data_path /f"{args.public_key}", is_private=False)

.. !SECTION - Save private Key

.. SECTION - Save CSR

>>> san_args={"ip_addresses": args.ip_addresses, "dns_names": args.host_names}

>>> server_pem = server_csr.build(load_private_key_from_pem(
...    pem_data=priv, 
...    passphrase= args.password
... ),**san_args).get_pem()

>>> save_pem(server_pem, 
... Path(f"{args.pki_name + '.csr'}"), is_private=False)


.. !SECTION - Save CSR


.. SECTION - pki- Container

>>> from ftwpki.baselibs.package import PKIPackage

>>> pki_pack = PKIPackage()

>>> conf_file = Path(args.conf_file)
>>> pki_pack.additional_files[f"{args.pki_name}.id.toml"]=conf_file.read_bytes()

>>> pki_file = pki_pack.save(config.pki_path/ args.pki_name)

.. !SECTION - pki- Container

.. SECTION - Cleanup

>>> conf_file.unlink()

.. !SECTION - Cleanup


.. !SECTION - Stop programm

.. SECTION - Test existing keys


>>> (config.private_keys / args.private_key).is_file()
True


>>> (config.pki_path / args.pki_name ).with_suffix(".pki").is_file()
True


.. !SECTION - Test existing keys

.. SECTION - Load and read CSR

>>> from ftwpki.baselibs.core import load_csr_from_pem

>>> csr_obj = load_csr_from_pem(Path(f"{args.pki_name + '.csr'}").read_bytes()) 

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

>>> env.clean_home()
>>> env.teardown()


.. !SECTION - Teardown
