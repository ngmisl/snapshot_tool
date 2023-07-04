import sys
import csv
import os
from web3 import Web3
from standardabi import erc721_abi

erc721_abi = erc721_abi

# Make sure to add the correct RPC provider
w3 = Web3(
    Web3.HTTPProvider(
        ""
    )
)


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

    token_owners = []
    for i in range(1, total_supply + 1):
        try:
            owner = erc721_contract.functions.ownerOf(i).call()
            if owner not in token_owners:
                token_owners.append(owner)
        except Exception as e:
            print(f"Error at token ID {i}: {str(e)}")

    return token_owners


def write_to_csv(token_owners, file_name):
    with open(file_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for wallet in token_owners:
            writer.writerow([wallet])


def create_clean_snapshot(input_file, output_file):
    # No need for cleaning since we're only outputting unique wallet addresses
    pass


if __name__ == "__main__":
    main()
