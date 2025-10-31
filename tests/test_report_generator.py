import pytest
import tempfile
import os
import sys

# Добавляем корневую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from report_generator import ReportGenerator


@pytest.fixture
def sample_files():
    files = []
    data1 = [
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", "999", "4.9"],
        ["galaxy s23 ultra", "samsung", "1199", "4.8"],
    ]
    data2 = [
        ["name", "brand", "price", "rating"],
        ["poco x5 pro", "xiaomi", "299", "4.4"],
        ["iphone se", "apple", "429", "4.1"],
    ]

    for i, data in enumerate([data1, data2]):
        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w") as f:
            for row in data:
                f.write(",".join(row) + "\n")
        files.append(path)

    yield files

    # Очистка временных файлов
    for path in files:
        try:
            os.remove(path)
        except OSError:
            pass


def test_average_rating(sample_files):
    generator = ReportGenerator()
    result = generator.generate_report("average-rating", sample_files)

    # Преобразуем в словарь для независимой от порядка проверки
    result_dict = dict(result)
    expected = {"apple": 4.5, "samsung": 4.8, "xiaomi": 4.4}

    assert result_dict == expected
    # Проверяем сортировку (по убыванию рейтинга)
    assert result[0][1] == 4.8  # samsung должен быть первым
    assert result[1][1] == 4.5  # apple вторым
    assert result[2][1] == 4.4  # xiaomi третьим


def test_invalid_report(sample_files):
    generator = ReportGenerator()
    with pytest.raises(ValueError, match="Отчет invalid-report не найден"):
        generator.generate_report("invalid-report", sample_files)


def test_empty_files():
    generator = ReportGenerator()

    # Создаем временный файл с помощью mkstemp вместо NamedTemporaryFile
    fd, path = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "w") as f:
            f.write("name,brand,price,rating\n")
        result = generator.generate_report("average-rating", [path])
        assert result == []
    finally:
        # Всегда удаляем временный файл
        try:
            os.remove(path)
        except OSError:
            pass


def test_single_brand():
    generator = ReportGenerator()

    # Создаем временный файл с данными только одного бренда
    fd, path = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "w") as f:
            f.write("name,brand,price,rating\n")
            f.write("iphone 15,apple,999,4.9\n")
            f.write("iphone 14,apple,799,4.7\n")

        result = generator.generate_report("average-rating", [path])
        expected = [("apple", 4.8)]  # (4.9 + 4.7) / 2 = 4.8
        assert result == expected
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
