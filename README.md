# Анализ рейтинга брендов

Скрипт `report_generator.py` генерирует отчеты на основе CSV-файлов с данными о товарах. Поддерживается отчет average-rating, который вычисляет средний рейтинг брендов.

## Запуск
- Установите зависимости:

```bash
pip install -r requirements.txt
```

- Запустите скрипт:

```bash
python report_generator.py --files products1.csv products2.csv --report average-rating
```

## Добавление новых отчетов
- Создайте функцию в классе `ReportGenerator`, которая принимает данные и возвращает отсортированный список кортежей.

- Зарегистрируйте отчет в словаре reports:

```python
self.reports["new-report"] = self.new_report_function
```

## Тестирование
- Запустите тесты:

```bash
pytest test_report_generator.py
```

## Архитектура
- ReportGenerator: центральный класс для управления отчетами.

- Динамическое добавление отчетов: через метод add_report.

- Обработка ошибок: проверка существования отчетов и файлов.

### Результат для 1-ого списка
![1-й_продукт.PNG](screenshots/1-%D0%B9_%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82.PNG)
### Результат для 2-ого списка
![2-й_продукт.PNG](screenshots/2-%D0%B9_%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82.PNG)
### Результат объединённого списка
![2_продукта.PNG](screenshots/2_%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0.PNG)
### Покрытие
![Покрытие.png](screenshots/%D0%9F%D0%BE%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5.png)