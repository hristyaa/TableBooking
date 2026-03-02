FROM python:3.13.3

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы Poetry
COPY pyproject.toml poetry.lock ./

# Отключаем создание виртуального окружения
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости с помощью Poetry
RUN poetry install --no-root

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Копируем остальные файлы проекта в контейнер
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
