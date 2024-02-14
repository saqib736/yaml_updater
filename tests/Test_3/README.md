# Test 3

## Description

Test the `yaml_updater` application that takes as an input two YAML files, `current_config`
and `replace_behaviour_check`, and updates `current_config` as follows:
- Force the update of `current_config` by replacing the values of the currently
  existing fields with the values from `replace_behaviour_check` and adding or removing 
  the fields according  to the requirement mentioned above. This is basically replacing 
  the current config file with the new one.