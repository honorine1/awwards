from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns=[
    url('^$',views.index,name = 'index'),
    url(r'^project_posts/', views.project_posts, name='project_posts'),
    url(r'^viewProject_details/', views.viewProject_details, name='viewProject_details'),
    url(r'^new_post/',views.new_post,name='new_post'),
    url(r'^profile/(\d+)',views.profile,name = 'profile'),
    url(r'^update_profile/',views.update_profile,name = 'update_profile'),
    url(r'^search/',views.search_project,name = 'search_project'),
    # url(r'^add_comment/(\d+)',views.add_comment,name = 'add_comment'),
    # url(r'^view_comment/',views.view_comments,name = 'view_comments'),
    url(r'^vote/(?P<id>\d+)',views.rating,name='rating'),
    url(r'^api/projects/$', views.ProjectsList.as_view(),name='projects_api'),
    url(r'^api/profile/$', views.ProfileList.as_view(),name='profile_api'),

   

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)