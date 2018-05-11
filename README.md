# idex-downloader

## Overview

This program downloads idex.market trade history via their API and outputs the data in CoinTracking.info CSV format.  I have no association with IDEX.

## Instructions

### Python Setup

This program requires Python 3 and has some dependencies.  If you are running Ubuntu, the following commands can be used to install the dependencies.  If you are running Windows 10, you can install Ubuntu here: https://www.microsoft.com/en-us/store/p/ubuntu/9nblggh4msv6.
```
sudo apt-get update
sudo apt-get install python3-pip
python3 -m pip install pandas --user
```

Run the following command:
```
python3 idex_downloader.py
```

Input the Ethereum addresses that you use for IDEX as prompted, using commas to separate multiple addresses.  An example address looks like this: 0xcc13fc627effd6e35d2d2706ea3c4d7396c610ea.  When entering multiple addresses, the addresses must have never traded with each other on IDEX.  Otherwise, unexpected behavior will occur when generating the output.

The program will output a CSV file in CoinTracking.info format in the same directory as the Python program file.

## Known Issues

- Up to 10,000 trades per Ethereum address entered are supported.  If an Ethereum address has more trades associated with it that exceed this limit, only the first 10,000 trades returned by the IDEX API will be in the output.
