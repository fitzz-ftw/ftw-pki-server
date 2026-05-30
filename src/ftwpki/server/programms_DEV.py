# File: src/ftwpki/server/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Modul programms documentation
"""

from pathlib import Path

from cryptography import x509

from ftwpki.baselibs.cert_request import CertificateRequest
from ftwpki.baselibs.cli_parser import (
    ServerClientCSRParser_DEV,
    ServerClientCSRProtocol,
)
from ftwpki.baselibs.configuration import BasePKIConfig_DEV, PKIPackage
from ftwpki.baselibs.core import (
    create_distinguished_name,
    generate_rsa_key_pair,
    load_private_key_from_pem,
    save_pem,
)
from ftwpki.baselibs.policies import ServerPolicy
from ftwpki.baselibs.toml_utils import toml2dn


def prog_server_csr(argv: list[str] | None = None,**kwargs) -> int:
    """
    Execute the server Certificate Signing Request (CSR) generation process.

    This function processes command-line arguments to generate a new
    private key and a corresponding CSR for the server infrastructure.

    :param argv: Optional list of command-line arguments. If None, sys.argv is used.
    :param kwargs: Additional keyword arguments for internal configuration overrides.
    :returns: The exit status code (0 for success, non-zero for errors).
    """
    try:
        # SECTION - Configuration
        pre_parser  = ServerClientCSRParser_DEV(add_help=False, allow_abbrev=False)
        pre_args, _ = pre_parser.parse_known_args(argv)
        pki_name = Path(pre_args.conf_file).stem
        pre_conf = toml2dn(pre_args.conf_file)
        pre_conf["pki_name"] = pki_name
        ca_parser: ServerClientCSRParser_DEV = ServerClientCSRParser_DEV(**kwargs)
        ca_parser.set_defaults(**pre_conf)
        args: ServerClientCSRProtocol = ca_parser.parse_args(argv)
        config: BasePKIConfig_DEV = BasePKIConfig_DEV(args.conf_file)
        config.set_config("server")
        # !SECTION - Configuration
        # SECTION - CSR Creation
        subject: x509.Name = create_distinguished_name(
            country=args.countryName,
            state=args.stateOrProvinceName,
            location=args.localityName,
            organization=args.organizationName,
            common_name=args.commonName,
            organizational_unit=args.organizationalUnitName,
        )
        server_csr: CertificateRequest = CertificateRequest(
            subject=subject,
            policy=ServerPolicy(),
        )

        # !SECTION - CSR Creation
        # SECTION - Keypair Creation
        priv, pub = generate_rsa_key_pair(passphrase=args.password, key_size=4096) 

        # !SECTION - Keypair Creation
        # SECTION - Save private Key
        save_pem(priv, 
                 config.private_keys/args.private_key, 
                 is_private=True)
        # !SECTION - Save private Key

        # SECTION - Save CSR

        san_args={"ip_addresses": args.ip_addresses, "dns_names": args.host_names}

        server_pem = server_csr.build(
                load_private_key_from_pem(pem_data=priv, passphrase=args.password),
                **san_args,
            ).get_pem()
        save_pem(server_pem, 
                 Path(f"{args.pki_name + '.csr'}"), 
                 is_private=False)
        # !SECTION - Save CSR
        # SECTION - pki- Container
        pki_pack = PKIPackage()
        conf_file = Path(args.conf_file)
        pki_pack.additional_files[f"{args.pki_name}.id.toml"]=conf_file.read_bytes()
        _ = pki_pack.save(config.pki_path/ args.pki_name)
        # !SECTION - pki- Container
        # SECTION - Cleanup
        conf_file.unlink()
        # !SECTION - Cleanup
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":  # pragma: no cover
    from doctest import FAIL_FAST, testfile

    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    passed_files = 0
    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_files = [
        # "get_started_programms.ci.rst",
        # "get_started_programms_DEV.ci.rst",
        "get_started_run_programms_DEV.ci.rst",
        # "get_started_run_programms.ci.rst",
    ]
    for file in test_files:
        test_file = testfiles_dir / file
        if test_file.exists():
            print(f"--- Running Doctest for {test_file.name} ---")
            doctestresult = testfile(
                str(test_file),
                module_relative=False,
                verbose=be_verbose,
                optionflags=option_flags,
            )
            test_failed += doctestresult.failed
            test_sum += doctestresult.attempted
            if doctestresult.failed > 0 and option_flags & FAIL_FAST:
                print(f"Doctest result for {test_file.name}: {doctestresult}")
                print(
                    f"\nKeep going! You already passed {passed_files} files "
                    f"with {test_sum} tests before this hit."
                )
                break  # Stop on first failure if FAIL_FAST is set
            passed_files += 1
        else:
            print(f"⚠️ Warning: Test file {test_file.name} not found.")
    if test_failed == 0:
        print(f"\nDocTests passed without errors, {test_sum} tests.")
    else:
        if not option_flags & FAIL_FAST:
            print(f"\nDocTests failed: {test_failed} tests out of {test_sum}.")
