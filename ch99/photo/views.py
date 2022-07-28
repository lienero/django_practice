import imp
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from photo.models import Album, Photo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin
# 폼셋이란 동일한 폼 여러 개로 구성된 폼을 말합니다.
# 인라인 폼셋이란 메인 폼에 딸려 있는 폼셋으로, 테이블 간의 관계가 1:N인 경우 N테이블의 레코드 여러 개를 한 꺼번에 입력받기 위한 폼
from photo.forms import PhotoInlineFormSet


class AlbumLV(ListView):
    model = Album


class AlbumDV(DetailView):
    model = Album


class PhotoDV(DetailView):
    model = Photo


# Photo CUD
class PhotoCV(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ('album', 'title', 'image', 'description')
    success_url = reverse_lazy('photo:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PhotoChangeLV(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_change_list.html'

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)


class PhotoUV(OwnerOnlyMixin, UpdateView):
    model = Photo
    fields = ('album', 'title', 'image', 'description')
    success_url = reverse_lazy('photo:index')


class PhotoDelV(OwnerOnlyMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('photo:index')


# Album CUD
class AlbumChangeLV(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'photo/album_change_list.html'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)


class AlbumDelV(OwnerOnlyMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('photo:index')


# 인라인 폼 사용하는 뷰
class AlbumPhotoCV(LoginRequiredMixin, CreateView):
    model = Album
    fields = ('name', 'description')
    success_url = reverse_lazy('photo:index')

    # 디폴트 컨텍스트 변수 이외에 추가적인 컨텍스트 변수를 정의하기 위해 get_context_data() 메소드를 오버라이딩 정의합니다.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # POST 요청인 경우 formset 컨텍스트 변수를 self.request.POST, self.request.FILES 파라미터를 사용해 지정합니다.
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(
                self.request.POST, self.request.FILES)
        # GET 요청인 경우, formset 컨텍스트 변수에 빈 폼셋을 지정
        else:
            context['formset'] = PhotoInlineFormSet()
        # 컨텍스트 변수 사전을 반환한다.
        return context

    # 폼에 입력된 내용에 대해 유효성 검사를 수행해 에러가 없는 경우 form_valid() 메소드를 호출합니다.
    def form_valid(self, form):
        form.instance.owner = self.request.user
        # get_context_data() 메소드를 호출해 fromset 객체를 구한다.
        # 이 시점에서 fromset 데이터는 유효성 검사 전이고 form 데이터는 유효성 검사를 통과한 데이터입니다.
        context = self.get_context_data()
        formset = context['formset']
        for photoform in formset:
            photoform.instance.owner = self.request.user
        # 폼셋의 메인 객체를 방금 테이블에 저장한 객체로 지정합니다.
        if formset.is_valid():
            # form.save()를 호출해 폼의 데이터를 테이블에 저장합니다. 즉 앨범 레코드를 하나 생성한 것입니다.
            self.object = form.save()
            # 폼셋의 메인 객체를 방금 테이블에 저장한 객체로 지정합니다.
            formset.instance = self.object
            # 폼셋 데이터를 테이블에 저장합니다. 즉, 앞에서 생성한 앨범 레코드에 1:N 관계로 연결된 여러 개의 사진 레코드를 테이블에 저장합니다.
            formset.save()
            # 마지막으로 앨범 리스트 페이지로 리다이렉트 됩니다.
            return redirect(self.get_success_url())
        else:
            # 폼셋의 데이터가 유효하지 않으면, 다시 메인 폼 및 인라인 폼셋을 출력합니다.
            # 이 때의 폼과 폼셋에는 직전에 사용자가 입력한 데이터를 다시 보여줍니다.
            # render_to_response는 제네릭 뷰에서 제공하는 함수로서, 템플릿을 자동적으로 기본 템플릿 엔진을 이용해서 html로 변환해주는 함수입니다.
            return self.render_to_response(self.get_context_data(form=form))


class AlbumPhotoUV(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ('name', 'description')
    success_url = reverse_lazy('photo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(
                self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = PhotoInlineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
