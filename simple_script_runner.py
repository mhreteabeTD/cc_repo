import os
import subprocess
import time

# Configuration options
CONFIG = {
    'directory': 'scripts',  # Directory where Python scripts are stored
    'repetition_number': 3,  # Number of times to run each script
    'cooling_period_secs': 2,  # Cooldown period between script runs in seconds
    'log_file': 'outputs/pm_run_log.txt'  # Log file to track the run order
}

def log_run(script, run_number, repetition_number):
    # Log the script run information to a file
    with open(CONFIG['log_file'], 'a') as log_file:
        log_file.write(f"Running script: {script}, Run {run_number} of {repetition_number}\n")

def run_scripts():
    # Get the list of Python scripts in the configured directory
    scripts = [f for f in os.listdir(CONFIG['directory']) if f.endswith('.py')]

    # Total number of runs
    total_runs = len(scripts) * CONFIG['repetition_number']
    current_run = 0  # Track the current run number

    # Clear log file at the start of the run
    with open(CONFIG['log_file'], 'w') as log_file:
        log_file.write("Run log for script execution:\n")

    for script in scripts:
        for i in range(CONFIG['repetition_number']):
            current_run += 1

            # Print progress to the console
            print(f"Running script {script}, Run {i + 1} of {CONFIG['repetition_number']}")
            print(f"Overall progress: {current_run} of {total_runs} runs")

            # Log the run order
            log_run(script, i + 1, CONFIG['repetition_number'])

            # Run the script
            subprocess.run(['python3', os.path.join(CONFIG['directory'], script)], check=True)

            # Optional cooling period between runs
            if i < CONFIG['repetition_number'] - 1:
                print(f"Cooling down for {CONFIG['cooling_period_secs']} seconds before next run")
                time.sleep(CONFIG['cooling_period_secs'])

            # Confirm run completion
            print(f"Run {i + 1} of script {script} completed.\n")

# Example of how to use this script
if __name__ == "__main__":
    run_scripts()
