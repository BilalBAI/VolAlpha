# VolAlpha

## VolAlpha
An illustrative volatility strategy based on a combination of spot and option positions, leveraging SABR model calibration of volatility smiles. The focus is on applying a stress-testing framework to an option+spot portfolio instead of a fully functioning trading strategy.

Read `VolAlpha.ipynb` for more information.

## portfolio-stress-test
[PortRisk](https://github.com/BilalBAI/portfolio-stress-test) is a production-ready Python-based stress testing tool, designed to evaluate portfolio risk under various stress scenarios. It leverages the Bloomberg API for data retrieval and offers a modular structure for customizable and flexible usage.

Read `PortfolioStressTest.pdf` for more information.

## Risk-Reporting
An illustrative dash app frontend for the stress testing system. 
The stress testing results will be pushed into a database and this frontend can read the database, trigger new stress testing, and send out email snapshots.