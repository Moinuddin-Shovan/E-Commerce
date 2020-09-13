from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="ShopAbout"),
    path("contact/", views.contact, name="ShopContact"),
    path("track/", views.track, name="Tracker"),
    path("search/", views.search, name="ShopSearch"),
    path("product/<int:prod_id>", views.product_view, name="Product"),
    path("checkout/", views.checkout, name="Checkout")

]
