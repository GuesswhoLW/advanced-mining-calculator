# Advanced Mining Profitability Calculator

This script calculates the profitability of mining Spectre (SPR) by estimating rewards and electricity costs. Users can input their details manually or use credentials stored in a `.env` file to fetch data from Hive OS.

## Features

- Calculate estimated mining rewards in SPR and USD.
- Calculate electricity costs based on user-defined tariffs.
- Determine profitability based on estimated rewards and electricity costs.
- Option to use Hive OS credentials stored in a `.env` file or input hashrate manually.
- Configurable loading bar duration.

## Requirements

- Python 3.x
- Required Python libraries:
  - requests
  - python-dotenv

## Installation

### On Hive OS or Linux

1. **Clone the repository:**
   ```sh
   git clone https://github.com/GuesswhoLW/advanced-mining-calculator.git
   cd advanced-mining-calculator
