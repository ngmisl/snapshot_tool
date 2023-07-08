# Snapshot Tool

## Introduction
The Snapshot Tool is a quick and efficient tool for getting all NFT holders of a contract via sys.arg. It's designed to provide a snapshot of the current state of a contract, including all current NFT holders.

## Installation
To install the Snapshot Tool, you will need to have Python installed on your machine. You will also need to install the dependencies listed in the `requirements.txt` file. You can do this by running `pip install -r requirements.txt` in your terminal.

## Usage
To use the Snapshot Tool, run the `main.py` file with the contract address as an argument. For example, `python main.py 0xYourContractAddress`.

## Interpreting the Output
The output of the Snapshot Tool is a CSV file that includes a list of all NFT holders for the given contract. Each row in the CSV file represents a single NFT holder.

## Examples
Here's an example of how to use the Snapshot Tool:

```
python main.py 0xYourContractAddress
```

This will generate a CSV file with a list of all NFT holders for the contract at `0xYourContractAddress`.

