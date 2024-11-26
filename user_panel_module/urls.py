from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserPanelDashboardPage.as_view(), name="user_panel_dashboard"),
    path('edit-profile', views.EditUserProfile.as_view(), name="edit_profile_page"),
    path('change-pass', views.ChangePasswordPage.as_view(), name="change_password_page"),
    path('user-basket', views.user_basket, name="user_basket_page"),
    path('user-shopping', views.UserShopping.as_view(), name="user-shopping_page"),
    path('user-shopping_detail/<order_id>', views.user_shopping_detail, name="user-shopping_detail_page"),
    path('remove-order-detail', views.remove_order_detail, name="remove-order-detail-ajax"),
    path('change-order-detail', views.change_order_detail_count, name="change-order-detail-count-ajax")

]
