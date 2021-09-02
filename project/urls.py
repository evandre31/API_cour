from django.contrib import admin
from django.urls import path, include
from django.urls.conf import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pythonarabia/', include('tickets.urls',namespace='pythonarabia')), # tutorial tickets python arabia 
    path('blog/', include('blog.urls',namespace='blog')), # tutorial blog Very Academy 
    path('blog_api/', include('blog_api.urls',namespace='blog_api')), # tutorial blog Very Academy 
    path('api-auth', include('rest_framework.urls')), # auth in interface restframeword E:\api\API_cour\readme\api_auth apres.jpg

]
