import configparser
import os

from baroque import defaults


def get_config_setting(setting, default=None):
    configuration = _load_config()
    try:
        result = configuration.get("defaults", setting)
        return result
    except (configparser.NoOptionError, configparser.NoSectionError):
        return default


def _load_config():
    config_file = defaults.CONFIG
    config = configparser.ConfigParser()
    config.read(config_file)
    if not os.path.exists(config_file):
        print("BAroQUe configuration file not found")
        configure = input("Would you like to create a configuration file? (y/n) ").strip()
        if configure.lower() in ["y", "yes"]:
            _create_config(config, config_file)
        else:
            print("Skipping create config.")
    return config


def _create_config(config, config_file):
    reports_dir_input = input("Enter a default reports directory: ")
    reports_dir = os.path.normpath(reports_dir_input.strip('"\' '))
    config.add_section("defaults")
    config.set("defaults", "destination", reports_dir)
    _save_config(config, config_file)


def _save_config(config, config_file):
    with open(config_file, "w") as f:
        config.write(f)
