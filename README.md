# YAML UPDATER
![MIT License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

The YAML UPDATER is a Python-based utility designed to streamline the process of updating YAML configuration files. It intelligently merges the content of a `current_version` YAML file with updates found in a `new_version` YAML file. The application supports adding new fields, keeping existing values, and removing obsolete entries. Additionally, users have the option to force updates in specific ways and to set the log level for operation feedback.

## Installation

### Prerequisites

Before installing the YAML UPDATER, ensure you have `Python>=3.8` installed on your system. It's recommended to use a virtual environment for Python projects to avoid conflicts between project dependencies.

### Steps

1. **Create and Activate a Virtual Environment**

   Open your terminal and navigate to your project directory. Create a virtual environment by running:

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:

     ```cmd
     .\venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

2. **Clone the Repository**

   With the virtual environment activated, clone the YAML UPDATER repository to your desired location:

   ```bash
   git clone https://github.com/saqib736/yaml_updater.git
   ```

   Navigate into the root directory of the repository:

   ```bash
   cd yaml-updater
   ```

3. **Install Dependencies**

   Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install the Application**

   Still in the root directory of the repository, install the YAML UPDATER application:

   ```bash
   pip install .
   ```

## Usage

The YAML UPDATER application is designed to be straightforward to use from the command line. Here's how you can leverage its capabilities:

### Basic Command Structure

```bash
config-updater <current.yaml_path> <new.yaml_path> [--force] [--replace] [--log-level LEVEL]
```

### Arguments

- `current.yaml_path`: Path to the current YAML file.
- `new.yaml_path`: Path to the new YAML file with updates.
- `--force`: (Optional) Forces the update of `current_version` by only replacing the values of currently existing fields with the values from `new_version`.
- `--replace`: (Optional) Forces the update of `current_version` by replacing the values of currently existing fields with the values from `new_version` and adding or removing fields as needed.
- `--log-level`: (Optional) Specifies the log level for the operation. Available levels are ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]. Default is "INFO".

### Examples

**Default Behavior (Merge and Update)**

```bash
config-updater current.yaml new.yaml
```

**Force Update (Replace Existing Values Only)**

```bash
config-updater current.yaml new.yaml --force
```

**Full Update (Replace, Add, and Remove)**

```bash
config-updater current.yaml new.yaml --replace
```

**Set Log Level**

```bash
config-updater current.yaml new.yaml --log-level debug
```

For detailed information about the command-line options, refer to the help documentation:

```bash
config-updater --help
```

## Testing

To test the YAML UPDATER application with PYTEST move into the `\tests` directory and run the following command from the terminal to check different test cases:

```bash
pytest test_updater.py -vv
```

- `-vv`: This argument is for the verbose mode to get the complete details of the test.

## Disclaimer
This project was the test project for the software QA engineer position. It was ranked at number 1 by the organization. 

## License

This project is licensed under the MIT License - see the LICENSE file for details.

![MIT License](https://img.shields.io/badge/license-MIT-green.svg)
