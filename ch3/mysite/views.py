from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    # 프로젝트 관련된 뷰이므로 mysite에서 코딩한다
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 프로젝트 하위의 애플리케이션 리스트를 보여주기 위해 컨테스트 변수 app_list에 담아서 템플릿 시스템에 건네줌
        context['app_list'] = ['polls', 'books']
        return context
