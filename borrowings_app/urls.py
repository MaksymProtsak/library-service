from django.urls import path, include

from rest_framework import routers

from borrowings_app.views import BorrowViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "borrowings"
