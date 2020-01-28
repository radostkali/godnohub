from django.contrib import admin
from django.urls import path, include, re_path
from collection.views import *
from django.views.generic import TemplateView
from accounts.views import *
from rest_framework.routers import Route, SimpleRouter


class AjaxRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
    ]


ajax_router = AjaxRouter()
ajax_router.register(r'cards/', CardsApi)
ajax_router.register(r'news/', NewsApi)
ajax_router.register(r'later/', LaterApi)
ajax_router.register(r'filters/', FiltersApi)

api_root = 'api/v1/'

urlpatterns = [

    path('', TemplateView.as_view(template_name="index.html")),

    path('service-worker.js', ServiceWorkerView.as_view(), name='service_worker'),
    path('admin.panel', admin.site.urls),

    # auth
    path(r'%sauth/info/' % api_root, get_info),
    path(r'%sauth/create_account/' % api_root, create_account),
    path(r'%sauth/login/' % api_root, login_account),
    path(r'%sauth/logout/' % api_root, logout_account),

    # card contoll
    path(r'%scard/create/' % api_root, create_card),
    path(r'%scard/delete/' % api_root, delete_card),
    path(r'%scard/get_images/' % api_root, get_images),
    path(r'%sgroup_edit/' % api_root, group_edit),

    # settings
    path(r'%saccount/load_avatar/' % api_root, load_avatar),
    path(r'%saccount/change_nickname/' % api_root, change_nickname),
    path(r'%saccount/change_page_id/' % api_root, change_page_id),

    # followers
    path(r'%sfollow/' % api_root, follow),

    # news
    path(r'%snews_info/' % api_root, news_info),

    # later
    path(r'%slater_filters/' % api_root, later_filters),

    # collection
    path(r'%sowner_info/' % api_root, owner_info),
    path(r'%s' % api_root, include(ajax_router.urls)),

    # main page
    path(r'%srandom_card/' % api_root, random_card),
    path(r'%srandom_collections/' % api_root, random_collections),

    path('<str:page>', TemplateView.as_view(template_name="index.html")),
    path('<str:page>/<str:group>', TemplateView.as_view(template_name="index.html")),

]

