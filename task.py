from pathlib import Path
from typing import Collection
from stable_map import StableMap
from stable_map.handlers import LoggingHandler


class InvalidFileStructure(RuntimeError):
    """The structure of the file is invalid"""
    def __init__(self, file: Path) -> None:
        super().__init__(file)
        file.with_name(f"!_invalid_{file.stem}")


def read_file(
    file: Path,
    encoding: str = "utf-8",
    valid_values: Collection[str] = ("success", "info", "error"),
) -> tuple[Path, str]:
    content = file.read_text(encoding).strip()

    if len(content) == 0:
        raise EOFError('File "%s" is empty' % file)

    if content.lower() not in valid_values:
        raise InvalidFileStructure(file)

    return file, content


def main() -> None:
    user_input = input("Введите путь к директории с файлами: ")
    source_dir = Path(user_input).expanduser().resolve()

    ...


if __name__ == "__main__":
    main()
