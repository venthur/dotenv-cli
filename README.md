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

## Install

### Using PyPi

dotenv-cli is [available on PyPi][pypi], you can install it via:

[pypi]: https://pypi.org/project/dotenv-cli/

```bash
$ pip install dotenv-cli
```

### On Debian and Ubuntu

Alternatively, you can install dotenv-cli on Debian based distributions via:

```bash
# apt-get install python3-dotenv-cli
```


## Usage

Create an `.env` file in the root of your project and populate it with some
values like so:

```sh
SOME_SECRET=donttrythisathome
SOME_CONFIG=foo
```

Just prepend the command you want to run with the extra environment variables
from the `.env` file with `dotenv`:

```bash
$ dotenv some-command
```

and those variables will be available in your environment variables.


### Multi-Line Value

For multi-line values, you can use quotes and the `\n` character:

```sh
SSH_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
```

### Comments

`dotenv` ignores lines starting with `#`:

```sh
# this is a comment
FOO=bar"
```
