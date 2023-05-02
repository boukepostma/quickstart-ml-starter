import logging

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from kedro.framework.hooks import hook_impl

logger = logging.getLogger(__name__)


class AzureSecretsHook:
    @hook_impl
    def after_context_created(self, context) -> None:
        params = context.config_loader["parameters"]

        current_credentials = context.config_loader["credentials"]
        service_principal_creds = current_credentials.get("service_principal")

        # If no service principal creds, don't access key vault
        if not (service_principal_creds and isinstance(service_principal_creds, dict)):
            logger.warning(
                "Service principal credentials are incomplete. "
                "Key vault will not be queried"
            )
            secrets = {cred: None for cred in params["key_vault_queries"]}

        # If missing value for service principal creds, don't access key vault
        elif not all(service_principal_creds.values()):
            logger.warning(
                "Service principal credentials are incomplete. "
                "Key vault will not be queried"
            )
            secrets = {cred: None for cred in params["key_vault_queries"]}

        # If possible, access key vault as service principal to access keys
        else:
            my_credential = ClientSecretCredential(**service_principal_creds)

            secrets = {}
            for query_name, secret_configs in params["key_vault_queries"].items():
                # Try query, send warning if not succesful
                try:
                    KVUri = (
                        f"https://{secret_configs['key_vault_name']}.vault.azure.net"
                    )
                    client = SecretClient(vault_url=KVUri, credential=my_credential)

                    storage_key_id = secret_configs["storage_key_id"]
                    account_key = client.get_secret(storage_key_id).value
                except:
                    logger.warning(
                        f"Query {query_name}: {secret_configs} failed and is skipped"
                    )
                    account_key = None
                secrets = {
                    **secrets,
                    query_name: {
                        "account_name": secret_configs["account_name"],
                        "account_key": account_key,
                    },
                }

        context.config_loader["credentials"] = {
            **current_credentials,
            **secrets,
        }
