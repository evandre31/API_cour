from django.contrib import admin
from django.urls import path, include
# from django.urls.conf import include

# rest_framework_simplejwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # api-auth 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # auth in interface restframeword E:\api\API_cour\readme\api_auth apres.jpg
    # pythonarabia
    path('pythonarabia/', include('tickets.urls',namespace='pythonarabia')), # tutorial tickets python arabia 
    # blog of very-academy
    path('blog/', include('blog.urls',namespace='blog')), # tutorial blog Very Academy 
    path('blog_api/', include('blog_api.urls',namespace='blog_api')), # tutorial blog Very Academy 
    # rest_framework_simplejwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
