import os
import subprocess
import pytest
from ruamel.yaml import YAML

# Initialize YAML processor with specific formatting preferences
yaml = YAML()
yaml.preserve_quotes = True  # Preserve quotes in YAML files
yaml.indent(mapping=2, sequence=4, offset=2)  # Set indentation preferences

# Script and file paths
APP_SCRIPT = "config-updater"
CURRENT_YAML_PATH = "./current_config.yaml"
DEFAULT_BEHAVIOR_PATH = "./Test_1/default_behaviour_check.yaml"
FORCE_BEHAVIOR_PATH = "./Test_2/force_behaviour_check.yaml"
REPLACE_BEHAVIOR_PATH = "./Test_3/replace_behaviour_check.yaml"

def read_yaml(file_path):
    """Reads YAML content from a file and returns it."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.load(file)

def write_yaml(file_path, data):
    """Writes data to a YAML file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Setup and teardown fixture that runs before and after each test.
    It ensures the original YAML configuration is restored after each test.
    """
    original_data = read_yaml(CURRENT_YAML_PATH)
    yield
    write_yaml(CURRENT_YAML_PATH, original_data)

def test_default_behavior():
    """Tests the default behavior of the YAML updater script."""
    subprocess.run([APP_SCRIPT, CURRENT_YAML_PATH, DEFAULT_BEHAVIOR_PATH], check=True)
    result = read_yaml(CURRENT_YAML_PATH)
    expected = read_yaml("./Test_1/expected_default_behaviour_result.yaml")
    assert result == expected, "Default behavior failed."

def test_force_behavior():
    """Tests the --force flag behavior of the YAML updater script."""
    subprocess.run([APP_SCRIPT, CURRENT_YAML_PATH, FORCE_BEHAVIOR_PATH, "--force"], check=True)
    result = read_yaml(CURRENT_YAML_PATH)
    expected = read_yaml("./Test_2/expected_force_behaviour_result.yaml")
    assert result == expected, "Force update failed."

def test_replace_behavior():
    """Tests the --replace flag behavior of the YAML updater script."""
    subprocess.run([APP_SCRIPT, CURRENT_YAML_PATH, REPLACE_BEHAVIOR_PATH, "--replace"], check=True)
    result = read_yaml(CURRENT_YAML_PATH)
    expected = read_yaml("./Test_3/expected_replace_behaviour_result.yaml")
    assert result == expected, "Replace behavior failed."

def test_log_level():
    """Tests the --log-level flag for setting log verbosity."""
    result = subprocess.run([APP_SCRIPT, CURRENT_YAML_PATH, DEFAULT_BEHAVIOR_PATH, "--log-level", "DEBUG"], capture_output=True)
    logs = result.stderr.decode('utf-8')
    assert "DEBUG" in logs, "Log level DEBUG not found in logs."

@pytest.mark.parametrize("empty_file_path", ["./Test_4/current_empty.yaml", "./Test_4/updated_empty.yaml"])
def test_empty_files(empty_file_path):
    """Tests handling of empty YAML files."""
    subprocess.run([APP_SCRIPT, CURRENT_YAML_PATH, empty_file_path], check=True)
    result = read_yaml(CURRENT_YAML_PATH)
    assert result == {}, "Failed to handle empty file gracefully."

def test_invalid_yaml_format():
    """Tests handling of invalid YAML format."""
    invalid_yaml_path = "./Test_5/invalid_format.yaml"
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run([APP_SCRIPT, CURRENT_YAML_PATH, invalid_yaml_path], check=True)

def test_read_only_file():
    """Tests behavior with read-only YAML files."""
    read_only_path = "./Test_6/read_only_current_config.yaml"
    os.chmod(read_only_path, 0o444)  # Make the file read-only
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run([APP_SCRIPT, read_only_path, DEFAULT_BEHAVIOR_PATH], check=True)

def test_non_existent_file():
    """Tests behavior with non-existent YAML files."""
    non_existent_path = "./Test_1/non_existent.yaml"
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run([APP_SCRIPT, CURRENT_YAML_PATH, non_existent_path], check=True)

def test_force_and_replace_behavior():
    """Tests behavior when both --force and --replace flags are used."""
    subprocess.run([APP_SCRIPT, CURRENT_YAML_PATH, REPLACE_BEHAVIOR_PATH, "--force", "--replace"], check=True)
    result = read_yaml(CURRENT_YAML_PATH)
    expected = read_yaml("./Test_3/expected_replace_behaviour_result.yaml")
    assert result == expected, "Both --force and --replace flags handling failed."
