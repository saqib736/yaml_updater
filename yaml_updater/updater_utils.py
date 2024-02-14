import os
import daiquiri
import logging
from ruamel.yaml import YAML
from typing import Dict, Any

# Setup logger for utility functions
daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)

def load_yaml(path: str) -> Dict[str, Any]:
    """
    Load a YAML file and return its contents as a dictionary.

    :param path: Path to the YAML file.
    :return: Contents of the YAML file as a dictionary.
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    
    # Check if the file exists
    if not os.path.exists(path):
        logger.error(f"YAML file at {path} does not exist.")
        raise FileNotFoundError(f"YAML file at {path} does not exist.")
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            logger.debug(f"Loading YAML file from {path}")
            data = yaml.load(file)
            return data if data is not None else {}
    except Exception as e:
        logger.error(f"Failed to load YAML file at {path}: {e}")
        raise

def save_yaml(path: str, data: Dict[str, Any]):
    """
    Save a dictionary to a YAML file.

    :param path: Path to save the YAML file.
    :param data: Dictionary containing the data to save.
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    
    # Check if the file is writable
    if not os.access(path, os.W_OK):
        logger.error(f"File at {path} is not writable.")
        raise PermissionError(f"File at {path} is not writable.")
    
    try:
        logger.debug(f"Saving updated configuration to {path}")
        with open(path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file)
            logger.info(f"Configuration successfully saved to {path}")
    except Exception as e:
        logger.error(f"Failed to save YAML file at {path}: {e}")
        raise
