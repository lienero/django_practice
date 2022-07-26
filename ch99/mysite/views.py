from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
# reverse_lazy(), reverse() 함수는 인자로 URL 패턴명을 받습니다.
# URL 패턴명을 인식하기 위해서는 url.py 모듈이 메모리에 로딩되어야 하나,
# 지금 작성하는 view.py 모듈이 로딩되고 처리되는 시점에 urls.py 모듈이 로딩되지 않을 수 있어 reverse_lazy() 함수를 임포트
from django.urls import reverse_lazy
# 뷰처리 진입단계에서 적절한 권한을 갖추었는지 판별할 때 사용하는 믹소인 클래스
from django.contrib.auth.mixins import AccessMixin


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


class OwnerOnlyMixin(AccessMixin):
    # 소유자가 아닌 경우 이 속성이 True면 403 인셉션 처리를 하고, False면 로그인 페이지로 리다이렉트 처리됩니다.
    raise_exception = True
    # 403 응답시 보여줄 메세지를 지정합니다. 403.html 템플릿 파일에서 사용합니다.
    permission_denied_message = "Owner only can update/delete the object"

    # 메인 메소드인 get() 처리 이전 단계의 dispatch() 메소드를 오버라이딩 합니다. 여기서 소유자 여부를 확인합니다.
    # AccessMixin 클래스를 상속받아 믹스인 클래스를 정의하는 경우에는 dispatch 메소드를 오버라이딩 하는 것이 일반적입니다.
    def dispatch(self, request, *args, **kwargs):
        # 대상이 되는 객체를 테이블로부터 가져옵니다.
        obj = self.get_object()
        if request.user != obj.owner:
            # handle_no_permission() 이 메소드에 의해 403 익셉션 처리, 클라이언트에게 403응답을 보냅니다.
            return self.handle_no_permission()
        # 같으면 상위 클래스의 dispatch() 메소드를 호출해서 정상 처리합니다.
        return super().dispath(request, *args, **kwargs)
