import black
import fire

from isort import SortImports
from isort.main import from_path as get_isort_config_from_path
from isort.main import iter_source_code as iter_isort_source_code


def _sort_python_imports(check=False):
    skipped = []
    config = get_isort_config_from_path(".")
    file_names = iter_isort_source_code(["."], config, skipped)
    results = [SortImports(file_name, check=check) for file_name in file_names]
    if any(result.incorrectly_sorted for result in results):
        raise SystemExit(1)


def _format_python_code(check=False):
    try:
        black.main(args=(*(("--check",) if check else ()), "."))
    except SystemExit as e:
        if e.code == 0:
            pass
        else:
            raise


def format():
    _sort_python_imports()
    _format_python_code()


def main():
    try:
        fire.Fire(dict(format=format))
    except SystemExit:
        raise


if __name__ == "__main__":
    main()
