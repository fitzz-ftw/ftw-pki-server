# Changelog: ftw-pki-server

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2026-06-18

### Added
- Finalize server module and core functionality
- Introduce temporary DEV server assets and testing configurations

### Changed
- Migrate server architecture to CSRWorkflow pattern
- Integrate TomlPreParser into server CSR program
- Rename legacy TOML functions to modernize utility interfaces
- Update configuration flags and clean up imports

### Fixed
- Update CLI flags and improve error handling for server CSR

### Testing
- Achieve 100% total test coverage for the server component

### Removed
- Remove deprecated get_started documentation files

## [0.0.1a1] - 2026-05-18

### Added
- Integrate local `LeafPKIConfig` to replace global `platformdirs` mechanics for secure, dynamic server path evaluation.
- Document the `prog_server_csr` command-line entry point with a comprehensive, Sphinx-compliant English docstring.
- Add a fail-fast switch (`FAIL_FAST`) to the main local doctest execution runner, featuring short-circuit termination and a progress tracking summary.

### Changed
- **Breaking Change**: Drop the explicit `--private-dir` command-line override; the private storage location is now inferred dynamically through core configuration paths.
- Enforce explicit and secure `.pem` file extensions (`.key.pem` and `config.ext_public`) for all freshly generated server keypairs.
- Update sequence diagram assets and reference guides to adapt to the architectural renaming of `ftwpkireceiver` to `ftwpkiunpacker`.
- Lower the project development status metadata from Beta to Alpha inside `pyproject.toml`.

### Removed
- Remove the unused `platformdirs` intersphinx mapping block from the Sphinx documentation build setup (`conf.py`).
