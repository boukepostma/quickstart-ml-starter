from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from kedro.framework.hooks import hook_impl


class AzureSecretsHook:
    @hook_impl
    def after_context_created(self, context) -> None:
        params = context.config_loader["parameters"]

        current_credentials = context.config_loader["credentials"]
        service_principal_creds = current_credentials.get("service_principal")

        if not (service_principal_creds and isinstance(service_principal_creds, dict)):
            return
        if not all(service_principal_creds.values()):
            return

        my_credential = ClientSecretCredential(**service_principal_creds)

        secrets = {}
        for cred_name, secret_configs in params["secret_sources"].items():
            KVUri = f"https://{secret_configs['key_vault_name']}.vault.azure.net"
            client = SecretClient(vault_url=KVUri, credential=my_credential)

            secrets = {
                **secrets,
                cred_name: {
                    "account_name": secret_configs["account_name"],
                    "account_key": client.get_secret(
                        secret_configs["storage_key_id"]
                    ).value,
                },
            }

        context.config_loader["credentials"] = {
            **current_credentials,
            **secrets,
        }
