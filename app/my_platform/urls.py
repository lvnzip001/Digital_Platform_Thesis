from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('error/',views.error,name='error'),
    path('account_profile/',views.account_profile,name='account_profile'),
    path('about_us/',views.about_us, name = 'about_us'),
    path('services/',views.services, name = 'services'),
    path('menu_embed/',views.menu_embed, name='menu_embed'),
    path('menu_extraction/',views.menu_extraction, name='menu_extraction'),
    path('embed_ownership/',views.embed_ownership, name='embed_ownership'),
    path('embed_enforcement/',views.embed_enforcement, name='embed_enforcement'),
    path('embed_ownership_text/',views.embed_ownership_text, name='embed_ownership_text'),
    path('embed_ownership_sound/',views.embed_ownership_sound, name='embed_ownership_sound'),
    path('embed_ownership_image/',views.embed_ownership_image, name='embed_ownership_image'),
    path('embed_enforcement_text/',views.embed_enforcement_text, name='embed_enforcement_text'),
    path('embed_enforcement_sound/',views.embed_enforcement_sound, name='embed_enforcement_sound'),
    path('embed_enforcement_image/',views.embed_enforcement_image, name='embed_enforcement_image'),
    path('embedded_files/',views.embedded_files, name='embedded_files'),
    path('extract_text_info/',views.extract_text_info, name='extract_text_info'),
    path('extract_sound_info/',views.extract_sound_info, name='extract_sound_info'),
    path('extract_image_info/',views.extract_image_info, name='extract_image_info'),
    path('delete_file/<str:hash_url>',views.delete_file,name='delete_file')
    
]

