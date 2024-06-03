from rest_framework import routers
from app.views import *

router = routers.DefaultRouter()
router.register('login', UserLoginView)
router.register('teachers', TeacherViewSet)
router.register('students', StudentViewSet)
router.register('subjects', SubjectViewSet)
router.register('class', Class_nameViewSet)
router.register('lessons', LessonViewSet)
router.register('parents', ParentViewSet)
router.register('marks', MarkViewSet)
urlpatterns = router.urls

