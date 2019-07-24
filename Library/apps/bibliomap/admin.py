from django.contrib import admin

from . import models

# Register your models here.
class AdminSite(admin.AdminSite):
    admin.AdminSite.site_header = "Administracion BiblioMap"
    admin.AdminSite.site_title = admin.AdminSite.site_header


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'state']
    list_display_link = ['name']
    search_fields = ['name']
    list_filter = ['state']


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']
    list_display_link = ['name']
    search_fields = ['name']
    list_filter = ['state']


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'state']
    list_display_link = ['name']
    search_fields = ['name', 'surname']
    list_filter = ['state']
    ordering = ['name', 'surname']


@admin.register(models.Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country']
    list_display_link = ['name']
    search_fields = ['name', 'city', 'country']
    list_filter = ['state']
    ordering = ['name', 'city', 'country']
    ordering = ['name']


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'editorial', 'isbn', 'state']
    list_display_link = ['title']
    filter_horizontal = ['authors']
    search_fields = ['title', 'editorial', 'isbn']
    list_filter = ['state']
    ordering = ['title', 'editorial']


@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'date', 'returnDate', 'deadline']
    list_display_link = ['user']
    search_fields = ['user__username', 'book__title', 'date', 'returnDate']
    list_filter = ['state']
    ordering = ['user', 'book', 'date']


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'date', 'state']
    list_display_link = ['user']
    search_fields = ['user__username', 'book', 'date']
    list_filter = ['state']
    ordering = ['user', 'book', 'date']


@admin.register(models.Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['daysForHouse', 'daysForClass']
    list_display_link = ['daysForHouse']