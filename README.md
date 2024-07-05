# Advanced Mining Profitability Calculator

This script calculates the profitability of mining [Spectre (SPR)](https://spectre-network.org) by estimating rewards and electricity costs. Users can input their details manually or use credentials stored in a `.env` file to fetch data from Hive OS.

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

1. *Clone the repository:*
   ```sh
   git clone https://github.com/GuesswhoLW/advanced-mining-calculator.git
   cd advanced-mining-calculator
   
2. Install required libraries:
   ```sh
   pip install -r requirements.txt

3. Create a .env file (optional if using Hive OS credentials):
   ```sh
   touch .env
  
4. Add the following lines to the .env file:
    ```sh
    HIVE_OS_API_KEY=your_hive_os_api_key
    HIVE_OS_FARM_ID=your_hive_os_farm_id    

5. Create a .gitignore file to ensure the .env file is not uploaded to GitHub:
   ```sh
   touch .gitignore

6. Add the following line to the .gitignore file:
    ```sh
    .env
    
7. Run the script:
   ```sh
   python advanced_calculator.py

### On Windows WSL

1. Install Python and pip:
   ```sh
   sudo apt update
   sudo apt install python3 python3-pip
   
2. Clone the repository:
   ```sh
   git clone https://github.com/GuesswhoLW/advanced-mining-calculator.git
   cd advanced-mining-calculator

3. Install required libraries:
   ```sh
   pip3 install -r requirements.txt
  
4. Create a .env file (optional if using Hive OS credentials):
    ```sh
    touch .env  

5. Add the following lines to the .env file:
   ```sh
   HIVE_OS_API_KEY=your_hive_os_api_key
   HIVE_OS_FARM_ID=your_hive_os_farm_id

6. Create a .gitignore file to ensure the .env file is not uploaded to GitHub:
   ```sh
   touch .gitignore

7. Add the following line to the .gitignore file:
    ```sh
    .env
    
8. Run the script:
   ```sh
   python3 advanced_calculator.py

## Usage

1. Select Tariff Type:

    - The script will prompt you to enter the tariff type (dual/single).
      
2. Enter Tariff Details:

    - Depending on the tariff type, enter the required details (day tariff, night tariff, single tariff, high tariffs if applicable).
      
3. Enter Power Consumption:

    - Enter the total power consumption in watts.
      
4. Enter Yearly Limit:
    - Enter the yearly limit in kWh (if any, else enter N/A).
      
5. Loading Bar Duration:

    - Enter the duration for the loading bar in minutes.
      
6. Select Hashrate Source:

    - Choose whether to use credentials from the .env file or enter your hashrate manually.
      
7. Script Execution:

    - The script will calculate and print estimated mining rewards, electricity costs, and determine profitability.

## Example

  Here's a sample interaction with the script:

  ![image](https://github.com/GuesswhoLW/advanced-mining-calculator/assets/174736759/8a385907-b75d-4bd8-9996-2a66b8523d4d)


## Notes

  - Ensure that the required Python libraries are installed using the requirements.txt file.
  - If using Hive OS credentials, create a .env file with your Hive OS API key and farm ID.
  - The script handles both online and offline modes for fetching hashrate.

## License

  This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support
  If you find this small project helpful and would like to support my work and future projects, feel free to donate a cup of coffee to my Spectre wallet:
  ```sh
    spectre:qr7nl6z8nc8gmagarmzrnaw90xu2xxzzn8qtg2wql967njendf5eqeqdnmhuc
