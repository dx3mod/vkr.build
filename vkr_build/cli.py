import argparse
from pathlib import Path

cli_parser = argparse.ArgumentParser(
    prog="vkr-build",
    description="Автоматизированное решение вёрстки курсовых/дипломных работ.",
)

cli_parser.add_argument(
    "-c", "--config-path", dest="config_path", type=Path, default=Path("document.toml")
)

cli_parser.add_argument("--validate-only", dest="validate_only", action="store_true")

cli_parser.add_argument("--html-only", dest="html_only", action="store_true")
