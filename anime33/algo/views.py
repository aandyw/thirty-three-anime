from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect

from .services import perform_inference, get_animes

def recommend(request):
    if request.method != 'GET':
        raise Http404('Only GETs are allowed')

    animes = request.session.get('favourite_anime')
    lst = [int(anime.get('id')) for anime in animes]
    # print(lst)
    results = perform_inference(lst)

    print(results)

    anime_data = get_animes(results)

    ctx = {
        "recommendations": anime_data
    }

    html = render_to_string(
        template_name='recommend.html',
        context=ctx
    )
    data = {"html_view": html}
    return JsonResponse(data, safe=False)
