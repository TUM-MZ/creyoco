# Create your views here.
from django.http import HttpResponse, HttpResponseForbidden
import os
from django.contrib.auth.decorators import login_required
from django.conf import settings
from sendfile import sendfile


@login_required
def serve_media(request, path):
    """Checks if path is in user's media folder
    and serves it per XAccelRedirec    t
    """
    user_media_path = request.user.profile.media_path
    requested_path = os.path.abspath(os.path.join(settings.MEDIA_ROOT, path))
    if (
        request.user.is_staff
        or requested_path.startswith(user_media_path)
        or requested_path.startswith(os.path.join(
            settings.MEDIA_ROOT, settings.WIKI_CACHE_DIR)
        )
    ):
        return sendfile(request, requested_path)
    else:
        return HttpResponseForbidden("Can't access the file")
