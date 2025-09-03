import argparse
import os
import runpy
import sys
import tempfile
from .transpile import translate_file, translate_yoruba


def run_python_code(code: str, filename: str = "<yorubapy>") -> int:
    globals_dict = {
        "__name__": "__main__",
        "__file__": filename,
        "__package__": None,
    }
    try:
        exec(compile(code, filename, "exec"), globals_dict)
        return 0
    except SystemExit as ex:
        # bubble up exit code from scripts using sys.exit
        return int(ex.code) if isinstance(ex.code, int) else 1
    except Exception as ex:  # noqa: BLE001 keep simple for CLI
        print(f"Runtime error: {ex}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="edepy",
        description="Run Yorùbá-flavored Python by transpiling to Python using tokenize.",
    )
    parser.add_argument("source", help="Path to .yoruba source file")
    parser.add_argument("--emit", "-e", action="store_true", help="Emit translated Python to stdout")
    parser.add_argument("--out", "-o", help="Write translated Python to this file path")
    parser.add_argument("--run", "-r", action="store_true", help="Execute after translation (default)")
    parser.add_argument("--no-run", dest="run_flag", action="store_false", help="Do not execute, only translate")
    parser.set_defaults(run_flag=True)

    args = parser.parse_args(argv)

    if not os.path.exists(args.source):
        print(f"Source not found: {args.source}", file=sys.stderr)
        return 2

    translated = translate_file(args.source)

    if args.emit:
        print(translated)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(translated)

    exit_code = 0
    if args.run_flag:
        # Execute from a temporary file to provide a reasonable __file__
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(translated)
            tmp_path = tmp.name
        try:
            exit_code = run_python_code(translated, filename=tmp_path)
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    return exit_code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

