from django.urls import path, include
from .xml import urls as xml_urls
from .views import *


urlpatterns = [
    path('xml/', include(xml_urls)),
    path('root/', PageRootView.as_view()),
    path('page/<int:pk>/', PageDetailView.as_view()),
    path('page/<int:parent_id>/children/', PageChildrenListView.as_view()),
    path('page/<int:page>/tasks/', TaskListView.as_view()),
    path('task/<int:pk>/', TaskDetailView.as_view()),

]