fulfill
==============================

__Version:__ 0.0.0

Assignment for fulfill

## Getting up and running

Minimum requirements: **pip, python3.7, redis & [PostgreSQL 11][install-postgres]**, setup is tested on Mac OSX only.

```
brew install python3 libmagic postgres 
```

[install-postgres]: http://www.gotealeaf.com/blog/how-to-install-postgresql-on-a-mac

In your terminal, type or copy-paste the following:

    git clone git@github.com:ShubhamBansal1997/fulfill-web.git; cd fulfill-web; make install

Go grab a cup of coffee, we bake your hot development machine.

Useful commands:

- `make run` - start [django server](http://localhost:8000/)
- `make deploy_docs` - deploy docs to server
- `make test` - run the test locally with ipdb

**NOTE:** Checkout `Makefile` for all the options available and how they do it.


## Deploying Project

The deployment are managed via travis, but for the first time you'll need to set the configuration values on each of the server.

Check out detailed server setup instruction [here](docs/backend/server_config.md).

## How to release fulfill

Execute the following commands:

```
git checkout master
make test
bumpversion patch  # 'patch' can be replaced with 'minor' or 'major'
git push origin master
git push origin master --tags
git checkout qa
git rebase master
git push origin qa
```

## Contributing

Golden Rule:

> Anything in **master** is always **deployable**.

Avoid working on `master` branch, create a new branch with meaningful name, send pull request asap. Be vocal!

Refer to [CONTRIBUTING.md][contributing]

[contributing]: http://github.com/ShubhamBansal1997/fulfill-web/tree/master/CONTRIBUTING.md
