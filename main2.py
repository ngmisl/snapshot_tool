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
# and then iterates over each token to get its owner. If the owner is not already in the list 
# of token owners, it is added.
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

# The write_to_csv function writes the token owners to a CSV file. It creates a CSV writer and 
# then writes each token owner to the file.
def write_to_csv(token_owners, file_name):
    with open(file_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for wallet in token_owners:
            writer.writerow([wallet])

# The create_clean_snapshot function does not need to do anything since we're only outputting 
# unique wallet addresses.
def create_clean_snapshot(input_file, output_file):
    pass

if __name__ == "__main__":
    main()
