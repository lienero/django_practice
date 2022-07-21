import imp
from multiprocessing import context
from operator import imod
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
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


class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        # super().get_context_data()를 호출하여 상위클래스의 컨텍스트 변수, 즉 변겨엊ㄴ의 컨텍스트 변수를 추가합니다.
        context = super().get_context_data(**kwargs)
        # 추가할 컨텍스트 변수명은 tagname 이고, 그 값은 URL에서 tag 파라미터로 넘어온 값을 사용합니다.
        context['tagname'] = self.kwargs['tag']
        return context
