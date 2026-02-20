
from django.urls import path
from .views import PostList, DetailPost, PostSearch, PostCreate, PostUpdate, PostDelete,IndexView

urlpatterns = [
    path("", PostList.as_view(), name="news"),
    path("search/", PostSearch.as_view(), name="news_search"),
    path("<int:pk>/", DetailPost.as_view(), name="news_detail"),
    path("create/", PostCreate.as_view(),name="news_create"),
    path("<int:pk>/edit", PostUpdate.as_view(), name="news_update"),
    path("<int:pk>/delete", PostDelete.as_view(), name="news_delete"),
    path("articles/create/", PostCreate.as_view(),name="Articles_create"),
    path("articles/<int:pk>/edit", PostUpdate.as_view(), name="Articles_update"),
    path("articles/<int:pk>/delete", PostDelete.as_view(), name="Articles_delete"),
    path('news/index',IndexView.as_view(),name="Became_auth")

]


