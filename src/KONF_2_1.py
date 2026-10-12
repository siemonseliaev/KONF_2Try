import sys
import os
import tomllib 
from pathlib import Path

CONFIG_FILE = "config.toml"


def load_config(file_path: str) -> dict:
    """Загружает и парсит TOML файл конфигурации."""

    current_dir = Path(__file__).resolve().parent
    config_path = current_dir / file_path
    
    if not config_path.exists():
        raise FileNotFoundError(f"Конфигурационный файл '{file_path}' не найден.")

    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Ошибка синтаксиса в TOML файле: {e}")


def validate_config(config: dict) -> None:
    """Проверяет наличие и типы всех обязательных параметров."""
    required_fields = {
        "package_name": str,
        "repo_url": str,
        "repo_mode": str,
        "package_version": str,
        "output_image": str,
        "max_depth": int
    }

    for field, expected_type in required_fields.items():
        if field not in config:
            raise KeyError(f"Отсутствует обязательный параметр: '{field}'")

        value = config[field]
        if not isinstance(value, expected_type) or (expected_type is int and isinstance(value, bool)):
            raise TypeError(
                f"Неверный тип для параметра '{field}'. Ожидался {expected_type.__name__}, "
                f"получен {type(value).__name__}"
            )

    if config["max_depth"] < 0:
        raise ValueError("Параметр 'max_depth' не может быть отрицательным.")

    valid_modes = ["online", "offline", "test"]
    if config["repo_mode"] not in valid_modes:
        raise ValueError(
            f"Некорректный режим 'repo_mode' ('{config['repo_mode']}'). "
            f"Допустимые значения: {valid_modes}"
        )


def main():
    print("=== Инициализация CLI-приложения ===")
    try:
        config = load_config(CONFIG_FILE)

        validate_config(config)

        print("\n[Успешно] Конфигурация успешно загружена:")
        for key, value in config.items():
            print(f"  - {key} = {value}")

    except (FileNotFoundError, ValueError, KeyError, TypeError) as e:
        print(f"\n[ОШИБКА КОНФИГУРАЦИИ]: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
