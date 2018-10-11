from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import CaseType, Case
from .forms import PhaseForm

def index(request):
    cases = Case.objects.all()

    paginator = Paginator(cases, 50)

    try:
        page = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    index = page.number - 1
    page_range = paginator.page_range[max(0, index - 5):(min(len(paginator.page_range), index + 5))]

    return render(request, 'index.html', {
        'page_range': page_range,
        'page': page
    })

def create_case(request, case_type_id):
    case_type = get_object_or_404(CaseType, pk=case_type_id)
    phase = case_type.phases.first()

    if request.method == 'POST':
        form = PhaseForm(phase, request.POST)
        if form.is_valid():
            case = Case(name='Nieuwe zaak', case_type=case_type, data=form.cleaned_data)
            case.save()
            redirect('overview')
        else:
            print(form.errors)
    else:
        form = PhaseForm(phase)

    return render(request, 'cases/create.html', {
        'case_type': case_type,
        'form': form
    })

def view_case(request, case_id):
    case = get_object_or_404(Case, pk=case_id)

    return render(request, 'cases/view.html', {
        'case': case
    })