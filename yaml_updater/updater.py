import argparse
import daiquiri
import logging
from .updater_utils import load_yaml, save_yaml

# Setup logger for info level
daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger(__name__)


class ConfigUpdater:
    def __init__(self, current_path, new_path, force_update=False, replace_update=False):
        """Initialize the ConfigUpdater with current and new configuration paths."""
        self.current_path = current_path
        self.new_path = new_path
        self.force_update = force_update
        self.replace_update = replace_update
        # Load current and new configurations from YAML files
        self.current_config = load_yaml(current_path)
        self.new_config = load_yaml(new_path)

    def deep_merge_dicts(self, source, updates, add_new_keys=True, remove_absent_keys=True, force_update=False):
        """Merges two dictionaries, with options to add new keys and remove absent ones."""
        keys_in_source = list(source.keys())
        for key in keys_in_source:
            if key in updates:
                if isinstance(source[key], dict) and isinstance(updates[key], dict):
                    self.deep_merge_dicts(source[key], updates[key], add_new_keys, remove_absent_keys, force_update)
                elif force_update:
                    source[key] = updates[key]
            elif remove_absent_keys:
                del source[key]

        if add_new_keys:
            for key, value in updates.items():
                if key not in source:
                    source[key] = value

    def update_config(self):
        """Update configuration based on the update mode."""
        if self.replace_update:
            if self.force_update:
                logger.info("Both --force and --replace were provided; --replace takes precedence.")
            self.current_config = self.new_config
            logger.info("Configuration replaced with the new file.")
        elif self.force_update:
            self.deep_merge_dicts(self.current_config, self.new_config, False, False, True)
            logger.info("Existing fields updated with new configuration values.")
        else:
            self.deep_merge_dicts(self.current_config, self.new_config)
            self.prune_extra_keys(self.current_config, self.new_config)
            logger.info("Configuration updated with new values.")
        save_yaml(self.current_path, self.current_config)

    def prune_extra_keys(self, current, new):
        """Removing extra keys."""
        keys_to_remove = set(current.keys()) - set(new.keys())
        for key in keys_to_remove:
            del current[key]
        for key in current:
            if key in new and isinstance(current[key], dict) and isinstance(new[key], dict):
                self.prune_extra_keys(current[key], new[key])


def main():
    parser = argparse.ArgumentParser(description="Update YAML configuration files.")
    parser.add_argument("current_path", help="Path to the current YAML file")
    parser.add_argument("new_path", help="Path to the new YAML file")
    parser.add_argument("--force", action="store_true", help="Force update existing fields only")
    parser.add_argument("--replace", action="store_true", help="Replace entire configuration")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level")

    args = parser.parse_args()
    daiquiri.setup(level=getattr(logging, args.log_level.upper(), None))
    logger.info("Starting configuration update...")

    updater = ConfigUpdater(args.current_path, args.new_path, args.force, args.replace)
    updater.update_config()

    logger.info("Configuration update completed successfully.")

if __name__ == "__main__":
    main()
