import os
from urllib import parse
from io import BytesIO
import logging
from django.db.models import Q

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseRedirect, HttpResponsePermanentRedirect
from django.conf import settings
from django.views.decorators.cache import never_cache
from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from exeapp.models import User, idevice_store, Package
from exeapp.shortcuts import get_package_by_id_or_error
from django import forms
from django.core.urlresolvers import reverse
from exeapp.models.package import DublinCore, PackageOrder
from exeapp.views.export.exporter_factory import exporter_factory, exporter_map
from exeapp.views.authoring import authoring
from django.template.loader import render_to_string
from io import BytesIO
from collections import OrderedDict

import logging

log = logging.getLogger(__name__)

__all__ = ['package', 'authoring', 'properties']


class PackagePropertiesForm(forms.ModelForm):
    form_type = "properties_form"
    form_type_field = forms.CharField(initial=form_type,
                                      widget=forms.HiddenInput())

    class Meta:
        model = Package
        fields = ('title', 'author', 'email', 'description', 'logoImg')


class DublinCoreForm(forms.ModelForm):
    form_type = "dublincore_form"
    form_type_field = forms.CharField(initial=form_type,
                                      widget=forms.HiddenInput())

    class Meta:
        model = DublinCore
        exclude=()


def generate_package_main(request, package, current_node, **kwargs):
    '''Generates main page, can take additional keyword args to
    create forms'''

    log.info("%s accesses package of %s" % (request.user.username,
                                            package.user.username))
    idevices = list(idevice_store.values())
    exporter_type_title_map = OrderedDict(((export_type, exporter.title) \
                                    for export_type, exporter in
                                    list(exporter_map.items())))
    properties_form = kwargs.get(PackagePropertiesForm.form_type,
                                 PackagePropertiesForm(instance=package))
    dublincore_form = kwargs.get(DublinCoreForm.form_type,
                                 DublinCoreForm(instance=package.dublincore))
    user = User.objects.get(username=request.user.username)
    order_list = [(order.package, order.sort_order) for order in
                  PackageOrder.objects.filter(
                          Q(user=request.user)
                          | Q(package__collaborators__pk__contains=request.user.pk)
                  ).select_related("package")]
    package_list = [package for package, _ in sorted(order_list, key=lambda k: k[1])]
    print("#" * 100)
    print(package_list)
    return render_to_response('exe/mainpage.html', locals())


def change_properties(request, package, current_node):
    '''Parses post requests and applies changes to the package'''
    form_type = request.POST['form_type_field']
    if form_type == PackagePropertiesForm.form_type:
        form = PackagePropertiesForm(request.POST, instance=package)
    elif form_type == DublinCoreForm.form_type:
        form = DublinCoreForm(request.POST, instance=package.dublincore)
    if form.is_valid():
        form.save()
        if request.is_ajax():
            return HttpResponse("")
        else:
            return HttpResponseRedirect(reverse(
                'exeapp.views.package.package_main',
                args=[package.id, current_node.id]))
    else:
        if request.is_ajax():
            return HttpResponse(
                render_to_string("exe/{}.html".format(form_type),
                                 {form_type: form}))
        else:
            return generate_package_main(request, package, current_node,
                                         **{form.form_type: form})


@never_cache
@login_required
@get_package_by_id_or_error
def package_main(request, package, current_node, properties_form=None):
    '''Handle calls to package site. Renders exe/mainpage.html.'''
    if request.method == 'POST':
        return change_properties(request, package, current_node)
    elif request.META.get('HTTP_X_PJAX') or request.is_ajax():
        return render_to_response("exe/authoring.html", locals())
    else:
        return generate_package_main(request, package, current_node)


@login_required
@get_package_by_id_or_error
def package_root(request, package):
    current_node = package.root
    return HttpResponseRedirect(reverse(package_main, args=[package.id,
                                                            current_node.id]))


@login_required
@get_package_by_id_or_error
def export(request, package, export_format):

    file_obj = BytesIO()
    try:
        exporter = exporter_factory(export_format, package, file_obj)
    except KeyError:
        return HttpResponseBadRequest("Invalid export type")
    exporter.export()
    zip_file = file_obj.getvalue()
    file_obj.close()
    filename = package.zipname
    response = HttpResponse(content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=%s' \
                                      % filename
    response['Content-Length'] = len(zip_file)

    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        filename_header = 'filename=%s' % filename
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        filename_header = ''
    else:
        filename_header = 'filename*=UTF-8\'\'%s' % parse.quote(filename)
    response['Content-Disposition'] = 'attachment; ' + filename_header


    response.write(zip_file)
    return response


@login_required
@get_package_by_id_or_error
def preview(request, package, node):
    node_id = node.id
    exporter = exporter_factory("website", package, None)
    exporter.create_pages()
    for page in exporter.pages:
        if page.node.id == node_id:
            found_page = page
            break
    return HttpResponse(found_page.render(full_style_url=True))


@login_required
@get_package_by_id_or_error
def preview_root(request, package):
    current_node = package.root
    return HttpResponseRedirect(reverse(preview, args=[package.id,
                                                            current_node.id]))


@login_required
@get_package_by_id_or_error
def preview_static(request, package, node, path):
    media_path = request.user.profile.media_path
    if os.path.exists(os.path.join(media_path, path)):
        user_media_url = request.user.profile.media_url
        return HttpResponseRedirect(user_media_url + path)
    elif os.path.exists(os.path.join(settings.MEDIA_ROOT, settings.WIKI_CACHE_DIR, path)):
        url = settings.MEDIA_URL + settings.WIKI_CACHE_DIR + "/" + path
        return HttpResponseRedirect(url)
    else:
        node_style_url = settings.STATIC_URL + \
                         "css/styles/" + \
                         node.package.style + \
                         "/"
        return HttpResponseRedirect(node_style_url + path)

