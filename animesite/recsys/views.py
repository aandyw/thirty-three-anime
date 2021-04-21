from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .services import get_search


def index(request):
    if request.method != 'GET':
        raise Http404('Only GETs are allowed')

    if 'favourite_anime' not in request.session:
        request.session['favourite_anime'] = [None] * 9

    ctx = {
        "aniresults": get_search("")
    }
    response = render(request, 'search.html', context=ctx)
    return response


def animes(request):
    if request.method != 'GET':
        raise Http404('Only GETs are allowed')

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


# select favourite anime
def select(request):
    if request.method != 'GET':
        raise Http404('Only GETs are allowed')

    title = request.GET.get('title', '')
    image_url = request.GET.get('image_url', '')

    # get dictionary and update key/value with new
    animes = request.session.get('favourite_anime')
    for i in range(len(animes)):
        if animes[i] is None:
            animes[i] = {'title': title, 'image_url': image_url}
            break

    request.session['favourite_anime'] = animes

    ctx = {
        "favourites": animes
    }

    html = render_to_string(
        template_name='matrix.html',
        context=ctx
    )
    data = {"html_view": html}
    return JsonResponse(data, safe=False)
