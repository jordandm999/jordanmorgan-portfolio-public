from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/', views.chatbot, name='chatbot'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)