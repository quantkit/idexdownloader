# idex-downloader

## Overview

This program downloads IDEX trade history via API and outputs the data in CoinTracking.info CSV format.

## Instructions

### Python Setup

This program requires Python 3 and has some dependencies.  If you are running Ubuntu, the following commands can be used to install the dependencies.  If you are running Windows 10, you can install Ubuntu here: https://www.microsoft.com/en-us/store/p/ubuntu/9nblggh4msv6.
```
sudo apt-get update
sudo apt-get install python3-pip
python3 -m pip install pandas --user
```

Download the idex_downloader.py file from this repository.  Navigate to the directory that contains the file and run the following command:
```
python3 idex_downloader.py
```

When prompted, input the Ethereum address(es) that you use for IDEX, using commas to separate multiple addresses.  An example address looks like this: 0xcc13fc627effd6e35d2d2706ea3c4d7396c610ea.  When entering multiple addresses, the addresses must have never traded with each other on IDEX.  Otherwise, unexpected behavior will occur when generating the output.

The program will output a CSV file in CoinTracking.info format in the same directory as the Python program file.

## Known Issues

- Up to 10,000 trades per Ethereum address entered are supported.  If the trades for an Ethereum address exceed this limit, only the first 10,000 trades returned by the IDEX API for that address will appear in the output.
