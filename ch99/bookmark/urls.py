from django.urls import path
from bookmark.views import BookmarkLV, BookmarkDV

# url 패턴의 이름을 정해 url 패턴 이름이 충돌되지 않도록 한다.
app_name = 'bookmark'
urlpatterns = [
    # 패턴 이름은 bookmark:index가 된다.
    path('', BookmarkLV.as_view(), name='index'),
    path('<int:pk>', BookmarkDV.as_view(), name='detail'),
]
