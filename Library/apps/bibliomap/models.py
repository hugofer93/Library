from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45, blank=True, null=True)
    state = models.BooleanField(default=True, verbose_name='available')

    state.boolean = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bibliomap:categoryDetail', kwargs = {'id': self.id})

    class Meta:
        ordering = ['name']


class Section(models.Model):
    name = models.CharField(max_length=45)
    location = models.ImageField(upload_to='location')
    state = models.BooleanField(default=True, verbose_name='available')

    state.boolean = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bibliomap:sectionDetail', kwargs = {'id': self.id})

    class Meta:
        ordering = ['name']


class Editorial(models.Model):
    name = models.CharField(max_length=45)
    city = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=45, blank=True, null=True)
    state = models.BooleanField(default=True, verbose_name='available')

    state.boolean = True

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'city', 'country']


class Author(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    birthDate = models.DateField(blank=True, null=True)
    state = models.BooleanField(default=True, verbose_name='available')

    state.boolean = True

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)

    class Meta:
        ordering = ['name', 'surname', 'birthDate']

# FALTA PROBAR
class Book(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=45)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=45, verbose_name='ISBN', blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    authors = models.ManyToManyField(Author)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    loans = models.ManyToManyField(
        User,
        verbose_name='Loans',
        through='Loan',
        through_fields=('book', 'user'),
        related_name='bookLoans'
    )
    reservations = models.ManyToManyField(
        User,
        verbose_name='Reservations',
        through='Reservation',
        through_fields=('book', 'user'),
        related_name='bookReservations',
    )
    coverPage = models.ImageField(upload_to='coverPage')
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    state = models.BooleanField(default=True, verbose_name='available')

    state.boolean = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bibliomap:bookDetail', kwargs = {'id': self.id})

    def available(self):
        if self.state == False:
            return False

        try:
            loans = self.loan_set.all().filter(state=True).count()
        except Exception:
            loans = 0

        try:
            reservations = self.reservation_set.all().filter(state=True).count()
        except Exception:
            reservations = 0

        try:
            total = loans + reservations
            if self.amount > total:
                return True
            else:
                return False
        except Exception:
            return False

    class Meta:
        ordering = ['title', 'editorial', 'year']


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    returnDate = models.DateField(verbose_name='Return Date', blank=True, null=True)
    deadline = models.DateField(verbose_name='Deadline')
    state = models.BooleanField(default=True, verbose_name='available')

    state.boolean = True

    def __str__(self):
        return '{} {}'.format(self.user.username, self.book.title)

    class Meta:
        ordering = ['date', 'user', 'book']


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    state = models.BooleanField(default=True, verbose_name='active')

    state.boolean = True

    def __str__(self):
        return '{} {}'.format(self.user.username, self.book.title)

    def get_absolute_url(self):
        return reverse('bibliomap:reservationDetail', kwargs = {'id': self.id})

    class Meta:
        ordering = ['date', 'user', 'book']


class Parameter(models.Model):
    daysForHouse = models.CharField(max_length=2, validators=[RegexValidator(r'^\d{1,2}$')])
    daysForClass = models.CharField(max_length=2, validators=[RegexValidator(r'^\d{1,2}$')])
    
    def __str__(self):
        return 'Parameter'