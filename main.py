import sys
import csv
import os
from web3 import Web3
from standardabi import erc721_abi
import polars as pl

erc721_abi = erc721_abi

# Make sure to add the correct RPC provider
w3 = Web3(Web3.HTTPProvider("https://canto.slingshot.finance/"))


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


def write_to_csv(token_owners, file_name):
    with open(file_name, "w", newline="") as csvfile:
        fieldnames = ["id", "wallet"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for token_id, wallet in token_owners.items():
            writer.writerow({"id": token_id, "wallet": wallet})


def create_clean_snapshot(input_file, output_file):
    if not os.path.exists(output_file):
        df = pl.read_csv(input_file)
        df_clean = df.groupby("wallet").agg(pl.col("id").alias("holdings").count())
        df_clean.write_csv(output_file)


if __name__ == "__main__":
    main()
