# QuickStart ML Kedro starter

## Usage for local & azure environment 
Execute the following inside Linux (or WSL2) with your current working directory where you'd like to store this project.
```bash
# For HTTPS cloning:
kedro new --starter=https://github.com/boukepostma/quickstart-ml-starter.git --checkout=local-azure

# For SSH cloning:
kedro new --starter=git@github.com:boukepostma/quickstart-ml-starter.git  --checkout=local-azure

# Follow the prompts to name your project and (optionally) set cloud project details.

# Then open the newly created project directory in vscode:
code <my-project-name>

# Now follow the setup instructions in the new project's README.md
```

## Prerequisites
* Linux / WSL2 environment with
    * kedro installed
    * git installed and configured
        ```bash
        git config --global user.name "John Doe"
        git config --global user.email johndoe@example.com
        ```
    * Azure CLI installed and set up to connect with your azure account(s) (through `az login`)
* Docker
