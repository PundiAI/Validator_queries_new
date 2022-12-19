import json
import Cmd

def convert_validator_data_to_dict()->dict:
    """
    convert validator string output from rpc query to dictionary

       {
      "operator_address": "fxvaloper1qcpxytptp0rfawxhgtm8z69y65g3g7d247d3wv",
      "consensus_pubkey": {
        "@type": "/cosmos.crypto.ed25519.PubKey",
        "key": "T3bm1LbS2zAgv5D7PQVxKyOA9GKu0AzRYLcWewpX4TY="
      },
      "jailed": false,
      "status": "BOND_STATUS_BONDED",
      "tokens": "5539423928702974185741506",
      "delegator_shares": "5539423928702974185741506.000000000000000000",
      "description": {
        "moniker": "ChiangMai",
        "identity": "",
        "website": "functionx.io",
        "security_contact": "contact@functionx.io",
        "details": "Details A Function X foundation self-hosted validator."
      },
      "unbonding_height": "0",
      "unbonding_time": "1970-01-01T00:00:00Z",
      "commission": {
        "commission_rates": {
          "rate": "0.050000000000000000",
          "max_rate": "0.200000000000000000",
          "max_change_rate": "0.010000000000000000"
        },
        "update_time": "2022-01-10T03:18:54.319159936Z"
      },
      "min_self_delegation": "10000000000000000"
    },

    """
    staking_validators = Cmd.get_staking_validators()
    data = json.loads(staking_validators)
    return data

def extract_validator_info()->list:
    """
    extract and return important validator info into a list
    """
    validator_dict = convert_validator_data_to_dict()
    validators = validator_dict["validators"]
    validator_info_list = []
    for validator in validators:
        validator_address = validator["operator_address"]
        moniker = validator["description"]["moniker"]
        jailed = validator["jailed"]
        tokens = validator["tokens"]
        val = (validator_address, moniker, jailed, tokens)
        validator_info_list.append(val)
    return validator_info_list