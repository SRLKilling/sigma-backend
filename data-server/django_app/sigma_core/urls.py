from django.conf.urls import url, include

from rest_framework import routers
router = routers.DefaultRouter()

from sigma_core.views.user import UserViewSet
from sigma_core.views.group import GroupViewSet
from sigma_core.views.group_member import GroupMemberViewSet
from sigma_core.views.group_field import GroupFieldViewSet
from sigma_core.views.group_field_value import GroupFieldValueViewSet
from sigma_core.views.group_invitation import GroupInvitationViewSet
from sigma_core.views.acknowledgment_invitation import AcknowledgmentInvitationViewSet
from sigma_core.views.shared_publication import SharedPublicationViewSet

router.register(r'group', GroupViewSet)
router.register(r'group-member', GroupMemberViewSet)
router.register(r'group-field', GroupFieldViewSet)
router.register(r'group-field-value', GroupFieldValueViewSet)
router.register(r'group-invitation', GroupInvitationViewSet)
router.register(r'user', UserViewSet)
router.register(r'acknowledge-invitation', AcknowledgmentInvitationViewSet)
router.register(r'publication', SharedPublicationViewSet)

from django.http.response import HttpResponse
from push_app.notify import notify
def testview(request):
    notify("test\n")
    return HttpResponse('Test send to clients')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^test', testview),
]
