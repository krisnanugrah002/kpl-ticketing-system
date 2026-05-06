import os
import shutil
from pathlib import Path

# Daftar folder yang 100% akurat dengan PDF
directories = [
    "src/domain/aggregates",
    "src/domain/entities",
    "src/domain/value_objects",
    "src/domain/services",
    "src/domain/events",
    "src/domain/factories",
    "src/domain/repositories",
    "src/application/commands",
    "src/application/command_handlers",
    "src/application/queries",
    "src/application/query_handlers",
    "src/application/dtos",
    "src/application/interfaces",
    "src/infrastructure/database",
    "src/infrastructure/repositories",
    "src/infrastructure/services",
    "src/presentation/controllers",
    "src/presentation/schemas",
    "tests/domain"
]

# 1. Generate folder
for d in directories:
    Path(d).mkdir(parents=True, exist_ok=True)

# 2. Buat file __init__.py di seluruh direktori
for path in Path("src").rglob("*"):
    if path.is_dir():
        (path / "__init__.py").touch()

# 3. Buat file spesifik yang dibutuhkan
Path("src/domain/exceptions.py").touch()

print("✅ Struktur Clean Architecture telah direvisi sesuai dengan spesifikasi PDF!")