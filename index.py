import Cmd
import Data



staking_validators = Cmd.get_staking_validators()

data = Data.extract_validator_data(staking_validators)

print(data)