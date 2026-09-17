import glob
import logging
import os
import shutil

from ansys.tools.protoc_helper import compile_proto_files

log = logging.getLogger()


def proto_compile(proto_path, output_dir):
    # compile_proto_files requires .proto files to be inside the output directory
    target_protos = glob.glob(os.path.join(proto_path, "**/*.proto"), recursive=True)
    copied = []
    for proto_file in target_protos:
        rel = os.path.relpath(proto_file, proto_path)
        dest = os.path.join(output_dir, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(proto_file, dest)
        copied.append(dest)

    try:
        compile_proto_files(output_dir)
    finally:
        for dest in copied:
            if os.path.exists(dest):
                os.remove(dest)

    log.info("Done compiling proto files.")


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
