from django.shortcuts import render
from django.views.generic import ListView, DetailView
from bookmark.models import Bookmark


class BookmarkLV(ListView):
  # ListView의 경우 모든 레코드를 가져와 구성하는 경우에는 테이블명만 지정해주면 된다.
  # object_list 와 템플릿 파일명은 디폴트로 알아서 지정해준다.
    model = Bookmark


class BookmarkDV(DetailView):
  # DetailView의 경우 PK로 조회해서 특정 객체를 가져오는 경우에는 테이블 명만 지정하면 됩니다.
  # object 와 템플릿 파일명은 디폴트로 알아서 지정해준다.
    model = Bookmark
