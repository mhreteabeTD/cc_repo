import os
import subprocess
import pandas as pd
import hashlib
import time
from itertools import product
from codecarbon import EmissionsTracker

# Configurable parameters
CONFIG = {
    "directory": "scripts",  # Directory containing the Python notebooks
    "output_csv": "outputs/energy_usage.csv",  # Output CSV file for energy data
    "run_log": "outputs/run_log.csv",  # Log file to track execution state
    "codecarbon_output_dir": "./codecarbon_output",  # Directory for Code Carbon outputs
    "device_id": "mhreteabe_pc",  # Device ID for tracking
    "repetition_number": 1,  # Number of repetitions for each script
    "cooling_period_secs": 2  # Cooling period between runs
}

# Code Carbon specific configurations
CC_CONFIG_OPTIONS = {
    "measure_power_secs": [5, 15, 30][:1],
    "tracking_mode": ["machine", "process"][:1],
    "log_level": ["debug", "info", "warning", "error", "critical"][:1]
}

# Initialize the run log if it does not exist
if not os.path.exists(CONFIG['run_log']):
    pd.DataFrame(columns=["Run ID", "Run Number", "Completed"]).to_csv(CONFIG['run_log'], index=False)

def generate_run_id(device_id, script_name, measure_power_secs, tracking_mode, log_level):
    unique_string = f"{device_id}-{script_name}-{measure_power_secs}-{tracking_mode}-{log_level}"
    return hashlib.sha256(unique_string.encode()).hexdigest()

def run_already_completed(run_id, run_number):
    run_log = pd.read_csv(CONFIG['run_log'])
    completed_runs = run_log[(run_log['Run ID'] == run_id) & (run_log['Run Number'] == run_number) & (run_log['Completed'] == True)]
    return not completed_runs.empty

def mark_run_completed(run_id, run_number):
    run_log = pd.read_csv(CONFIG['run_log'])
    new_entry = pd.DataFrame({"Run ID": [run_id], "Run Number": [run_number], "Completed": [True]})
    updated_log = pd.concat([run_log, new_entry], ignore_index=True)
    updated_log.to_csv(CONFIG['run_log'], index=False)

def load_existing_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Device ID", "Script", "Run ID", "Run Number", "Measure Power Secs", "Tracking Mode", "Log Level",
                                     "Energy (kWh)", "Duration (s)", "CPU Energy", "GPU Energy", "RAM Energy", 
                                     "Total Energy Consumed", "Measurement Type", "CPU Model", "GPU Model", "RAM", "OS"])

import os
import pandas as pd
import subprocess
import time
from itertools import product
from codecarbon import EmissionsTracker

def run_scripts_and_log():
    run_data = load_existing_data(CONFIG['output_csv'])

    scripts = [f for f in os.listdir(CONFIG['directory']) if f.endswith('.py')]
    os.makedirs(CONFIG['codecarbon_output_dir'], exist_ok=True)

    total_runs = len(scripts) * len(CC_CONFIG_OPTIONS['measure_power_secs']) * len(CC_CONFIG_OPTIONS['tracking_mode']) * len(CC_CONFIG_OPTIONS['log_level']) * CONFIG['repetition_number']
    current_run = 0  # Track the number of completed runs

    for measure_power_secs, tracking_mode, log_level in product(CC_CONFIG_OPTIONS['measure_power_secs'], CC_CONFIG_OPTIONS['tracking_mode'], CC_CONFIG_OPTIONS['log_level']):
        for script in scripts:
            run_id = generate_run_id(CONFIG['device_id'], script, measure_power_secs, tracking_mode, log_level)
            for i in range(CONFIG['repetition_number']):
                current_run += 1

                # Skip if the run has already been completed
                if run_already_completed(run_id, i + 1):
                    continue

                # Output to the console
                print(f"Running script {script}, configuration (Measure Power Secs: {measure_power_secs}, Tracking Mode: {tracking_mode}, Log Level: {log_level}), Run {i + 1} of {CONFIG['repetition_number']}")
                print(f"Overall progress: {current_run} of {total_runs} runs")

                # Start energy tracking and run the script
                tracker = EmissionsTracker(output_dir=CONFIG['codecarbon_output_dir'], measure_power_secs=measure_power_secs, tracking_mode=tracking_mode, log_level=log_level)
                tracker.start()

                subprocess.run(['python3', os.path.join(CONFIG['directory'], script)], check=True)

                emissions = tracker.stop()

                # Load emissions data and append to run data
                if os.path.exists(os.path.join(CONFIG['codecarbon_output_dir'], "emissions.csv")):
                    cc_data = pd.read_csv(os.path.join(CONFIG['codecarbon_output_dir'], "emissions.csv"))
                    new_row = pd.DataFrame({
                        "Device ID": [CONFIG['device_id']], "Script": [script], "Run ID": [run_id], "Run Number": [i + 1], "Measure Power Secs": [measure_power_secs],
                        "Tracking Mode": [tracking_mode], "Log Level": [log_level], "Energy (kWh)": [cc_data.iloc[0]['energy_consumed']],
                        "Duration (s)": [cc_data.iloc[0]['duration']], "CPU Energy": [cc_data.iloc[0]['cpu_energy']], "GPU Energy": [cc_data.iloc[0]['gpu_energy']],
                        "RAM Energy": [cc_data.iloc[0]['ram_energy']], "Total Energy Consumed": [cc_data.iloc[0]['energy_consumed']], "Measurement Type": ["CC"],
                        "CPU Model": [cc_data.iloc[0]['cpu_model']], "GPU Model": [cc_data.iloc[0]['gpu_model']], "RAM": [cc_data.iloc[0]['ram_total_size']],
                        "OS": [cc_data.iloc[0]['os']]
                    })
                    run_data = pd.concat([run_data, new_row], ignore_index=True)
                    os.remove(os.path.join(CONFIG['codecarbon_output_dir'], "emissions.csv"))

                # Mark the run as completed and save results
                mark_run_completed(run_id, i + 1)
                run_data.to_csv(CONFIG['output_csv'], index=False)  # Save after each run completion

                # Optional cooling period
                if i < CONFIG['repetition_number'] - 1:
                    print(f"Cooling down for {CONFIG['cooling_period_secs']} seconds before next run")
                    time.sleep(CONFIG['cooling_period_secs'])

                print(f"Run {i + 1} of script {script} completed.\n")


if __name__ == "__main__":
    run_scripts_and_log()
