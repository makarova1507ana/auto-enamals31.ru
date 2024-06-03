from django.db import models


class Brand(models.Model):
    """
    Модель бренда товара

    Атрибуты:
    - name - названия бренда
    - slug - URL
    """

    name = models.CharField(max_length=150, unique=True, verbose_name="Название бренда")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    class Meta:
        """
        Класс для отображения в админке 

         Атрибуты:
        - db_table - названия таблицы
        - verbose_name - название в ед. числе
        - verbose_name_plural - название в множественном числе
        """
        db_table = 'brand'
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class SubSubcategory(models.Model):
    """
    Модель подкатегории

    Атрибуты:
    - name - название подкатегории
    - slug - URL
    """
    subcategory = models.ForeignKey('Subcategory', on_delete=models.PROTECT, verbose_name="Категория")
    name = models.CharField(max_length=150, unique=True, blank=True, null=True, verbose_name="Название подкатегории")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    image = models.ImageField(upload_to='subsubcategory-images', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        """
        Класс для отображения в админке

         Атрибуты:
        - db_table - названия таблицы
        - verbose_name - название в ед. числе
        - verbose_name_plural - название в множественном числе
        """
        db_table = 'subsubcategory'
        verbose_name = "ПодПодкатегория"
        verbose_name_plural = "ПодПодкатегории"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Модель подкатегории

    Атрибуты:
    - name - название подкатегории
    - slug - URL
    """
    category = models.ForeignKey('Categories', on_delete=models.PROTECT, verbose_name="Категория")
    name = models.CharField(max_length=150, unique=True, blank=True, null=True, verbose_name="Название подкатегории")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    image = models.ImageField(upload_to='subcategory-images', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        """
        Класс для отображения в админке 

         Атрибуты:
        - db_table - названия таблицы
        - verbose_name - название в ед. числе
        - verbose_name_plural - название в множественном числе
        """
        db_table = 'subcategory'
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name


class Categories(models.Model):
    """
    Модель цвета краски

    Атрибуты:
    - name - название цвета
    - slug - URL
    """

    name = models.CharField(max_length=150, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    image = models.ImageField(upload_to='categories-images', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        """
        Класс для отображения в админке 

         Атрибуты:
        - db_table - названия таблицы
        - verbose_name - название в ед. числе
        - verbose_name_plural - название в множественном числе
        """
        db_table = 'category'
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Цвет")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    class Meta:
        """
        Класс для отображения в админке 
         Атрибуты:
        - db_table - название таблицы
        - verbose_name - название в ед. числе
        - verbose_name_plural - название в множественном числе
        """
        db_table = 'color'
        verbose_name = "Цвет"
        verbose_name_plural = "Цвет"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель товара

    Атрибуты:
    - name - название товара
    - slug - URL
    - description - описание товара
    - price - цена товара
    - discount - скидка на товар 
    - quantity - количество
    - category - категория
    - color - цвет
    - brand - бренд
    """
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.IntegerField(default=0, verbose_name="Цена")
    discount = models.DecimalField(default=0.0, max_digits=7, decimal_places=2, verbose_name="Скидка в %")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    category = models.ForeignKey('Categories', on_delete=models.PROTECT, verbose_name="Категория")
    color = models.ForeignKey('Color', on_delete=models.PROTECT, verbose_name="Цвет", blank=True, null=True)
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, verbose_name="Бренд", blank=True, null=True)
    subcategory = models.ForeignKey('Subcategory', on_delete=models.PROTECT, verbose_name="Подкатегория", blank=True,
                                    null=True)
    subsubcategory = models.ForeignKey('SubSubcategory', on_delete=models.PROTECT, verbose_name="ПодПодкатегория",
                                       blank=True, null=True)
    image = models.ImageField(upload_to='goods-images', blank=True, null=True, verbose_name="Изображение")
    url_image = models.CharField(max_length=200, blank=True, null=True, verbose_name="URL Изображение")

    class Meta:
        """
        Класс для отображения в админке 

         Атрибуты:
        - db_table - название таблицы
        - verbose_name - название в ед. числе
        - verbose_name_plural - название в множественном числе
        - ordering - отображения товаров по критерию 
        """
        db_table = 'product'
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ('-quantity',)

    def __str__(self):
        """
        Функция для отобрадения в админке
        """
        return f'{self.name} Колисчество - {self.quantity} Скидка - {self.discount}'

    def display_id(self):
        """
        Отображения id 
        """
        return f'{self.id:05}'

    def sell_price(self):
        """
        Функция для отображения цены 
        """
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 0)

        return self.price