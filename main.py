import sys
import csv
import os
from web3 import Web3
from standardabi import erc721_abi
import polars as pl

erc721_abi = erc721_abi

# Make sure to add the correct RPC provider
w3 = Web3(Web3.HTTPProvider("https://polygon-mainnet.g.alchemy.com/v2/GVWi59Zd_weqiDY_nVNGoE6lU6ZKjvi-"))

# The main function is the entry point of the program. It checks the command line arguments, 
# calls the total_supply function to get the token owners, writes the token owners to a CSV file, 
# and creates a clean snapshot.
def main():
    if len(sys.argv) != 2:
        print("Error: You can only enter the Contract Address")
    else:
        for arg in sys.argv[1:]:
            token_owners = total_supply(arg)
            snapshot_file = "snapshot.csv"
            if not os.path.exists(snapshot_file):
                write_to_csv(token_owners, snapshot_file)
            create_clean_snapshot(snapshot_file, "snapshot_clean.csv")

# The total_supply function creates a contract instance using the provided contract address, 
# calls the totalSupply function of the contract to get the total supply of tokens, 
# and then iterates over each token to get its owner.
def total_supply(contract):
    erc721_contract = w3.eth.contract(
        address=w3.toChecksumAddress(contract), abi=erc721_abi
    )
    total_supply = erc721_contract.functions.totalSupply().call()

    token_owners = {}
    for i in range(1, total_supply + 1):
        owner = erc721_contract.functions.ownerOf(i).call()
        token_owners[i] = owner

    return token_owners

# The write_to_csv function writes the token owners to a CSV file. It creates a CSV writer with 
# the fieldnames "id" and "wallet", writes the header, and then writes each token owner to the file.
def write_to_csv(token_owners, file_name):
    with open(file_name, "w", newline="") as csvfile:
        fieldnames = ["id", "wallet"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for token_id, wallet in token_owners.items():
            writer.writerow({"id": token_id, "wallet": wallet})

# The create_clean_snapshot function reads the CSV file of token owners, groups the data by wallet, 
# counts the number of tokens each wallet holds, and writes the clean snapshot to a new CSV file.
def create_clean_snapshot(input_file, output_file):
    if not os.path.exists(output_file):
        df = pl.read_csv(input_file)
        df_clean = df.groupby("wallet").agg(pl.col("id").alias("holdings").count())
        df_clean.write_csv(output_file)

if __name__ == "__main__":
    main()
