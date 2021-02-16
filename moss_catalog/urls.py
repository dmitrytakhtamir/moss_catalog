"""moss_catalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from moss import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('taxons/', include('moss.urls', namespace='taxons')),
    path('definer/', include('definer.urls', namespace='definer')),
    
    path('', views.home, name='home'),
    path('profile/', views.profile_page, name='profile_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('search/', views.search, name='search'),
    path('base_settings/', views.base_settings, name='base_settings'),
    path('map/', views.to_map, name='to_map'),
    path('add_point/', views.add_point, name='add_point'),
    path('point_page/<int:point_id>/', views.point_page, name='point_page'),
    path('points_list/', views.points_list, name='points_list'),

    path('base/', views.base, name='base'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()