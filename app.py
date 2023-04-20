import base64
import pandas as pd
import streamlit as st
from retry import retry
from web3 import Web3

from standardabi import erc721_abi

erc721_abi = erc721_abi

# Make sure to add the correct RPC provider
w3 = Web3(Web3.HTTPProvider("http://34.162.187.208:8545"))


@retry(tries=5, delay=5)
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


def create_clean_snapshot(token_owners):
    df = pd.DataFrame(token_owners.items(), columns=["id", "wallet"])
    df_clean = df.groupby("wallet")["id"].count().reset_index(name="holdings")
    df_clean_sorted = df_clean.sort_values(by="holdings", ascending=False)
    return df_clean_sorted


def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV file</a>'  # noqa: E501


st.title("ERC721 Token Holders Snapshot")
st.markdown("Follow Us: [Click Here](https://linktr.ee/cantoverse)")

contract_input = st.text_input("Enter the contract address:")

if contract_input:
    try:
        token_owners = total_supply(contract_input)
        snapshot_df = create_clean_snapshot(token_owners)
        st.write(snapshot_df)

        # Add the option to download as CSV
        download_link = get_csv_download_link(snapshot_df, "erc721_snapshot.csv")
        st.markdown(download_link, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {e}")
