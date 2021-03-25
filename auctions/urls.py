from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing",views.create_listing,name="create_listing"),
    path("view/<int:list_id>",views.view_listing,name="view_list"),
    path("view/<int:list_id>/remove",views.remove_listing,name="remove_list"),
    path("view/<int:list_id>/comment",views.add_comment,name="add_comment"),
    path("view/<int:list_id>/watchlist",views.add_watchlist,name="add_watchlist"),
    path("view/<int:list_id>/remove_watchlist",views.remove_watchlist,name="remove_watchlist"),
    path("watchlist",views.view_watchlist,name="view_watchlist"),
    path("categories",views.view_category,name="view_categories")
]
