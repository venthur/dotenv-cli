# dotenv CLI

Dotenv-CLI is a simple package that provides the `dotenv` command. It reads the
`.env` file from the current directory puts the contents in the environment and
executes the given command.

`dotenv` supports alternative `.env` files like `.env.development` via the `-e`
or `--dotenv` parametes.

`dotenv` provides bash completion, so you can use `dotenv` like this:

```bash
$ dotenv make <TAB>
all      clean    docs     lint     release  test
```

## Usage

Just prepend the command you want to run with the extra environment variables
from the `.env` file with `dotenv`:

```bash
$ dotenv some-command
```

## Install

### Using PyPi

```bash
$ pip install dotenv-cli
```

### On Debian and Ubuntu

```bash
# apt-get install python3-dotenv-cli
```
