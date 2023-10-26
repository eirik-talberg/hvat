# HVAT (HashiCorp Vault Automation Toolkit)
This is a small CLI tool indented to help automate setting up [HashiCorp Vault](https://www.vaultproject.io/). It leverages the built-in HTTP API in Vault to perform tasks with a provided configuration.

## Features
* Initialization (`vault operator init`)
    * Automatic set-up and export of keys and tokens created when Vault is initialized
    * Display or distribute initialization output:
        * Standard out
        * HCP Vault Secrets
        * Vault Transit Engine (Auto Unseal)
        * AWS KMS (Auto Unseal)(Planned)
        * Azure KeyVault (Auto Unseal)(Planned)



## Running the image

HVAT is a CLI application intended to run containerized (i.e. Docker, podman or Kubernetes). The config file location can be supplied through an argument or, preferably, mounted in the image to `/etc/hvat/config.yaml`.

```
Usage: python -m hvat.main [OPTIONS] COMMAND [ARGS]...

Options:
  --config TEXT  Location of config file to use
  --help         Show this message and exit.

Commands:
  init
```



## Configuration options
|key|description|required|default|
|---|---|---|---|
| `vault_url` |URL to the Vault instance you want to configure | Yes | |
| `init.auto_unseal` | Flag to enable/disable the auto unseal capabilities in Vault. If `true`, a provider configuration is required. | Yes | `false` |
| `init.destination.type` | Where to publish/export the results of the initialization. `stdout` is currently supported.| Yes | |


### Minimal configuration - STDOUT

**WARNING**: This method prints the unseal keys and the root token to the terminal. Use only for development and local testing. 

```yaml
vault_url: "http://localhost:8200"
init:  
  auto_unseal: false
  destination:
    type: stdout
```

### Configuration example - HCP Vault Secrets


## Development
This application is written in Python 3.11 with [Poetry](https://python-poetry.org/) as its package manager.

### Requirements
* Python 3.11
* Poetry 1.6.x

### Setup
With an up-to-date Python installation and `poetry` in your `$PATH`, just run `poetry install` to set up a virtual environment with dependencies installed for development.

## Releases
This project uses `semantic-release` to automatically release a new version whenever a feature, bugfix or breaking change has been merged, tested and verified.

## Resources and references
* https://www.hashicorp.com/
* https://www.vaultproject.io/
* https://python-poetry.org/
* https://semantic-release.gitbook.io/semantic-release/
* https://github.com/angular/angular/blob/main/CONTRIBUTING.md
