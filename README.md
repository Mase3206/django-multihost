# Django MultiHost

> [!NOTE]
> **GROUPS!** See [instructions.md](instructions.md) for deployment instructions.

This is a set of helpful wrapper scripts and Docker configurations to self-host a multi-site Django server.

**We have a wiki now!** It goes a bit more in depth than this README does, so [take a look at it](https://github.com/Mase3206/web-dev-host/wiki) if you're curious.

## Requirements
### System
- Python 3.12+
- Python Pip
- [jq](https://jqlang.github.io/jq/)
- Git
- [Docker CE](https://docs.docker.com/desktop/setup/install/linux/)
- [pwgen](https://pkgs.org/search/?q=pwgen) - found in the EPEL repos in RHEL-based distros
- make

### Python
Make sure to install these system-wide!
- PyYAML

## Known Issues
- Whitenoise version 6.8 or newer defined in the requirements.txt file is required for static files to be served correctly (or at all) - [Issue #5](https://github.com/Mase3206/django-multihost/issues/5)

## Installing

1. Clone this repo to /django/source
```bash
git clone https://github.com/mase3206/django-multihost.git /django/source
```
2. Navigate to /django/source via `cd`
> [!WARNING]
> Do not run the following commands as root! Doing so will result in broken permissions. Run them as yourself and enter your password when prompted.
3. Run `make groups` to set up the necessary groups for your user
	- adds your user to the 'docker' group
	- creates and adds your user to the 'classadmin' group
4. Run `make install` to:
	- set permissions
	- create symlinks for 'deploy.py' to `deploy` and 'create-group.sh' to `create-group`


## Removing

1. Navigate to /django/source via `cd`
2. Run `make remove` to:
	- remove symlinks
3. Delete the /django/source folder, if desired.


## Licensing

This code is licensed under the GPLv3 license. See [LICENSE](./LICENSE) for more details or [TL;DR Legal](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3) for a rundown.
