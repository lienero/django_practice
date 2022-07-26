from django.urls import path
# from bookmark.views import BookmarkLV, BookmarkDV
from bookmark import views

# url 패턴의 이름을 정해 url 패턴 이름이 충돌되지 않도록 한다.
app_name = 'bookmark'
urlpatterns = [
    # 패턴 이름은 bookmark:index가 된다.
    path('', views.BookmarkLV.as_view(), name='index'),
    path('<int:pk>', views.BookmarkDV.as_view(), name='detail'),
    path('add/', views.BookmarkCreateView.as_view(), name='add',),
    path('change/', views.BookmarkChangeLV.as_view(), name='change',),
    path('<int:pk>/update/', views.BookmarkUpdateView.as_view(), name='update',),
    path('<int:pk>/delete/', views.BookmarkDeleteView.as_view(), name='delete',)
]
