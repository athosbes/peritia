# peritia
Digital Forensics Toolkit: A comprehensive collection of scripts and tools for common digital forensic investigations


# 1 - Windows Software Inventory with Hash Generator (software_inventory.py)

## Overview
This Python script collects information about installed software on a Windows machine, generates CSV files with detailed software data, and computes SHA-256 hashes for the generated files. It supports Windows 7 through Windows 11. The output files are saved in a timestamped directory, and an additional file containing the hashes of all generated files is created.

## Features
* **Software Inventory**: Collects software data from the Windows registry, WMIC, and Winget.
* **Hash Generation**: Computes SHA-256 hashes of all generated files.
* **Output Organization**: Saves output in a timestamped directory, including a unique identifier for the machine.

## Prerequisites
* Python 3.6 or higher
* `pyinstaller` package for creating an executable

## Installation
1. **Clone the Repository**

   ```bash
   git clone https://github.com/athosbes/peritia.git
   cd peritia
   ```

2. **Install Required Packages**
   Install the required Python packages using `pip`:

   ```bash
   pip install wmi pyinstaller
   ```

3. **Generate executable file**
   Install the required Python packages using `pip`:

   ```bash
   pip install wmi pyinstaller
   ```

## Script Overview
### Script Files
* `software_inventory.py`: Main script for gathering software data and generating files.

### Key Functions
* `run_command(command)`: Executes a command and returns its output.
* `get_wmic_data()`: Retrieves installed software information using WMIC and saves it to a CSV file.
* `get_winget_data()`: Retrieves installed software information using Winget and saves it to a CSV file.
* `get_installed_software_from_registry()`: Retrieves installed software information from the Windows registry and saves it to a CSV file.
* `save_hashes(file_paths)`: Computes SHA-256 hashes of the generated files and saves them to a CSV file.

### Unique Identifier
A unique identifier based on the MAC address and system information is used to ensure the machine's uniqueness in the output directory.

## Usage
1. **Run the Script**
   Execute the script using Python:

   ```bash
   python software_inventory.py
   ```

2. **Generate Executable (Optional)**
   To create an executable version of the script, use `pyinstaller`:

   ```bash
   pyinstaller --onefile --noconsole software_inventory.py
   ```
   This will generate an executable file in the `dist` directory.

## Output
* **CSV Files**: Located in the timestamped output directory, including:
   * `wmic_products.csv`: Software list from WMIC.
   * `winget_list.csv`: Software list from Winget.
   * `installed_software.csv`: Software list from the Windows registry.
* **Hash File**: `file_hashes.csv` contains SHA-256 hashes of all generated files.

## Troubleshooting
* **Command Not Found**: If `pyinstaller` is not recognized, ensure it's installed and included in your PATH.
* **Execution Errors**: Ensure the script has the necessary permissions and that all dependencies are installed correctly.

## Contributing
Contributions are welcome! Please submit issues or pull requests through GitHub.

## License
This project is licensed under the MIT License - see the LICENSE file for details.