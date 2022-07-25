import django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from mysite.views import HomeView, UserCreateView, UserCreateDoneTV

# from bookmark.views import BookmarkLV, BookmarkDV

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', UserCreateView.as_view(), name='register'),
    path('accounts/register/done/',
         UserCreateDoneTV.as_view(), name='register_done'),
    path('', HomeView.as_view(), name='home'),
    # 처리를 bookmark url로 위임
    path('bookmark/', include('bookmark.urls')),
    path('blog/', include('blog.urls')),
    path('photo/', include('photo.urls')),
    # class-based views
    # path 함수는 route, view 2개의 필수 인자와 kwargs, name 2개의 선택 인자를 받습니다.
    # 여기서 정해준 name 인자값은 템플릿 파일에서 많이 사용됩니다.
    # MVT 원칙을 따르기 위해서 뷰로직을 URL에서 적용하지 않는다.
    # path('bookmark/', BookmarkLV.as_view(), name='index'),
    # path('bookmark/<int:pk>', BookmarkDV.as_view(), name='detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
