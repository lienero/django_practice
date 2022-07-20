import imp
from operator import imod
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from blog.models import Post


class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    # 별도로 지정하더라도 디폴트 컨텍스트 변수명인 'object_list'도 사용할 수 있다.
    context_object_name = 'posts'
    # 페이지 기능 사용
    paginate_by = 2


class PostDV(DetailView):
    model = Post


# ArchiveIndexView는 테이블로부터 객체 리스트를 가져와, 날짜 필드를 기준으로 최신 객체를 먼저 출력합니다.
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'


# 연도를 기준으로 객체 리스트를 가져와 그 객체들이 속한 월을 리스트로 출력한다.
class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    # 해당 연도에 해당하는 객체의 리스트를 만들어서 템플릿에 넘겨줌. 'object_list'도 사용할 수 있다.
    make_object_list = True


# 연월을 기준으로 객체 리스트를 가져와 그 리스트를 출력합니다.
class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'


# 연월일을 기준으로 객체 리스트를 가져와 리스트를 출력합니다.
class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'


class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'
