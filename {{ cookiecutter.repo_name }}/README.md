# {{ cookiecutter.project_name }}

This is your new Kedro project configured according to QuickStart ML principles. Modify this README as you develop your project, for now you will find here some basic info that you need to get started. For more detailed assistance please refer to the [Kedro documentation](https://kedro.readthedocs.io/en/stable/index.html) and [QuickStart ML Blueprints](https://github.com/getindata/quickstart-ml-blueprints).

Additionally to a blank Kedro template it features technological stack used in QuickStart ML approach, such as:
  - [Poetry](https://python-poetry.org/)
  - [pre-commit](https://pre-commit.com/) hooks
  - [Dockerfile](https://docs.docker.com/engine/reference/builder/) setup
  - [VSCode Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) for ease of development
  - [MLFlow integration](https://kedro-mlflow.readthedocs.io/en/stable/)

# Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://kedro.readthedocs.io/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

# Setting up the project

Below there are short instructions on how to get the environment for your new project up and running. Detailed version with some remarks and specific cases described are available in [QuickStart ML Blueprints documentation](https://github.com/getindata/quickstart-ml-blueprints).

## Local Setup using VSCode devcontainers (recommended approach)
This approach facilitates use of [VSCode devcontainers](https://code.visualstudio.com/docs/devcontainers/containers). It is the easiest way to set up the development environment. 

Prerequisites:
* [VSCode](https://code.visualstudio.com/) with [Remote development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) extension
* [Docker](https://www.docker.com/) with `/workspaces` entry in `Docker Desktop > Preferences > Resources > File Sharing`

Setting up:
1. Clone this repository and [open it in a container](https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-open-an-existing-folder-in-a-container).
2. You're good to go!

---

<details>
  <summary>Click here for instructions to install locally (not recommended)</summary>

  ## Local Manual Setup

  The project is using pyenv Python version management. It lets you easily install and switch between multiple versions of Python. To install pyenv, follow [these steps](https://github.com/pyenv/pyenv#installation=) for your operating system.

  To install a specific Python version use this command:
  ```bash
  pyenv install 3.8.16
  pyenv shell 3.8.16
  ```

  ### Virtual environment

  It is recommended to create a virtual environment in your project:
  ```
  python -m venv venv
  source ./venv/bin/activate
  ```

  ### Installing dependencies with Poetry

  To install libraries declared in the pyproject.toml you need to have `Poetry` installed. Install it from [here](https://python-poetry.org/docs/#installing-with-the-official-installer) and then run this command:
  ```bash
  poetry install
  ```

  To add and install dependencies with:
  ```bash
  # dependencies
  poetry add <package_name>

  # dev dependencies
  poetry add -D <package_name>
  ```

  ### Setting up Azure CLI
  Login and configure workspace and follow the instructions to log in to azure through the browser using a device code:
  ```bash
  az login --use-device-code
  az account set --subscription {{ cookiecutter.subscription_id }}
  az configure --defaults workspace= {{ cookiecutter.azure_prefix }}-mlw group={{ cookiecutter.azure_prefix }}-rg location={{ cookiecutter.azure_location }}
  ```
</details>

# How to run Kedro

You can run your Kedro project with:

```bash
kedro run
```

To run a specific pipeline:
```bash
kedro run -p "<PIPELINE_NAME>"
```

# Setting up cloud infrastructure for the first time using Terraform
{% if cookiecutter.subscription_id=="<SUBSCRIPTION_ID>" -%}
0. This project has been initiated without disclosing a subscription_id, so first replace all occurrences of "<SUBSCRIPTION_ID>" with your subscription ID in this repository. {% endif %}
1. Create service principal with contributor role and write down the appid, password and tenant 
```bash
az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/{{ cookiecutter.subscription_id }}"
```
2. Use these values to fill in `terraform/secret.tfvars` and `conf/local/credentials.yml`. Note that `client_id` refers to the `appId` output
3. Set `terraform` as working directory
```bash
cd terraform
```
4. Initialize terraform
```bash
terraform init
```
5. Apply terraform. You may have to wait a minute before the service principal is registered
```bash
terraform apply --var-file secret.tfvars
```

## Setting up remote logging of data and models
By default this project template logs all data and models locally. In order to log remotely after following the infrastructure setup with terraform above, you can toggle configurations in `globals.yml` (under `storage_prefix`) and `mlflow.yml` (under `server`).

Troubleshooting:
* Check whether `service_principal` has been correctly defined in `conf/local/credentials.yml`
* Check whether `server.mlflow_tracking_uri` matches with the result of 
  ```bash
  az ml workspace show --query mlflow_tracking_uri
  ```

# Kedro plugins
### [Kedro-Viz](https://github.com/kedro-org/kedro-viz)
- visualizes Kedro pipelines in an informative way
- to run, `kedro viz --autoreload` inside project's directory
- this will run a server on `http://127.0.0.1:4141`


### [kedro-mlflow](https://github.com/Galileo-Galilei/kedro-mlflow)
- lightweight integration of `MLflow` inside `Kedro` projects
- configuration can be specified inside `conf/<ENV>/mlflow.yml` file
- by default, experiments are saved inside `mlruns` local directory
- to see all the local experiments, run `kedro mlflow ui`
