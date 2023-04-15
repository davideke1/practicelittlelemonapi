from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
#     path('menu-items/', views.menu, name='menu'),
# path('menu-items/<int:pk>', views.menu_singleitem),
path('category/<int:pk>',views.category_detail, name='category-detail'),
#     path('menu', views.menu),
# path('welcome',views.welcome),
#  path('food-items/', views.FoodItemView.as_view(), name='food-items'),
# path('food-items/<int:pk>', views.FoodItemSingleView.as_view(), name='food-itme-single'),
 path('menu-items', views.MenuItemViewset.as_view({'get':'list'})),
path('menu-items/<int:pk>', views.MenuItemViewset.as_view({'get':'retrieve'})),
    path('category', views.CategoryViews.as_view()),
    path('menu-items', views.Menuview.as_view()),
    path('secret', views.secret),
    path('auth-token-auth/', obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('throttle-check/', views.throttle_check),
path('throttle-check-auth/', views.throttle_check_auth),
    path('group/manager/user/', views.managers),
    path('ratings', views.RatingsView.as_view()),
    # path('bookss/', views.bookss, name='bookss'),
    # path('books/', views.BookList.as_view()),
    # path('book/<int:pk>', views.Book.as_view()),
    # path('menu-items/', views.MenuItemView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view())
]