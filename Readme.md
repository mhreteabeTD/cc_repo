
# Code Carbon Accuracy Replication Package

## Overview
This package includes a Python script designed to execute Jupyter notebooks and log the energy consumption of each run. The script is crafted with replication and consistency in mind, ensuring that each notebook is executed under specified configurations multiple times to average out any anomalies in energy usage measurements.

## Setup Instructions

1. **Open Command Line Interface**: Launch your command line interface or terminal.
2. **Navigate to Project Directory**:
   Change your current directory to the location of the `CODE_CARBON_ACCURACY_REPLICATION_PACKAGE`.
   ```bash
   cd path/to/CODE_CARBON_ACCURACY_REPLICATION_PACKAGE
   ```
3. **Install Dependencies**:
   Install the necessary Python packages listed in `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```
4. **Execute the Script**:
   Run the script using Python.
   ```bash
   python script_runner_and_logger.py
   ```

## Configuration Variables
Configure the script via the `CONFIG` dictionary. Each variable is described below:

- **`directory`**: Directory containing the Jupyter notebooks to be executed. Defaults to the current directory (".").
- **`output_csv`**: Filename for the CSV file storing energy consumption data. Defaults to "energy_usage.csv".
- **`run_log`**: Filename for the log file tracking the execution status of each run, facilitating the resume feature. Defaults to "run_log.csv".
- **`codecarbon_output_dir`**: Specifies where CodeCarbon will output its emissions data. Defaults to "./codecarbon_output".
- **`device_id`**: Name of the device on which the scripts are run, used to generate unique run IDs for tracking. Example: "JohnDoeLaptop".
- **`repetition_number`**: Number of executions per script to ensure measurement accuracy. Defaults to 5.
- **`cooling_period_secs`**: Cooling period in seconds between runs to prevent performance biases due to thermal effects. Defaults to 5 seconds.

## Script Execution Details
- **Unique Run Identification**: Each script run is uniquely identified by a `run_id`, generated from the `device_id`, script name, and the CodeCarbon configuration settings. This ID ensures distinct logging for each run.
- **Pause and Resume Capability**: Execution can be paused and later resumed. On restart, the script continues from the last incomplete run, using the log file to skip completed runs.
- **Output Data**: Logs include energy consumption, execution duration, CPU and GPU energy usage, and carbon emissions for each run, saved in the designated `output_csv` file.

## Output
Energy consumption measurement results are saved in the `output_csv` file located in the directory specified in `CONFIG['output_csv']`.
