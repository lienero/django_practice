from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from polls.models import Choice, Question
# Create your views here.


def index(request):  # request 객체는 뷰 함수의 필수인자이다.
    # -pud_dated : pud_dated 컬럼의 역순으로 정렬
    # [:5] 5개의 최근 Question 객체를 가져와서 만듭니다.
    latest_question_list = Question.objects.all().order_by('-pud_date')[:5]
    context = {'latest_question_list': latest_question_list}
    # render 함수는 템플릿 파일에 content 변수를 적용하여 사용자에게 보여줄 최종 HTML 텍스트를 만들고,
    # 이를 담아서 HttpResponse 객체를 반환합니다.
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # get_object_or_404의 첫번째 인자는 모델 클래스이고, 두번째 인자부터는 검색 조건을 여러개 사용할 수 있다.
    # Question 모델클래스로부터 pk=question_id 검색 조건에 맞는 객체를 조회하고 없으면 http404 익셉션을 발생시킨다.
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice']는 폼데이터 키가 'choice'에 해당하는 값인 choice.id를 스트링으로 리턴합니다.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # 폼의 POST 데이터에서 'choice'라는 키가 없으면 KetyError 익센셥을 발생시킵니다.
    # 또는 검색 조건에 맞는 객체가 없으면 Choice.DoseNotExist 익셉션이 발생합니다.
    except (KeyError, Choice.DoesNotExist):
        # 설문 투표 폼을 다시 보여준다.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST 데이터를 정상적으로 처리하였으면,
        # 항상 HttpResponseRedirect를 반환하여 리다이렉션처리함
        # reverse() 함수로 타겟 url을 만든다.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
