import Data
import utils
import File
from Report import Report



def main():


    
    # ---------------toggle the below once csv files have been generated------------
    data = Data.build_validator_info()
    columns=["operator_address","moniker","jailed","total_delegated_tokens",
    "outstanding_commission","outstanding_rewards","withdrawn_commission","withdrawn_rewards",
    "total_commission","total_rewards","total_earnings"]
    File._write_to_csv(data,"Validator_Earnings_Report.csv",columns)
    # val_status_master_report=Report("Val_status_master",val_status,"csv",comms_columns)
    # val_status_master_report.write_to_file()
    # Validator_Earnings_Report = Report("Validator_Earnings_Report",data,"csv",columns)
    # Validator_Earnings_Report.write_to_file()


if __name__ == '__main__':
    main()