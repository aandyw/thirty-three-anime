from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse


from .services import get_search


def index(request):
    ctx = {
        "aniresults": get_search('naruto')
    }
    return render(request, 'search.html', context=ctx)


def animes(request):
    title_param = request.GET.get('q')

    anime_results = []
    if title_param:
        anime_results = get_search(title_param)

    ctx = {
        "aniresults": anime_results
    }

    html = render_to_string(
        template_name='results.html',
        context=ctx
    )
    data = {"html_view": html}
    return JsonResponse(data, safe=False)


def fav(request):
    request.session['fav'] = 'test'
