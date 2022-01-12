from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from books.models import Book, Author, Publisher

# TemplateView

# BooksModelView는 books 애플리케이션의 첫 화면을 보여주기 위한 뷰다
# 특별한 로직이 없고 템플릿 파일만을 렌더링하는 경우에는 TemplateView 제네릭 뷰를 상속받아 사용하면 간단하다.


class BooksModelView(TemplateView):
  # TemplateView를 사용하는 경우에는 필수적으로 template_name 클래스 변수를 오버라읻딩해서 지정해줘야 합니다.
    template_name = 'books/index.html'

    # 템블릿 시스템으로 넘겨줄 컨텍스트 변수가 있는 경우에는 get_context_data() 메소드를 오버라이딩해서 정의해주면 됩니다.
    def get_context_data(self, **kwargs):
        # get_context_data() 메소드를 정의할 때는 반드시 첫 줄에 super() 메소드를 호출해야 한다.
        context = super(BooksModelView, self).get_context_data(**kwargs)
        # 첫 화면에 테이블 리스트를 보여주기 위해 컨텍스트 변수 model_list에 담아서 템플릿 시스템에 넘겨주고 있습니다.
        context['model_list'] = ['Book', 'Author', 'Publisher']
        return context

# ListView

# ListView를 상속받는 경우는 객체가 들어있는 리스트를 구성해서 이를 컨텍스트 변수로 템플릿 시스템에 넘겨주면 됩니다.
# 명시적으로 지정되지 않아도 장고에서 디폴트로 알아서 지정해주는 속성이 2가지 있습니다.
# 1. 컨텍스트 변수로 object_list를 사용하는 것, 2.모델명 소문자_list.html형식의 이름으로 지정하는 것.


class BookList(ListView):
    # Book 테이블로부터 모든 레코드를 가져와 object_list라는 컨텍스트 변수를 구성한다.
    # 템플릿 파일은 디폴트로 books/book_list.html파일이 됨
    model = Book


class AuthorList(ListView):
    model = Author


class PublisherList(ListView):
    model = Publisher

# DetailView

# DetailView를 상속받는 경우로 특정 객체 하나를 컨텍스트 변수에 담아서 템플릿 시스템에 넘겨주면 된다.
# 명시적으로 지정되지 않아도 장고에서 디폴트로 알아서 지정해주는 속성이 2가지 있습니다.
# 1. 컨텍스트 변수로 object를 사용하는 것, 2.모델명 소문자_detail.html형식의 이름으로 지정하는 것.


class BookDetail(DetailView):
    # 테이블에서 primary key로 조회해서 특정 객체를 가져오는 경우에는 테이블명, 즉 모델 클래스명만 지정해주면 된다.
    # 조회에 사용할 primary key 값은 URLconf에서 추출하여 뷰로 넘어온 파라미터를 사용합니다.
    model = Book


class AuthorDetail(DetailView):
    model = Author


class PublisherDetail(DetailView):
    model = Publisher
