from django.http import HttpResponseRedirect

def render_misma_vista(request):
    referer = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer)