# Web Dev Host

> [!NOTE]
> **USERS!** See [instructions.md](./instructions.md) for deployment instructions.

This is a set of helpful wrapper scripts and Docker configurations to self-host a multi-site Django server.

## Installing

1. Clone this repo to /django/source
```bash
git clone https://github.com/mase3206/web-dev-host.git /django/source
```
2. Navigate to /django/source via `cd`
3. Run `make groups` to set up the necessary groups for your user
	- adds your user to the 'docker' group
	- creates and adds your user to the 'classadmin' group
4. Run `make install` to:
	- install dependencies
	- set permissions
	- create symlinks for 'deploy.py' to `deploy` and 'create-group.sh' to `create-group`


## Removing

1. Navigate to /django/source via `cd`
2. Run `make remove` to:
	- remove symlinks
3. Delete the /django/source folder, if desired.


## Licensing

This code is licensed under the GPLv3 license. See [LICENSE](./LICENSE) for more details.