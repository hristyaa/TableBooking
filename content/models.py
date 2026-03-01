from django.db import models

# Create your models here.


class HomePage(models.Model):
    """Модель для главной страницы сайта"""

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    subtitle = models.TextField(verbose_name="Подзаголовок", blank=True)

    hall_title = models.CharField(
        verbose_name="Заголовок зала", max_length=200, blank=True
    )
    hall_description = models.TextField(verbose_name="Описание зала", blank=True)
    hall_image = models.ImageField(
        verbose_name="Фото зала", upload_to="home/", blank=True
    )

    terrace_title = models.CharField(
        verbose_name="Заголовок террасы", max_length=200, blank=True
    )
    terrace_description = models.TextField(verbose_name="Описание террасы", blank=True)
    terrace_image = models.ImageField(
        verbose_name="Фото террасы", upload_to="home/", blank=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

    def __str__(self):
        return self.title


class Contacts(models.Model):
    """Модель для контактов и общей информации"""

    restaurant_name = models.CharField(
        max_length=200, verbose_name="Название ресторана"
    )
    phone = models.CharField(max_length=35, verbose_name="Телефон", blank=True)
    email = models.EmailField(unique=True, blank=True, verbose_name="Почта")
    address = models.CharField(
        max_length=200, verbose_name="Адрес ресторана", blank=True
    )
    work_hours = models.CharField(
        max_length=200, blank=True, verbose_name="Часы работы"
    )

    class Meta:
        verbose_name = "Контакты и общая информация"
        verbose_name_plural = "Контакты и общая информация"

    def __str__(self):
        return self.restaurant_name


class Services(models.Model):
    """Модель для предоставляемых рестораном услуг"""

    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(blank=True, verbose_name="Описание услуги")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Feedback(models.Model):
    """Модель для обратной связи"""

    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Почта")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"

    def __str__(self):
        return f"{self.name} - {self.created_at}"


class Values(models.Model):
    name = models.TextField(verbose_name="Ценность ресторана", blank=True)
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Ценность"
        verbose_name_plural = "Ценности"

    def __str__(self):
        return self.name


class AboutPage(models.Model):
    """Модель для контента 'О ресторане'"""

    history = models.TextField(verbose_name="История ресторана", blank=True)
    mission = models.TextField(verbose_name="Миссия ресторана", blank=True)
    values = models.ManyToManyField(
        Values, verbose_name="Ценности ресторана", blank=True
    )

    class Meta:
        verbose_name = "О ресторане"
        verbose_name_plural = "О ресторане"


class Staff(models.Model):
    """Модель для команды"""

    name = models.CharField(max_length=150, verbose_name="Имя сотрудника")
    role = models.CharField(max_length=150, verbose_name="Должность")
    description = models.TextField(blank=True, verbose_name="Характеристика")
    photo = models.ImageField(upload_to="team/", blank=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.name
