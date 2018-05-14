# py-ulord-api

[![](https://img.shields.io/badge/py--ulord--api-incomplete-red.svg)](https://shields.io/)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![](https://img.shields.io/badge/cli-completed-green.svg)](https://shields.io/)

Ulord-platform HTTP Client Library

Check out [the client API reference]() for the full command reference.

*Important*: The legacy py-ulord-api package/module will only work for Ulord-platform 0.0.1 and Python 2.7.

*Note*: This library constantly has to change to stay compatible with the Ulord-platform HTTP API. Currently, this library is tested against Ulord-platform v0.0.1. You may experience compatibility issues when attempting to use it with other versions of Ulord-platform.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Documentation](#documentation)
  - [Features from ulord 0.0.1](#important-changes-from-ipfsapi-02x)
- [Featured Projects](#featured-projects)
- [Contribute](#contribute)
  - [IRC](#irc)
  - [Bug reports](#bug-reports)
  - [Pull requests](#pull-requests)
- [License](#license)

## Install
> import: haven't completed!

Install with pip:

```sh
pip install ulordapi
```

Or you can use this repository to set up
```sh
git clone https://github.com/UlordChain/py-ulord-api.git
cd py-ulord-api
python setup.py
```

## Usage
This package has three functions,including cli, py-api and web-API.

### cli
You can use cli to print help and other functions:

```sh
usage: ulordapi [-h] [-v] {daemon,up,udfs,DB,config} ...

ulordapi ---- SDK for the Ulord APIs

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

ulordapi sub-command:
  ulordapi sub-command

  {daemon,up,udfs,DB,config}
                        subcommand help
    daemon              Daemon process,including web server and udfs daemon
    up                  ulord-platform
    udfs                udfs
    DB                  DB
    config              config

Use 'ulordapi <command> --help' to learn more about each command.

EXIT STATUS

The CLI will exit with one of the following values:

0   Successful execution.
1   Failed executions.
```
### py-api:

waiting example...

### web-api:

waiting document...

## Documentation

waiting...

### Features from `ulord 0.0.1`

 waiting...

## Contribute

### Bug reports

You can submit bug reports using the [GitHub issue tracker](https://github.com/UlordChain/py-ulord-api/issues).

### Pull requests

Pull requests are welcome.  Before submitting a new pull request, please waiting...

### Want to read this repository?

Some places to get you started. (WIP)

Senior programmer Main file: [ulordapi/src/user/user1.py](https://github.com/ipfs/go-ipfs/blob/master/cmd/ipfs/main.go) <br>
Junior Programmer Main file: [ulordapi/src/user/user2.py](https://github.com/ipfs/go-ipfs/blob/master/cmd/ipfs/main.go) <br>
CLI Commands: [ulordapi/src/daemon/daemonCLI.py](https://github.com/UlordChain/py-ulord-api/blob/master/ulordapi/src/daemon/daemonCLI.py) <br>

## License

This code is distributed under the terms of the [MIT license](https://opensource.org/licenses/MIT).  Details can be found in the file
[LICENSE](LICENSE) in this repository.