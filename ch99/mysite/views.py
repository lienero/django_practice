from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
# reverse_lazy(), reverse() 함수는 인자로 URL 패턴명을 받습니다.
# URL 패턴명을 인식하기 위해서는 url.py 모듈이 메모리에 로딩되어야 하나,
# 지금 작성하는 view.py 모듈이 로딩되고 처리되는 시점에 urls.py 모듈이 로딩되지 않을 수 있어 reverse_lazy() 함수를 임포트
from django.urls import reverse_lazy


# 홈페이지 뷰
class HomeView(TemplateView):
    template_name = 'home.html'


# 로그인 관련 뷰
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    # 폼에 임력된 내용에 에러가 없고 테이블 레코드 생성이 완료된 후에 이동할 URL을 지정합니다.
    success_url = reverse_lazy('register_done')


class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'
