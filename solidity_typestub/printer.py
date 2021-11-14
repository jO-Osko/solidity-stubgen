import dataclasses
import json
import os

import black

from .solidity_types import Contract, header


@dataclasses.dataclass
class PrintConfig:
    output_folder: str = "artifacts"
    format: bool = True
    include_header: bool = True


def print_file(input_file: str, config: PrintConfig) -> None:
    os.makedirs(config.output_folder, exist_ok=True)

    json_data = json.load(open(input_file, "r"))
    output_file = os.path.join(
        config.output_folder, f"{os.path.basename(input_file).replace('.json', '.pyi')}"
    )

    contract = Contract.from_json(json_data)
    contract_stub = contract.stub_source()

    if config.include_header:
        contract_stub = header + contract_stub

    full_text = "\n".join(contract_stub)
    if config.format:
        full_text = black.format_str(full_text, mode=black.Mode(is_pyi=True))

    print(full_text, file=open(output_file, "w"), end="")
    if not os.path.isfile(os.path.join(config.output_folder, "__init__.py")):
        open(os.path.join(config.output_folder, "__init__.py"), "w").write(
            "# Dummy file to enable .pyi imports\n"
        )


def process_folder(input_folder: str, config: PrintConfig) -> None:
    for (dirpath, _, filenames) in os.walk(input_folder):
        for filename in filenames:
            if filename.endswith(".json"):
                print_file(os.path.join(dirpath, filename), config)
