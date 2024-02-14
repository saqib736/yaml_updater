# Test 1

## Description

Test the `yaml_updater` application that takes as an input two YAML files, `current_config`
and `default_behaviour_check`, and updates `current_config` as follows:
- If a field of `default_behaviour_check` is not present in `current_config`, it should be
  added to `current_version` with its value set to the value from `default_behaviour_check`.
- If a field of `default_behaviour_check` is present in `current_config`, it should keep the
  value from `current_config`.
- If a field of `current_config` is not present in `default_behaviour_check`, it should be
  removed from `current_config`.