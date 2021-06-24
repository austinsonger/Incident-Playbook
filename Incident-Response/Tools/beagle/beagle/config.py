import os
from configparser import ConfigParser

# Inspired by the Airflow Configuration class
# https://github.com/apache/airflow/blob/master/airflow/configuration.py


class BeagleConfig(ConfigParser):
    @staticmethod
    def _env_var_name(section: str, key: str):
        return f"BEAGLE__{section.upper()}__{key.upper()}"

    def _get_env_var_option(self, section, key):
        # must have format AIRFLOW__{SECTION}__{KEY} (note double underscore)
        env_var = self._env_var_name(section, key)
        if env_var in os.environ:
            return expand_env_var(os.environ[env_var])
        else:
            return None

    def get(self, section: str, key: str, **kwargs):  # type: ignore
        section = str(section).lower()
        key = str(key).lower()

        # Try and get the enviroment variable
        value = self._get_env_var_option(section, key)
        if value:
            return value

        if super(BeagleConfig, self).has_option(section, key):
            # Use the parent's methods to get the actual config here to be able to
            # separate the config from default config.
            return expand_env_var(super(BeagleConfig, self).get(section, key, **kwargs))


def expand_env_var(env_var: str):
    """
    Expands (potentially nested) env vars by repeatedly applying
    `expandvars` and `expanduser` until interpolation stops having
    any effect.
    """
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        else:
            env_var = interpolated


# Get the parent path
config_dir = os.path.join(os.path.dirname(__file__), "config_templates")

# Export the default config
Config = BeagleConfig()
Config.read(f"{config_dir}/beagle_default.cfg")
