from dynaconf import Dynaconf

config = Dynaconf(
    settings_files=['.secrets.toml'],
)