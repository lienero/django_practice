from django.urls import path, re_path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostLV.as_view(), name='index'),
    # PostLV 뷰 클래스 blog 와 blog/post 2가지 요청을 모두 처리한다.
    path('post/', views.PostLV.as_view(), name='post_list'),
    # /blog/post/django-example/
    # 정규식을 지정하여 한글이 포함된 슬러그를 처리하도록 함.
    # 본래 슬러그 컨버터는 한글을 인식 못함
    re_path(r'^post/(?P<slug>[-\w]+)/$',
            views.PostDV.as_view(), name='post_detail'),
    path('archive/', views.PostAV.as_view(), name='post_archive'),
    path('archive/<int:year>/', views.PostYAV.as_view(), name='post_year_archive'),
    path('archive/<int:year>/<str:month>/',
         views.PostMAV.as_view(), name='post_month_archive'),
    path('archive/<int:year>/<str:month>/<int:day>',
         views.PostDAV.as_view(), name='post_day_archive'),
    path('archive/today/', views.PostTAV.as_view(), name='post_today_archive'),
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(),
         name='tagged_object_list'),
    path('search/', views.SearchFormView.as_view(), name='search'),
]
