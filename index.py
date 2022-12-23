import Data
import utils
import File




def main():



    # ---------------------------------------------main report---------------------------------------------
    data = Data.build_validator_info()
    columns=["operator_address","moniker","jailed","total_delegated_tokens",
    "outstanding_commission","outstanding_rewards","withdrawn_commission","withdrawn_rewards",
    "total_commission","total_rewards","total_earnings"]
    File._write_to_csv(data,"Validator_Earnings_Report.csv",columns)


if __name__ == '__main__':
    main()