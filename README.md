# ansys-api-result-explorer gRPC Interface Package

This Python package contains the auto-generated gRPC Python interface files for Result Explorer.

## Installation

Provided that these wheels have been published to public PyPI, they can be installed with:

```bash
pip install ansys-api-result-explorer
```

Otherwise, they can be installed from sources with:

```bash
pip install "ansys-api-result-explorer @ git+https://github.com/ansys/ansys-api-result-explorer.git"
```

## Build

Create a virtual environment

```
uv venv
.venv\Scripts\activate
```

Install build requirements

```
uv sync --group build
```

Run the build script to run the proto compiler

```
python scripts/proto_compile.py
```
