# jO-Osko's stub generator

Generate `.pyi` stubs from abi files to ease typechecking and development with `web3py`.

## Features

Solidity typestub generates `.pyi` files that enable type directed code completion and typechecking of web3py wrappers around solidity contracts.

## Usage

Install using pip `pip install solidity_typestub`. 
Invoke it with `solidity_typestub path/to/input/file_or_folder.json path/to/another/file/or/folder ...`. 
Stub generator generates stubs for input files or recursively searches the provided input folder for `.json` files with abi.
The generated stubs are written to the folder `artifacts` (configurable) and a dummy `__init__.py` is generated  (provided it does not exist) to make them importable.

Available options:

- `--no-format`, `-nf`: Do not autoformat generated files using black (default: use autoformatter)
- `--output <directory_name>`: Specify output directory (default: `artifacts`)

```python3
contract: SampleContract = w3.eth.contract(address=sample_address, abi=sample_abi)
reveal_type(contract.functions.exampleFun.call)
# note: Revealed type is "def (_arg1: builtins.int, _arg2: builtins.list[builtins.bool]) -> Tuple[builtins.int, builtins.str]"
```

## Roadmap
- Support custom structs
- Support api acquisition of abi files from blockexplorer and blockscout
- More configuration options
- Provide support for `transact()` types
- Provide workable contracts a-la truffle
- Generate stub files directly from solidity files using `solcx`

## Contributing
Any contributions are welcome (PR, Issues, documentation, comments).

## Acknowledgements
This work builds greatly on ocaml solidity developed by ocamlpro and modified a bit.

AFLabs and Flare foundation for testing and bug reporting.

----- 

jO-Osko