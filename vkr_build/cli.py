import argparse
from pathlib import Path

cli_parser = argparse.ArgumentParser(
    prog="vkr-build",
    description="Автоматизированное решение вёрстки курсовых/дипломных работ.",
)

cli_parser.add_argument(
    "-c", "--config-path", dest="config_path", type=Path, default=Path("document.toml")
)
