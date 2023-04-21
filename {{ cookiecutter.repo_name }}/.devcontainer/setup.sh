git init
pre-commit install

az account set --subscription="{{ cookiecutter.subscription_id }}"
az configure --defaults workspace="{{ cookiecutter.azure_prefix }}-dev-mlw" group="{{ cookiecutter.azure_prefix }}-dev-rg" location="{{ cookiecutter.azure_location }}" --scope local

# Initialize pyenv
echo 'eval "$(pyenv init -)"' >> ~/.zshrc