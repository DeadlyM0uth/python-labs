# Лабораторная работа № 8: Клиент-серверное приложение с Jinja2

## Описание проекта

Простое клиент-серверное приложение на Python для управления курсами валют. Приложение использует стандартный `HTTPServer` из стандартной библиотеки Python и реализует архитектуру **MVC** (Model-View-Controller).

### Основные функции:

- **Управление пользователями** — просмотр списка пользователей и их профилей
- **Отслеживание валют** — получение актуальных курсов от Центрального банка РФ
- **Подписка на валюты** — пользователи могут подписаться на интересующие валюты
- **Отображение динамики** — просмотр валют, на которые подписан пользователь

## Структура проекта

```
lab_work_8/
├── myapp/
│   ├── __init__.py
│   ├── myapp.py                 # Главное приложение (контроллер HTTPServer)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── author.py            # Модель Author
│   │   ├── app.py               # Модель App
│   │   ├── user.py              # Модель User
│   │   ├── currency.py          # Модель Currency
│   │   └── user_currency.py     # Модель UserCurrency (связь M2M)
│   ├── templates/
│   │   ├── index.html           # Главная страница
│   │   ├── users.html           # Список пользователей
│   │   ├── user_detail.html     # Профиль пользователя
│   │   ├── currencies.html      # Список валют
│   │   └── author.html          # Информация об авторе
│   ├── static/                  # Папка для CSS и изображений
│   └── utils/
│       ├── __init__.py
│       └── currencies_api.py    # Функции получения курсов валют
├── test_models.py               # Тесты моделей
├── test_currencies_api.py       # Тесты функции get_currencies
├── test_server.py               # Тесты контроллера
└── README.md                    # Этот файл
```

## Архитектура MVC

### Models (Модели)
Содержат описание предметной области с геттерами/сеттерами и валидацией:

- **Author** — информация об авторе
- **App** — метаинформация о приложении
- **User** — пользователь системы
- **Currency** — валюта (код, название, курс, номинал)
- **UserCurrency** — связь "много ко многим" между User и Currency

### Views (Представления)
HTML шаблоны на Jinja2 в папке `templates/`:

- `index.html` — главная страница с информацией о приложении
- `users.html` — список всех пользователей
- `user_detail.html` — профиль пользователя с его подписками
- `currencies.html` — текущие курсы валют
- `author.html` — информация об авторе

### Controller (Контроллер)
`myapp.py` — класс `CurrenciesServer`:
- Обработка HTTP запросов
- Маршрутизация запросов на обработчики
- Рендеринг шаблонов с данными

## Установка и запуск

### Требования

- Python 3.8+
- Jinja2

### Установка зависимостей

```bash
pip install jinja2
```

### Запуск приложения

```bash
cd lab_work_8
python run.py
```

Приложение будет запущено на `http://localhost:8000`

## Маршруты приложения

| Маршрут | Описание |
|---------|---------|
| `GET /` | Главная страница с информацией о приложении |
| `GET /users` | Список всех пользователей |
| `GET /user?id=<id>` | Профиль пользователя и его подписки |
| `GET /currencies` | Список текущих курсов валют |
| `GET /author` | Информация об авторе приложения |

## Описание моделей

### Author

```python
Author(name: str, group: str)
```

Параметры:
- `name` — имя автора (строка, не может быть пустой)
- `group` — учебная группа (строка, не может быть пустой)

### App

```python
App(name: str, version: str, author: Author)
```

Параметры:
- `name` — название приложения
- `version` — версия в формате `X.Y.Z`
- `author` — объект Author

### User

```python
User(user_id: int, name: str)
```

Параметры:
- `user_id` — уникальный ID (положительное целое число)
- `name` — имя пользователя (не может быть пустым)

### Currency

```python
Currency(
    currency_id: str,
    num_code: str,    # 3 цифры
    char_code: str,   # 3 буквы (ISO 4217)
    name: str,
    value: str,       # курс (может содержать запятую)
    nominal: str      # номинал
)
```

