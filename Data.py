import json
import Cmd
from utils import exception_logger
import pandas as pd
import utils


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
    ie. (validator_address, moniker, jailed, tokens)
    """
    validator_dict = convert_validator_data_to_dict()
    validators = validator_dict["validators"]
    validator_info_list = []
    for validator in validators:
        validator_address = validator["operator_address"]
        moniker = validator["description"]["moniker"]
        jailed = validator["jailed"]
        tokens = utils.convert_to_human_readable(float(validator["tokens"]))
        val = (validator_address, moniker, jailed, tokens)
        validator_info_list.append(val)
    return validator_info_list


def get_validator_address(validator_address:str)->str:
  """
  {
  "acc_address": "fx1qcpxytptp0rfawxhgtm8z69y65g3g7d2a0swsv",
  "base64_address": "BgJiLCsLxp6410L2cWik1REUeao=",
  "hex_address": "0602622c2b0bc69eb8d742f67168a4d5111479aa",
  "val_address": "fxvaloper1qcpxytptp0rfawxhgtm8z69y65g3g7d247d3wv"
  }

  returns the acc_address
  """

  cmd = Cmd.get_validator_address_cmd(validator_address)
  data = Cmd.run(cmd)
  return data["acc_address"]


def get_val_outstanding_comms(validator_address:str)->float:
  """
  returns a validator's outstanding commission
  """

  cmd=Cmd.get_val_outstanding_comms_cmd(validator_address)
  commission_data = Cmd.run(cmd)
  if len(commission_data["commission"])>0:
        commission=float(commission_data["commission"][0]["amount"])/10**18
  else:
      commission=0
  return commission

def get_val_outstanding_delegated_rewards(validator_address:str)->float:
  """
  returns a validator's self-delegated rewards (not just to his validator)
  """
  
  validator_wallet_address = get_validator_address(validator_address)
  cmd = Cmd.get_val_outstanding_delegated_rewards_cmd(validator_wallet_address)
  rewards_data = Cmd.run(cmd)
  if len(rewards_data["rewards"])>0:
    if len(rewards_data["total"])>0:
      rewards=float(rewards_data["total"][0]["amount"])/10**18
    else:
      rewards = 0
  else:
    rewards=0
  return rewards


def get_all_withdrawals(validator_address:str)->dict:
  """
  get the raw validator withdrawals info
  """

  cmd = Cmd.get_all_withdrawals_cmd(validator_address)
  data = Cmd.run(cmd)
  return data



def filter_val_withdrawals(validator_address:str)->list:
  """
  filters out all validator withdrawals "withdraw_rewards" & "withdraw_commission" and returns it in a dictionary with the following format:
  [{'height': 3159408, 'withdrawn_rewards': '11553708047937658746100FX', 'withdrawn_commission': '23239037402816277824585FX'}, {'height': 5552017, 'withdraw_rewards': '9639369075157032800FX', 'withdraw_commission': '31625759293826379901863FX'}]
  """
  withdraw_events = get_all_withdrawals(validator_address)
  withdrawal_list = []
  if len(withdraw_events['txs']) > 0:
    for tx in withdraw_events["txs"]:
      withdrawals={}
      withdrawals["height"]=tx["height"]
      for log in tx["logs"]:
        for event in log["events"]:
          if event["type"]=="withdraw_commission":
            if event["attributes"][0].get("value") == None:
              withdrawals["withdrawn_commission"] = 0
            else:
              withdrawals["withdrawn_commission"]=utils.convert_to_human_readable(float(event["attributes"][0]["value"][0:-2]))
          if event["type"]=="withdraw_rewards":
            if event["attributes"][0].get("value") == None:
              withdrawals["withdrawn_commission"] = 0
            else:
              withdrawals["withdrawn_rewards"]=utils.convert_to_human_readable(float(event["attributes"][0]["value"][0:-2]))
          else:
              pass
      withdrawal_list.append(withdrawals)
  else:
    withdrawal_list = [{'height': 0, 'withdrawn_rewards': 0, 'withdrawn_commission': 0}]
  return withdrawal_list


def convert_rewards_and_commission_to_dataframe(filtered_data:list)->pd.DataFrame:
  """
        height  withdrawn_rewards  withdrawn_commission
  0  3159408      11553.708048         23239.037403
  1  5552017          9.639369         31625.759294
  
  this is for easier tracking of info for each validator when required
  """
  
  df = pd.DataFrame.from_dict(filtered_data)
  return df

def sum_rewards_and_commission(df:pd.DataFrame)->tuple:
  """
  sum and return the commission and rewards
  """

  withdrawn_commission = df['withdrawn_commission'].sum()
  withdrawn_rewards = df['withdrawn_rewards'].sum()
  return withdrawn_commission, withdrawn_rewards
    

def get_validator_total_withdrawn_rewards_and_commission(validator_address:str)->tuple:
  """
  input validator address and returns a df of all withdrawals then sums the total withdrawn commission and rewards
  """
  data = filter_val_withdrawals(validator_address)
  df = convert_rewards_and_commission_to_dataframe(data)
  return sum_rewards_and_commission(df)


def build_validator_info():
  """
  [('fxvaloper1c0gnd02hwatfukgcux5f3hvhutcfj9kdvqrmuj', 'Cogni🧠', False, 4915426.917313896, 591.8402775296655, 4.2337591781656325, 4665.656907786245, 34.94493206874103)]

  returns a list of validator info
  """
  data = extract_validator_info()
  validator_info = []
  for d in data:
    validator_address, moniker, jailed, tokens = d[0], d[1], d[2], d[3]
    # print(validator_address,moniker)
    outstanding_comms = get_val_outstanding_comms(validator_address)
    outstanding_rewards = get_val_outstanding_delegated_rewards(validator_address)
    withdrawn_commission, withdrawn_rewards = get_validator_total_withdrawn_rewards_and_commission(validator_address)
    total_commission = outstanding_comms + withdrawn_commission
    total_rewards = outstanding_rewards + withdrawn_rewards
    total_earnings = total_commission + total_rewards
    val = (validator_address, moniker, jailed, tokens, outstanding_comms, outstanding_rewards, withdrawn_commission, withdrawn_rewards, total_commission, total_rewards, total_earnings)
    validator_info.append(val)
  return validator_info