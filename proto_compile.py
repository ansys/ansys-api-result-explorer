import glob
import logging
import os
import subprocess

log = logging.getLogger()


def proto_compile(proto_path, output_dir):
    target_protos = glob.glob(os.path.join(proto_path, "**/*.proto"), recursive=True)
    command = [
        f"python -m grpc_tools.protoc",
        f"--python_out={output_dir}",
        f"--grpc_python_out={output_dir}",
        f"--mypy_out={output_dir}",
        f"--mypy_grpc_out={output_dir}",
        f"--proto_path={proto_path}",
    ] + target_protos

    log.debug(f"Running: {' '.join(command)}")
    exit_code = subprocess.call(" ".join(command), shell=True)
    if exit_code != 0:
        raise RuntimeError(
            f"Proto file compilation failed, command '{' '.join(command)}'."
        )
    log.info("Done compiling proto file.")


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s | %(levelname)5s] %(message)s",
        level=logging.DEBUG,
    )

    cwd = os.getcwd()

    proto_path = os.path.abspath(os.path.join(cwd, "proto"))
    out_dir = os.path.join(cwd, "src", "ansys", "api", "result_explorer", "v0")
    # clear output directory
    if os.path.exists(out_dir):
        log.info(f"Clearing output directory: {out_dir}")
        for f in glob.glob(os.path.join(out_dir, "**/*.p*"), recursive=True):
            if not f.endswith("__init__.py"):
                log.debug(f"Removing {f}")
                os.remove(f)
    else:
        os.makedirs(out_dir)
    proto_compile(proto_path, out_dir)
