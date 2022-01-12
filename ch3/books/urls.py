from django.urls import path
from . import views

# app_name: URL 패턴의 이름이 충돌나는 것을 방지하기 위한 이름 공간
app_name = 'books'
urlpatterns = [
    path('', views.BooksModelView.as_view(), name='index'),
    path('book/', views.BookList.as_view(), name='book_list'),
    path('author/', views.AuthorList.as_view(), name='author_list'),
    path('publisher/', views.PublisherList.as_view(), name='publisher_list'),
    path('book/<int:pk>', views.BookDetail.as_view(), name='book_detail'),
    path('author/<int:pk>', views.AuthorDetail.as_view(), name='author_detail'),
    path('publisher/<int:pk>', views.PublisherDetail.as_view(),
         name='publisher_detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote')
]
