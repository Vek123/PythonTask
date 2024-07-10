from pathlib import Path
from typing import Collection
from stable_map import StableMap
from stable_map.context import ErrorContext, ExceptionType, T
from stable_map.handler import ErrorHandler


class InvalidFileStructure(RuntimeError):
    """The structure of the file is invalid"""

    ...


class InvalidFileStructureHandler(ErrorHandler[Path, ExceptionType]):
    def handle(self, context: ErrorContext[Path, ExceptionType]) -> None:
        context.element.with_name(f"!_invalid_{context.element.stem}")


class EOFErrorHandler(ErrorHandler[Path, ExceptionType]):
    def handle(self, context: ErrorContext[Path, ExceptionType]) -> None:
        print(context.element.name)


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
    stable_map = StableMap(read_file, source_dir.iterdir(), [
        EOFErrorHandler(exceptions=[EOFError]),
        InvalidFileStructureHandler(exceptions=[InvalidFileStructure]),
    ])
    print(list(stable_map))


if __name__ == "__main__":
    main()
