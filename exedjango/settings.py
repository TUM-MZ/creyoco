# Django settings for exedjango project.

import os
import sys


def _get_file_from_root(folder_name):
    '''Returns path to a file or folder in root of the project'''
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), folder_name).replace('\\',
                                                                                         '/')


DEBUG = True
REQUIRE_DEBUG = True
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    sys.dont_write_bytecode = True

import logging

logging.basicConfig(
    level=DEBUG and logging.DEBUG or logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)

ADMINS = (
    ('Dmytro Vorona', 'alendit@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _get_file_from_root('exedjango/sqlite.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = _get_file_from_root('exedjango/exeapp_media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g4c9r)uzvpig@%g5mc+6i$6o6tm-qh@^l=*8=#hw+jo_j_*fl_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    _get_file_from_root("templates"),
)

AUTH_PROFILE_MODULE = "exeapp.UserProfile"

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # handling of 403 exception
    'exedjango.base.middleware.Http403Middleware',
)

ROOT_URLCONF = 'exedjango.urls'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.flatpages',
    'django_autobahn',
    'require',
    'filebrowser',
    'registration',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_extensions',
    'jsonrpc',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'check_media',
    'strict_filebrowser',
    'exeapp',
    'gunicorn',
    'ckeditor',
)


ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda user: '/',
}

STATIC_ROOT = _get_file_from_root('exedjango/static')
STATICFILES_DIRS = (
    'require',
)
STATIC_URL = '/static/'
STYLE_DIR = "%s/css/styles/" % STATIC_ROOT
STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'

WIKI_CACHE_DIR = "wiki_cache_images"

TINYMCE_JS_URL = os.path.join(STATIC_URL, 'tiny_mce/tiny_mce.js')

TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'tiny_mce')

TINYMCE_COMPRESSOR = False

LINK_LIST = "authoring/link_list"

TINYMCE_DEFAULT_CONFIG = {
    "content_css": "/static/css/extra.css",
    "strict_loading_mode": True,
    "apply_source_formatting": True,
    "cleanup_on_startup": True,
    "entity_encoding": "raw",
    "gecko_spellcheck": True,
    "external_link_list_url": LINK_LIST,
    # "mode": "specific_textareas",
    # "editor_selector": "mceEditmainpageor",
    "plugins": "table,save,advhr,advimage,advlink,emotions,media, "
               "contextmenu,paste,directionality, heading",
    "theme": "advanced",
    "theme_advanced_layout_manager": "SimpleLayout",
    "theme_advanced_toolbar_location": "top",
    "theme_advanced_buttons1": "newdocument,separator,bold,italic,underline,"
                               "fontsizeselect,h1,h2,h3,h4,h5,h6,separator,"
                               "forecolor,backcolor,separator,sub,sup,"
                               "separator,justifyleft,justifycenter,"
                               "justifyright,justifyfull,separator,bullist,"
                               "numlist,outdent,indent",
    "theme_advanced_buttons2": "image,media,exemath,advhr,fontselect,"
                               "tablecontrols,separator,link,unlink,"
                               "separator, undo,redo,separator,charmap,code,"
                               "removeformat,separator,anchor",
    "theme_advanced_buttons3": "cut,copy,paste,pastetext,"
                               "pasteword",
    "advimage_image_browser_callback": "chooseImage_viaTinyMCE",
    "advimage_image2insert_browser_callback": "chooseImage_viaTinyMCE",
    "media_media_browser_callback": "chooseImage_viaTinyMCE",
    "media_media2insert_browser_callback": "chooseImage_viaTinyMCE",
    "advlink_file_browser_callback": "chooseImage_viaTinyMCE",
    "advlink_file2insert_browser_callback": "chooseImage_viaTinyMCE",
    "theme_advanced_statusbar_location": "bottom",
    "theme_advanced_resize_horizontal": False,
    "theme_advanced_resizing": True,
    "width": "100%",
    "remove_script_host": False,
    "convert_urls": False
}

# filebrowser settings
FILEBROWSER_PATH_FILEBROWSER_MEDIA = "%s/filebrowser/" % STATIC_ROOT
FILEBROWSER_URL_FILEBROWSER_MEDIA = "%sfilebrowser/" % STATIC_URL

# FILEBROWSER_URL_TINYMCE = "%stiny_mce/" % STATIC_URL
# FILEBROWSER_PATH_TINYMCE = "/tinymce/"

FILEBROWSER_SAVE_FULL_URL = True

FILEBROWSER_CONVERT_FILENAME = False
FILEBROWSER_STRICT_PIL = True

FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.svg'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.xlsx', '.csv', '.docx', '.ppt', '.pptx'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm', '.mp4', '.webm'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p']
}

SENDFILE_BACKEND = 'sendfile.backends.development'

REQUIRE_BASE_URL = "scripts/"

REQUIRE_BUILD_PROFILE = "app.build.js"

REQUIRE_STANDALONE_MODULES = {
    "main": {
        "out": "main-built.js",
        "build_profile": "app.build.js",
    }
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = os.path.join(STATIC_URL, "scripts/bower_components/jquery/dist/jquery.min.js")
CKEDITOR_CONFIGS = {
    'creyoco': {
        "filebrowserBrowseUrl": '/exeapp/filebrowser/browse/?pop=3',
        "removeDialogTabs": 'link:upload;image:Upload',
        "autoParagraph": False,
        "extraPlugins": 'autogrow,mathjax,video',
        "extraAllowedContent": 'video[*]{*};source[*]{*}',
        "mathJaxLib": '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML',
        "autoGrow_minHeight": 100,
        "autoGrow_maxHeight": 500,
        "width": "100%",
        "height": 100,
        "mathJaxLib": "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js",
        "toolbar": [
            {
                "name": "clipboard", "items": [ "Cut", "Copy", "Paste", "PasteText", "PasteFromWord", "-", "Undo", "Redo" ]
            },
            {
                "name": "paragraph",
                "items": [ "NumberedList", "BulletedList", "-", "Outdent", "Indent", "-", "Blockquote", "-", "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock" ] }
            ,
            {
                "name": "links", "items": [ "Link", "Unlink", "Anchor" ]
            },
            {
                "name": "insert", "items": [ "Image", "Video", "Table", "HorizontalRule", "Mathjax" ]
            },
            "/",
            {
                "name": "styles", "items": [ "Styles", "Format", "FontSize" ]
            },
            {
                "name": "basicstyles", "items": [ "Bold", "Italic", "Underline", "Strike", "Subscript", "Superscript", "-", "RemoveFormat" ]
            },
            {
                "name": "colors", "items": [ "TextColor", "BGColor" ]
            },
            {
                "name": "document", "items": [ "Source" ]
            },
            {
                "name": "tools", "items": [ "Maximize" ]
            }
        ],
    },
}
