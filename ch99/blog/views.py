import imp
from multiprocessing import context
from operator import imod
from pydoc import describe
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from django.conf import settings
from django.db.models import Q

from blog.models import Post
from blog.forms import PostSearchForm


class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    # 별도로 지정하더라도 디폴트 컨텍스트 변수명인 'object_list'도 사용할 수 있다.
    context_object_name = 'posts'
    # 페이지 기능 사용
    paginate_by = 2


class PostDV(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        # 기존의 컨텍스트 변수들을 구하고 이를 context 변수에 할당합니다.
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        # 템플릿 변수에 페이지별 식별자로 사용할 유일값을 만들어 대입합니다.
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.slug}"
        return context


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


# FormView 제네릭 뷰는 get 요청인 경우 폼을 화면에 보여주고 사용자의 입력을 기다립니다.
# 사용자가 폼에 데이터를 입력한 후 제출하면 이는 POST 요청으로 접수되며 FromView 클래스는 데이터에 대한 유효성 검사를 합니다.
# 데이터가 유효하면 form_valid 함수를 실행한 후 적절한 url로 리다이렉트 시키는 기능을 갖고있습니다.
class SearchFormView(FormView):
    # 폼으로 사용될 클래스를 지정
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        # 유효성 검사를 통과하면 사용자가 입력한 데이터들은 cleaned_data 사전에 존재합니다.
        searchWord = form.cleaned_data['search_word']
        # Q 객체는 filter() 메소드의 매칭 조건을 다양하게 줄 수 있도록 합니다.
        # icontains 연산자는 대소문자를 구분하지 않고 단어가 포함되어 있는지 검사합니다.
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(
            description__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()

        # context를 사전 혀ㅑㅇ식으로 정의합니다.
        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        # render()는 템플릿 파일과 컨텍스트 변수를 처리해 최종적으로 HttpRespons 객체를 반환합니다.
        # from_valid()메소드는 보통 리다이렉트 처리를 위해 HttopResponseRedirect 객체를 반환합니다.
        # 여기서는 from_valid() 메소드를 재정의하여 render() 함수를 사용함으로써, HttpResponseRedirect가 아니라 HttpRespons 객체를 반환합니다.
        return render(self.request, self.template_name, context)
