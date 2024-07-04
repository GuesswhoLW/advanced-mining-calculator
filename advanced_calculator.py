import requests
import json
import os
import time
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
spectre_api_url = "https://api.spectre-network.org/info/hashrate"
spr_price_api_url = "https://api.spectre-network.org/info/price"
block_reward_api_url = "https://api.spectre-network.org/info/blockreward"
hive_os_api_url = "https://api2.hiveos.farm/api/v2"
hive_os_api_key = os.getenv("HIVE_OS_API_KEY")
farm_id = os.getenv("HIVE_OS_FARM_ID")

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_str_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please enter one of the following: {', '.join(valid_options)}")

def get_network_hashrate():
    response = requests.get(spectre_api_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("hashrate", 0) * 1e6  # Convert to MH/s
    else:
        print("Failed to fetch hashrate data:", response.status_code, response.text)
        return 0

def get_current_spr_price():
    response = requests.get(spr_price_api_url)
    if response.status_code == 200:
        data = response.json()
        current_price = data.get("price", 0)
        return current_price
    else:
        print("Failed to fetch SPR price data:", response.status_code, response.text)
        return 0

def get_block_reward():
    response = requests.get(block_reward_api_url)
    if response.status_code == 200:
        data = response.json()
        return data.get("blockreward", 0)
    else:
        print("Failed to fetch block reward data:", response.status_code, response.text)
        return 0

def get_worker_hashrates():
    headers = {
        "Authorization": f"Bearer {hive_os_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{hive_os_api_url}/farms/{farm_id}/workers", headers=headers)
    if response.status_code == 200:
        data = response.json()
        total_hashrate = 0
        for worker in data.get('data', []):
            miners_summary = worker.get("miners_summary", {})
            for hashrate_info in miners_summary.get("hashrates", []):
                if hashrate_info.get("coin") == "SPR":
                    total_hashrate += hashrate_info.get("hash", 0)
        return total_hashrate  # Since we have KH/s, no conversion needed
    else:
        print("Failed to fetch workers data:", response.status_code, response.text)
        return 0

def calculate_estimated_rewards(network_hashrate, my_hashrate, block_reward, spr_price):
    if network_hashrate == 0:
        my_portion = 0
    else:
        my_portion = (my_hashrate * 1e-3) / network_hashrate  # Convert my_hashrate from KH/s to MH/s for comparison

    daily_network_reward = 1015200  # Correct total SPR mined per day
    daily_my_reward = daily_network_reward * my_portion
    
    estimated_hourly_spr = daily_my_reward / 24
    estimated_daily_spr = daily_my_reward
    estimated_weekly_spr = estimated_daily_spr * 7
    estimated_monthly_spr = estimated_daily_spr * 30
    estimated_yearly_spr = estimated_daily_spr * 365

    estimated_hourly_usd = estimated_hourly_spr * spr_price
    estimated_daily_usd = estimated_daily_spr * spr_price
    estimated_weekly_usd = estimated_weekly_spr * spr_price
    estimated_monthly_usd = estimated_monthly_spr * spr_price
    estimated_yearly_usd = estimated_yearly_spr * spr_price

    return {
        "hourly": (estimated_hourly_spr, estimated_hourly_usd),
        "daily": (estimated_daily_spr, estimated_daily_usd),
        "weekly": (estimated_weekly_spr, estimated_weekly_usd),
        "monthly": (estimated_monthly_spr, estimated_monthly_usd),
        "yearly": (estimated_yearly_spr, estimated_yearly_usd)
    }

def calculate_electricity_cost(total_watts, above_limit=False):
    power_usage_kw = total_watts / 1000  # Convert W to kW
    
    if tariff_type == "dual":
        day_energy_consumption_kwh = power_usage_kw * day_hours
        night_energy_consumption_kwh = power_usage_kw * night_hours

        if above_limit:
            day_cost_usd = day_energy_consumption_kwh * high_day_tariff_usd_per_kwh
            night_cost_usd = night_energy_consumption_kwh * high_night_tariff_usd_per_kwh
        else:
            day_cost_usd = day_energy_consumption_kwh * day_tariff_usd_per_kwh
            night_cost_usd = night_energy_consumption_kwh * night_tariff_usd_per_kwh

        total_cost_usd = day_cost_usd + night_cost_usd
        return total_cost_usd, day_cost_usd / day_energy_consumption_kwh, night_cost_usd / night_energy_consumption_kwh
    elif tariff_type == "single":
        total_energy_consumption_kwh = power_usage_kw * 24
        if above_limit and high_single_tariff_usd_per_kwh > 0:
            combined_cost_usd = total_energy_consumption_kwh * high_single_tariff_usd_per_kwh
        else:
            combined_cost_usd = total_energy_consumption_kwh * single_tariff_usd_per_kwh
        return combined_cost_usd, combined_cost_usd / total_energy_consumption_kwh, combined_cost_usd / total_energy_consumption_kwh

def print_estimated_rewards(rewards):
    print(f"\nEstimated Mining Rewards:")
    print(f"Hour: {rewards['hourly'][0]:.2f} SPR (${rewards['hourly'][1]:.2f})")
    print(f"Day: {rewards['daily'][0]:.2f} SPR (${rewards['daily'][1]:.2f})")
    print(f"Week: {rewards['weekly'][0]:.2f} SPR (${rewards['weekly'][1]:.2f})")
    print(f"Month: {rewards['monthly'][0]:.2f} SPR (${rewards['monthly'][1]:.2f})")
    print(f"Year: {rewards['yearly'][0]:.2f} SPR (${rewards['yearly'][1]:.2f})")

def print_loading_bar(duration):
    start_time = time.time()
    while time.time() - start_time <= duration:
        elapsed_time = time.time() - start_time
        percentage = (elapsed_time / duration) * 100
        bar_length = int((elapsed_time / duration) * 50)
        bar = '=' * bar_length + ' ' * (50 - bar_length)
        eta = max(0, duration - int(elapsed_time))
        sys.stdout.write(f'\rNext check in: [{bar}] {percentage:.0f}% eta {eta}s')
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\rNext check in: [==================================================] 100% eta 0s\n')

def main():
    try:
        use_env_credentials = get_str_input("Do you want to use credentials from the .env file? (yes/no): ", ["yes", "no"])

        if use_env_credentials == "yes":
            my_hashrate = get_worker_hashrates()
        else:
            my_hashrate = get_float_input("Enter your hashrate in KH/s: ")

        while True:
            network_hashrate = get_network_hashrate()
            block_reward = get_block_reward()
            spr_price = get_current_spr_price()

            print(f"\nCurrent Network Hashrate: {network_hashrate:.2f} MH/s")
            print(f"Total Network SPR Mined per Day: {block_reward * 86400:.2f}")
            print(f"Current Blockreward: {block_reward:.2f} SPR")
            print(f"Current Price (USD per SPR): ${spr_price:.4f}")
            print(f"Your Portion of the Network Hashrate: ({(my_hashrate * 1e-3) / network_hashrate:.3%})")
            print(f"Your Current Hashrate: {my_hashrate:.2f} KH/s")

            rewards = calculate_estimated_rewards(network_hashrate, my_hashrate, block_reward, spr_price)
            print_estimated_rewards(rewards)

            yearly_energy_consumption_kwh = total_power_watts / 1000 * 24 * 365

            if yearly_limit_kwh is None:
                above_limit = False
            else:
                if yearly_energy_consumption_kwh > yearly_limit_kwh:
                    above_limit = True
                else:
                    above_limit = False

            daily_cost_usd, day_cost_usd_per_kwh, night_cost_usd_per_kwh = calculate_electricity_cost(total_power_watts, above_limit)

            print(f"\nTotal Power Consumption: {total_power_watts:.2f} W")
            print(f"Electricity Cost (Daily): ${daily_cost_usd:.2f} per day")
            if tariff_type == "dual":
                print(f"Electricity Cost per kWh (Day Tariff): ${day_cost_usd_per_kwh:.2f}")
                print(f"Electricity Cost per kWh (Night Tariff): ${night_cost_usd_per_kwh:.2f}")
            elif tariff_type == "single":
                print(f"Electricity Cost per kWh (Single Tariff): ${day_cost_usd_per_kwh:.2f}")

            print(f"\nYearly Energy Consumption: {yearly_energy_consumption_kwh:.2f} kWh")
            if yearly_limit_kwh is not None:
                print(f"Yearly Limit: {yearly_limit_kwh:.2f} kWh")
                if yearly_energy_consumption_kwh > yearly_limit_kwh:
                    print(f"Exceeding Yearly Limit by: {yearly_energy_consumption_kwh - yearly_limit_kwh:.2f} kWh")
                else:
                    print(f"Under Yearly Limit by: {yearly_limit_kwh - yearly_energy_consumption_kwh:.2f} kWh")

            if rewards['daily'][1] < daily_cost_usd:
                print("Mining is not profitable with the increased tariffs.")
            else:
                print("Mining is profitable.")

            print_loading_bar(loading_bar_duration)

    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    # Ask user for input
    tariff_type = get_str_input("Enter tariff type (dual/single): ", ["dual", "single"])

    if tariff_type == "dual":
        day_tariff_usd_per_kwh = get_float_input("Enter day tariff in USD per kWh: ")
        night_tariff_usd_per_kwh = get_float_input("Enter night tariff in USD per kWh: ")
        day_hours = get_float_input("Enter number of day hours per day: ")
        night_hours = get_float_input("Enter number of night hours per day: ")
    elif tariff_type == "single":
        single_tariff_usd_per_kwh = get_float_input("Enter single tariff in USD per kWh: ")

    total_power_watts = get_float_input("Enter total power consumption in watts: ")
    yearly_limit_input = input("Enter yearly limit in kWh (if any, else enter N/A): ").strip().lower()
    if yearly_limit_input == "n/a":
        yearly_limit_kwh = None
        high_single_tariff_usd_per_kwh = 0
        high_day_tariff_usd_per_kwh = 0
        high_night_tariff_usd_per_kwh = 0
    else:
        yearly_limit_kwh = float(yearly_limit_input)
        if yearly_limit_kwh > 0:
            if tariff_type == "dual":
                high_day_tariff_usd_per_kwh = get_float_input("Enter high day tariff in USD per kWh (beyond limit): ")
                high_night_tariff_usd_per_kwh = get_float_input("Enter high night tariff in USD per kWh (beyond limit): ")
            elif tariff_type == "single":
                high_single_tariff_usd_per_kwh = get_float_input("Enter high single tariff in USD per kWh (beyond limit): ")

    loading_bar_minutes = get_float_input("Enter the duration for the loading bar in minutes: ")
    loading_bar_duration = int(loading_bar_minutes * 60)  # Convert minutes to seconds

    main()
