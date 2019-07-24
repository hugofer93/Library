from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from . import views


app_name = 'bibliomap'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    
    path('login/', LoginView.as_view(template_name='bibliomap/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='bibliomap:home'), name='logout'),

    path('book/', views.Book.as_view(), name='book'),
    path('book/id/<int:id>', views.BookDetail.as_view(), name='bookDetail'),

    path('category/', views.Category.as_view(), name='category'),
    path('category/id/<int:id>', views.CategoryDetail.as_view(), name='categoryDetail'),

    path('section/', views.Section.as_view(), name='section'),
    path('section/id/<int:id>', views.SectionDetail.as_view(), name='sectionDetail'),    

    path('search/<str:search>', views.Search.as_view(), name='search'),
    
    path('book/id/<int:id>/loan/', views.LoanForm.as_view(), name='loanForm'),
    path('loan/', views.Loan.as_view(), name='loan'),

    path('book/id/<int:id>/reservation/', views.ReservationForm.as_view(), name='reservationForm'),
    path('reservation/id/<int:id>', views.ReservationDetail.as_view(), name='reservationDetail'),
    path('reservation/', views.Reservation.as_view(), name='reservation'),

    path('loan/return/', views.LoanReturn.as_view(), name='loanReturn'),
    path('success/', TemplateView.as_view(template_name='bibliomap/success.html'), name='success'),
]