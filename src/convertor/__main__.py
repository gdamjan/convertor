from .core import convert_file

import sys
import logging
import pathlib
import argparse

DESCRIPTION = """\
Convert Open Document Format (ODF) files from YUSCII to UTF-8.

For each file `FILE.odt' it will create a converted `FILE-NEW.odt' in
the same directory.
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "files",
        nargs="+",
        help="file(s) to convert",
        type=pathlib.Path,
        metavar="FILE",
    )
    args = parser.parse_args()
    errors = convert_files(args.files)
    if len(errors) > 0:
        sys.exit(2)


def convert_files(input_files: list[pathlib.Path]):
    """Oportunistically convert files, if a conversion fails, report it but continue with the rest of the files."""
    errors = []
    for p in input_files:
        try:
            output_filename = p.with_stem(f"{p.stem}-NEW")
            convert_file(p, output_filename)
        except Exception as exc:
            logger.warning(f"Can't convert `{p.absolute()}`", exc_info=True)
            errors.append((p, exc))
    return errors


if __name__ == "__main__":
    main()
