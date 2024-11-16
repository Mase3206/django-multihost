# Django MultiHost

> [!NOTE]
> **GROUPS!** See [instructions.md](docs/instructions.md) for deployment instructions.

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
- PyYAML

## Installing

1. Clone this repo to /django/source
```bash
git clone https://github.com/mase3206/django-multihost.git /django/source
```
2. Navigate to /django/source via `cd`
3. Run `sudo make groups` to set up the necessary groups for your user
	- adds your user to the 'docker' group
	- creates and adds your user to the 'classadmin' group
4. Run `sudo make install` to:
	- set permissions
	- create symlinks for 'deploy.py' to `deploy` and 'create-group.sh' to `create-group`


## Removing

1. Navigate to /django/source via `cd`
2. Run `sudo make remove` to:
	- remove symlinks
3. Delete the /django/source folder, if desired.


## Licensing

This code is licensed under the GPLv3 license. See [LICENSE](./LICENSE) for more details.
