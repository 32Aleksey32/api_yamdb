from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, SignupView, TokenView


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users_list')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token')
]
