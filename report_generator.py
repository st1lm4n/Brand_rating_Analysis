import argparse
import csv
from collections import defaultdict

try:
    from tabulate import tabulate
except ImportError:
    print("Установите библиотеку tabulate: pip install tabulate")
    exit(1)


class ReportGenerator:
    def __init__(self):
        self.reports = {
            "average-rating": self.average_rating_report,
        }

    def read_files(self, files):
        data = []
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data.extend(list(reader))
        return data

    def average_rating_report(self, data):
        brands = defaultdict(list)
        for row in data:
            brands[row["brand"]].append(float(row["rating"]))

        report_data = []
        for brand, ratings in brands.items():
            avg_rating = sum(ratings) / len(ratings)
            report_data.append((brand, round(avg_rating, 2)))

        # Сортировка по убыванию рейтинга
        return sorted(report_data, key=lambda x: x[1], reverse=True)

    def generate_report(self, report_name, files):
        if report_name not in self.reports:
            raise ValueError(f"Отчет {report_name} не найден")

        data = self.read_files(files)
        report = self.reports[report_name](data)
        return report

    def add_report(self, name, function):
        self.reports[name] = function


def main():
    parser = argparse.ArgumentParser(description="Генератор отчетов из CSV-файлов")
    parser.add_argument("--files", nargs="+", required=True, help="Пути к CSV-файлам")
    parser.add_argument("--report", required=True, help="Название отчета")
    args = parser.parse_args()

    generator = ReportGenerator()

    try:
        result = generator.generate_report(args.report, args.files)
        print(tabulate(result, headers=["Бренд", "Средний рейтинг"], tablefmt="grid"))
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
