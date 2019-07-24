from datetime import date

from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView
)

from . import models
from ..utils.days import addWorkDays

# Create your views here.
class Home(TemplateView):
    http_method_names = ['get']
    template_name = 'bibliomap/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['book'] = models.Book.objects.all().filter(state=True)
        except Exception:
            context['book'] = None

        try:
            context['category'] = models.Category.objects.all().filter(state=True)
        except Exception:
            context['category'] = None

        try:
            context['section'] = models.Section.objects.all().filter(state=True)
        except Exception:
            context['section'] = None

        if self.request.user.is_authenticated:
            try:
                reservation = models.Reservation.objects.all()
                reservation = reservation.filter(user=self.request.user)
                reservation = reservation.exclude(state=False)
                context['reservation'] = reservation
            except Exception:
                context['reservation'] = None

            try:
                loan = models.Loan.objects.all().filter(user=self.request.user)
                context['loanReturn'] = loan.filter(state=True)
                context['loan'] = loan.filter(state=False)
            except Exception:
                context['loanReturn'] = None
                context['loan'] = None
        
        return context


class Book(ListView):
    http_method_names = ['get']
    model = models.Book
    template_name = 'bibliomap/book.html'
    queryset = model.objects.all().filter(state=True)


class BookDetail(DetailView):
    http_method_names = ['get']
    model = models.Book
    template_name = 'bibliomap/bookDetail.html'
    pk_url_kwarg = 'id'


class Category(ListView):
    http_method_names = ['get']
    model = models.Category
    template_name = 'bibliomap/category.html'
    queryset = model.objects.all().filter(state=True)


class CategoryDetail(DetailView):
    http_method_names = ['get']
    model = models.Category
    template_name = 'bibliomap/categoryDetail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = context['object']
        categoria = categoria.book_set.all().filter(state=True)
        context['object_list'] = categoria
        return context


class Section(ListView):
    http_method_names = ['get']
    model = models.Section
    template_name = 'bibliomap/section.html'
    queryset = model.objects.all().filter(state=True)


class SectionDetail(DetailView):
    http_method_names = ['get']
    model = models.Section
    template_name = 'bibliomap/sectionDetail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = context['object']
        context['object_list'] = section.book_set.all().filter(state=True)
        return context


class Search(ListView):
    http_method_names = ['get']
    model = models.Book
    template_name = 'bibliomap/search.html'

    def get_queryset(self):
        queryset = self.model.objects.all()

        try:
            txtSearch = self.kwargs['search']
            if txtSearch:
                query = (
                    Q(title__icontains = txtSearch) |
                    Q(authors__name__icontains = txtSearch) |
                    Q(authors__surname__icontains = txtSearch)
                )
                queryset = queryset.filter(query)
                queryset = queryset.distinct()
                query = queryset.exclude(state=False)

        except Exception:
            pass

        return queryset


class LoanForm(LoginRequiredMixin, DetailView):
    http_method_names = ['get', 'post']
    model = models.Book
    template_name = 'bibliomap/loanForm.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['parameter'] = models.Parameter.objects.all()[0]
        except Exception:
            context['parameter'] = None
        
        return context

    def post(self, request, *args, **kwargs):
        try:
            book = self.model.objects.get(id=self.request.POST['bookId'])
        except Exception:
            book = None
        
        if book and self.request.user.is_authenticated:
            user = self.request.user
            loanDays = int(self.request.POST['loanDays'])
            dateLoan = date.today()
            deadline = addWorkDays(dateLoan, loanDays)
            loan = models.Loan(
                user=user,
                book=book,
                deadline=deadline,
                state=True
            )
            loan.save()
            return HttpResponseRedirect(reverse('bibliomap:success'))
        else:
            return HttpResponseRedirect(reverse('bibliomap:home'))


class Loan(LoginRequiredMixin, ListView):
    http_method_names = ['get']
    model = models.Loan
    template_name = 'bibliomap/loan.html'

    def get_queryset(self):
        queryset = self.model.objects.all()

        try:
            user = self.request.user
            queryset = queryset.filter(user=user).exclude(state=True)
        except Exception:
            queryset = None

        return queryset


class ReservationForm(LoginRequiredMixin, DetailView):
    http_method_names = ['get', 'post']
    model = models.Book
    template_name = 'bibliomap/reservationForm.html'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        try:
            bookId = self.request.POST['bookId']
            book = self.model.objects.get(id=bookId)
        except Exception:
            book = None

        if book.state and self.request.user.is_authenticated:
            user = self.request.user
            reservation = models.Reservation(
                user=user,
                book=book,
                state=True
            )
            reservation.save()
            return HttpResponseRedirect(reverse('bibliomap:success'))
        else:
            return HttpResponseRedirect(reverse('bibliomap:home'))


class ReservationDetail(LoginRequiredMixin, DetailView):
    http_method_names = ['get', 'post']
    model = models.Reservation
    template_name = 'bibliomap/reservationDetail.html'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        try:
            if str(self.kwargs['id']) == self.request.POST['reservationId']:
                reservationId = self.kwargs['id']
                reservation = self.model.objects.get(id=reservationId)
        except Exception:
            reservation = None

        if reservation and reservation.state and self.request.user.is_authenticated:
            reservation.state = False
            reservation.save()
            return HttpResponseRedirect(reverse('bibliomap:success'))
        else:
            return HttpResponseRedirect(reverse('bibliomap:home'))


class Reservation(LoginRequiredMixin, ListView):
    http_method_names = ['get']
    model = models.Reservation
    template_name = 'bibliomap/reservation.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user).exclude(state=False)
        return queryset


class LoanReturn(LoginRequiredMixin, ListView):
    http_method_names = ['get']
    model = models.Loan
    template_name = 'bibliomap/loanReturn.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user).exclude(state=False)
        return queryset