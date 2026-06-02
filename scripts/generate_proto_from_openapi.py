"""
Script to generate server_models.proto from OpenAPI spec.

Usage:
    python generate_proto_from_openapi.py [openapi_spec]

    openapi_spec: URL or file path to OpenAPI JSON/YAML spec
                  Default: http://127.0.0.1:5100/api/v1/openapi.json
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

OPENAPI_GENERATOR_VERSION = "7.19.0"


def main():
    # Get OpenAPI spec location from command line or use default
    if len(sys.argv) > 1:
        openapi_spec = sys.argv[1]
    else:
        openapi_spec = "http://127.0.0.1:5100/api/v1/openapi.json"
        print(f"No OpenAPI spec provided, using default: {openapi_spec}")
        print("Make sure the server is running, or provide a file path/URL as argument")
        print()
    # Get the repository root
    script_dir = Path(__file__).parent.parent
    target_file = script_dir / "proto" / "server_models.proto"

    print("Creating temporary directory...")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        venv_path = temp_path / ".venv"

        print(f"Working directory: {temp_path}")

        # Create venv with uv
        print("Creating virtual environment with uv...")
        subprocess.run(["uv", "venv", str(venv_path)], check=True, cwd=temp_path)

        # Determine the executable paths
        if os.name == "nt":  # Windows
            openapi_cli = venv_path / "Scripts" / "openapi-generator-cli.exe"
        else:  # Unix-like
            openapi_cli = venv_path / "bin" / "openapi-generator-cli"

        # Install openapi-generator-cli
        print("Installing openapi-generator-cli...")
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                f"openapi-generator-cli=={OPENAPI_GENERATOR_VERSION}",
            ],
            check=True,
            cwd=temp_path,
            env={**os.environ, "VIRTUAL_ENV": str(venv_path)},
        )

        # Run openapi-generator-cli
        print(f"Running openapi-generator-cli with spec: {openapi_spec}...")
        output_dir = temp_path / "generated"
        result = subprocess.run(
            [
                str(openapi_cli),
                "generate",
                "-g",
                "protobuf-schema",
                "-i",
                openapi_spec,
                "-o",
                str(output_dir),
                "--remove-operation-id-prefix",
                "--additional-properties=aggregateModelsName=server_models",
                "--additional-properties=numberedFieldNumberList=true",
            ],
            cwd=temp_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("ERROR: openapi-generator-cli failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            raise subprocess.CalledProcessError(
                result.returncode, result.args, result.stdout, result.stderr
            )

        print("STDOUT:", result.stdout)

        # Find the generated server_models.proto file
        # List what was actually generated
        if output_dir.exists():
            print(f"Contents of {output_dir}:")
            for item in output_dir.rglob("*"):
                print(f"  {item.relative_to(output_dir)}")

        generated_proto = output_dir / "models" / "server_models.proto"

        if not generated_proto.exists():
            raise FileNotFoundError(f"Generated file not found at {generated_proto}")

        print(f"Reading generated file: {generated_proto}")
        content = generated_proto.read_text(encoding="utf-8")

        # Replace syntax declaration with package declaration
        print("Replacing syntax declaration with package declaration...")
        content = content.replace(
            "package openapitools;",
            "package ansys.api.result_explorer.v0.server_models;",
        )

        # Replace all bool fields with optional bool (skip if already optional)
        print("Replacing bool fields with optional bool...")
        lines = content.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if " bool " in line and "optional bool" not in line:
                lines[i] = line.replace(" bool ", " optional bool ")
        content = "".join(lines)

        # Write to target location
        print(f"Writing to {target_file}...")
        target_file.write_text(content, encoding="utf-8")

        print("Successfully generated server_models.proto")


if __name__ == "__main__":
    main()
