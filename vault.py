import hvac
import os

if not 'VAULT_ADDR' in os.environ or not 'VAULT_ROLE_ID' in os.environ:
    raise Exception('VAULT_ADDR or VAULT_ROLE_ID are missing')

vault = hvac.Client(os.environ['VAULT_ADDR'])
auth = vault.auth_approle(os.environ['VAULT_ROLE_ID'])
if 'auth' in auth and 'client_token' in auth['auth']:
    vault.token = auth['auth']['client_token']
else:
    raise Exception('Authorization to Vault failed!')


def read_data(key):
    resp = vault.read(key)
    if 'data' not in resp:
        raise Exception('Unable to read configuration')
    return resp['data']
