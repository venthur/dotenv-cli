# dotenv CLI

Dotenv-CLI is a simple Package that provides the `dotenv` command. It
reads the `.env` file from the current directory puts the contents in
the environment and executes the given command.

`dotenv` supports alternative `.env` files like `.env.development` via
the `-e` or `--dotenv` parametes.

## Usage

Just prepend the command you want to run with the extra environment
variables from the `.env` file with `dotenv`:

```bash
$ dotenv some-command
```

## Install

```bash
$ pip install dotenv-cli
```
