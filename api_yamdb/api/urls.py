from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('', include('api.v1.urls')),
]
