from django.shortcuts import render
from polls.models import Question
# Create your views here.


def index(request):  # request 객체는 뷰 함수의 필수인자이다.
  # -pud_dated : pud_dated 컬럼의 역순으로 정렬
  # [:5] 5개의 최근 Question 객체를 가져와서 만듭니다.
    latest_question_list = Question.objects.all().order_by('-pud_date')[:5]
    context = {'latest_question_list': latest_question_list}
    # render 함수는 템플릿 파일에 content 변수를 적용하여 사용자에게 보여줄 최종 HTML 텍스트를 만들고,
    # 이를 담아서 HttpResponse 객체를 반환합니다.
    return render(request, 'polls/index.html', context)
