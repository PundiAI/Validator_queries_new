import requests

# validator_info = ["fxcored","q","staking","validators","--node=https://fx-json.functionx.io:26657"],
# "create_val":["fxcored","q","txs","--events","message.action=create_validator","--node=https://fx-json.functionx.io:26657","--limit=100"],
# "val_withdrawals":["fxcored","q","txs","--events","msg","--node=https://fx-json.functionx.io:26657"],
# "val_outstanding_comms":["fxcored","q","distribution","commission","val","--node=https://fx-json.functionx.io:26657"],
# "delegator_rewards":["fxcored","q","distribution","rewards","wallet","--node=https://fx-json.functionx.io:26657"]


def get_val_outstanding_rewards(validator_address):
    r = requests.get(f'https://fx-rest.functionx.io/cosmos/distribution/v1beta1/validators/{validator_address}/outstanding_rewards')
    print(r.text)

def get_val_commission(validator_address):
    r = requests.get(f'https://fx-rest.functionx.io/cosmos/distribution/v1beta1/validators/{validator_address}/commission')
    print(r.text)

def get_staking_validators():
    r = requests.get('https://fx-rest.functionx.io/cosmos/staking/v1beta1/validators')
    return r.text


# fxcored query distribution rewards fx1a73plz6w7fc8ydlwxddanc7a239kk45jmwcesj
# fxcored query distribution commission fxvaloper1a73plz6w7fc8ydlwxddanc7a239kk45jnl9xwj
# fxcored query txs --events 'message.sender=fxvaloper19psvqem8jafc5ydg4cnh0t2m04ngw9gfqkeceu&message.module=distribution'

