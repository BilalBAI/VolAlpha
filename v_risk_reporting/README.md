# Risk-Reporting
An illustrative dash app frontend for the stress testing system. 
The stress testing results will be pushed into a database and this frontend can read the database, trigger new stress testing, and send out email snapshots.

## `.env`
In the `.env` you need the following keys:
```ini
USERNAME=<USERNAME>
PASSWORD=<PASSWORD>
DB_CON_STR=<str>
ENVIRONMENT=<develop/production>
```

## Installation

Clone down the reop; make the `.env`; create the env and activate;

### Steps

``` bash
conda create --name dapp -y python=3.7 pip=20.1.1
conda activate dapp
pip install -r requirements.txt
```