Параметры:
- `currency_id` — уникальный идентификатор (ID от ЦБ РФ, например "R01235" для USD)
- `num_code` — цифровой код (3 цифры, например "840" для USD)
- `char_code` — символьный код (3 буквы, например "USD")
- `name` — название валюты
- `value` — текущий курс (может содержать запятую как разделитель)
- `nominal` — номинал (за сколько единиц указан курс)

### UserCurrency

```python
UserCurrency(uc_id: int, user_id: int, currency_id: str)
```

Параметры:
- `uc_id` — уникальный ID записи
- `user_id` — внешний ключ к User (ID пользователя)
- `currency_id` — внешний ключ к Currency (ID валюты)

Реализует связь "много ко многим" — один пользователь может быть подписан на несколько валют.

## Использование API курсов валют

### Функция `get_currencies()`

Получает список валют от Центрального банка РФ:

```python
from myapp.utils import get_currencies

currencies = get_currencies()
# Возвращает список словарей с полями:
# {
#     'id': 'R01235',
#     'num_code': '840',
#     'char_code': 'USD',
#     'name': 'Доллар США',
#     'value': '75.5',
#     'nominal': '1'
# }
```

**Исключения:**
- `urllib.error.URLError` — ошибка подключения к API
- `ET.ParseError` — невалидный XML
- `ValueError` — отсутствуют валюты в ответе

### Функция `get_currencies_by_code()`

Получает валюту по символьному коду:

```python
from myapp.utils import get_currencies_by_code

# Получить USD (поиск без учета регистра)
usd = get_currencies_by_code('USD')

# Получить валюту из предопределённого списка
currencies = [...]
usd = get_currencies_by_code('USD', currencies)
```

## Тестирование

### Запуск всех тестов

```bash
cd lab_work_8

# Тесты моделей
python -m pytest test_models.py -v

# Тесты функции get_currencies
python -m pytest test_currencies_api.py -v

# Тесты контроллера
python -m pytest test_server.py -v

# Или через unittest
python -m unittest discover -p "test_*.py" -v
```

### Структура тестов

#### `test_models.py`

Тестирует все модели:
- Создание объектов
- Установку свойств (setters)
- Валидацию типов и значений
- Сравнение объектов (equality, hashing)

**Примеры тестов:**
```python
def test_author_creation(self):
    """Тест создания объекта Author."""
    author = Author(name="Иван Иванов", group="P3120")
    self.assertEqual(author.name, "Иван Иванов")

def test_author_name_invalid_type(self):
    """Тест установки имени с неверным типом."""
    author = Author(name="Иван", group="P3120")
    with self.assertRaises(TypeError):
        author.name = 123

def test_currency_value_with_comma(self):
    """Тест установки значения курса с запятой."""
    currency = Currency(...)
    currency.value = "75,5"
    self.assertEqual(currency.value, 75.5)
```

#### `test_currencies_api.py`

Тестирует функции получения курсов валют:
- Успешное получение данных
- Обработка ошибок сети
- Парсинг XML
- Поиск валюты по коду

**Примеры тестов:**
```python
@patch('urllib.request.urlopen')
def test_get_currencies_success(self, mock_urlopen):
    """Тест успешного получения курсов валют."""
    # Подготавливаем mock
    mock_response = MagicMock()
    mock_response.read.return_value = valid_xml.encode('utf-8')
    
    currencies = get_currencies()
    self.assertEqual(len(currencies), 2)
```

#### `test_server.py`

Тестирует контроллер и маршрутизацию:
- Инициализация приложения
- Хранение пользователей и валют
- Обработка параметров запроса

## Пример использования

### Запуск приложения

```bash
python -m myapp.myapp
```

### Запросы к приложению

```bash
# Главная страница
curl http://localhost:8000/

# Список пользователей
curl http://localhost:8000/users

# Профиль пользователя
curl http://localhost:8000/user?id=1

# Текущие курсы валют
curl http://localhost:8000/currencies

# Информация об авторе
curl http://localhost:8000/author
```