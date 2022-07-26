from turtle import title
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from bookmark.models import Bookmark
# LoginRequiredMixin클래스는 @login_required() 데코레이터 기능을 클래스에 적용할 때 사용합니다.
# 사용자가 로그인 된 경우는 정상 처리를 하지만, 로그인이 안 된 사용자라면 로그인 페이지로 리다이렉트 시킵니다.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnltMixin


class BookmarkLV(ListView):
  # ListView의 경우 모든 레코드를 가져와 구성하는 경우에는 테이블명만 지정해주면 된다.
  # object_list 와 템플릿 파일명은 디폴트로 알아서 지정해준다.
    model = Bookmark


class BookmarkDV(DetailView):
  # DetailView의 경우 PK로 조회해서 특정 객체를 가져오는 경우에는 테이블 명만 지정하면 됩니다.
  # object 와 템플릿 파일명은 디폴트로 알아서 지정해준다.
    model = Bookmark


# LoginRequiredMixin 클래스를 상속받는 클래스는 로그인된 경우만 접근 가능합니다.
# 만일 로그인되지 않은 상태에서 BookmarkCreateView 뷰를 호출하면 로그인 페이지로 이동시킵니다.
# CreateView 클래스는 중요한 몇가지 클래스 속성만 정의하면 적절한 폼을 보여주고,
# 폼에 입력된 내용에서 에러여부를 체크한 후 에러가 없으면 입력된 내용으로 테이블에 레코드를 작성합니다.
class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = ['title', 'url']
    # form_vail() 메소드를 호출하여 테이블의 레코드를 수정하고 success_url로 지정된 url 로 리다이렉트 처리함
    success_url = reverse_lazy('bookmark:index')

    # 입력된 내용에 에러가 없으면 form_valid 메소드를 호출합니다.
    def form_valid(self, form):
        # 폼에 연결된 모델 객체의 owner 필드에는 현재 로그인 된 사용자의 User 객체를 할당합니다.
        form.instance.owner = self.request.user
        # 상위 클래스의 form_valid 메소드에 의해 form.save(), 즉 db에 반영되고 그후 success_url로 리다이렉트 됩니다.
        return super().form_valid(form)


# ListView 는 객체의 리스트만 지정하면 그 리스트를 화면에 출력해줍니다.
class BookmarkChangeLV(LoginRequiredMixin, ListView):
    template_name = 'bookmark/bookmark_change_list.html'

    # get_queryset() 메소드는 화면에 출력할 레코드 리스트를 반환합니다.
    # 즉 Bookmark 테이블의 레코드 중에서 owner 필드가 로그인한 사용자인 레코드만 필터링 해 그 리스트를 반환합니다.
    def get_queryset(self):
        return Bookmark.objects.filter(owner=self.request.user)


# OwnerOnltMixin 클래스에 의해 로그인 사용자가 대상 콘텐츠의 소유자인 경우에만 UpdateView 기능이 동작합니다.
# UpdateView 클래스를 상속받는 클래스는 중요한 몇 가지 클래스 속성만 정의하면,
# 테이블의 레코드들 중에 지정된 레코드 하나에 대한 내용을 폼으로 보여주고,
# 폼에서 수정 입력된 내용에서 에러 여부를 체크하며, 에러가 없으면 입력된 내용으로 테이블의 레코드를 수정합니다.
class BookmarkUpdateView(OwnerOnltMixin, UpdateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')


# DeleteView 클래스는 중요한 몇가지 클래스 속성만 정의하면 기존 레코드 중에서 지정된 레코드를 삭제할 것인지 확인하는 페이지를 보여줌
# 사용자가 확인 응답을 하면 해당 레코드를 삭제합니다.
class BookmarkDeleteView(OwnerOnltMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:index')
