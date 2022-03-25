from django.urls import path, include

from .views import *

from .sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('account', AccountView.as_view(), name='account-view'),
    path('account/create/', AccountCreation.as_view(), name='account-creation'),
    path('create/', URLCreate.as_view(), name='url-create'),
    path('privacy/', PrivacyPolicy.as_view(), name='privacy'),
    path('tos/', TOS.as_view(), name='tos'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('robots.txt', Robots.as_view(), name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('<str:link_string>', get_dest, name='random'),
    path('<str:link_string>/', get_dest),  # Just allows the user to mess up and put a slash at the end
    path('<str:link_string>/info/', get_dest_info, name='random-info'),
    path('<str:link_string>/edit/', URLEdit.as_view(), name='url-edit'),
    path('<int:pk>/delete/', URLDelete.as_view(), name='url-delete')
]
