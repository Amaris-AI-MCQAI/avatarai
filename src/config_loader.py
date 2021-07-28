import os
import yaml

"""
Byan: python configuration loader
"""

DEPLOY = "development"
if "DEPLOY" in os.environ:
    DEPLOY = os.environ["DEPLOY"]


def load_config() -> dict:
    config = None

    with open(f"./config/{DEPLOY}.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

        stream.close()

    return config


config = load_config()
model_config = config["model"]



