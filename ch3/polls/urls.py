from django.urls import path
from . import views

# app_name: URL 패턴의 이름이 충돌나는 것을 방지하기 위한 이름 공간
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
