from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from sigma_core.views.sigma_viewset import SigmaViewSet

from sigma_core.models.user import User
from sigma_core.serializers.user import UserSerializer

from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
import random

reset_mail = {
    'from_email': 'support@sigma.fr',
    'subject': 'Mot de passe Sigma',
    'message': u"""
Bonjour,
Ton mot de passe Sigma a été réinitialisé.
C'est maintenant "{password}".
Cordialement,
L'équipe Sigma.
"""
}


class UserViewSet(SigmaViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    #*********************************************************************************************#
    #**                                   Read actions                                          **#
    #*********************************************************************************************#

    def retrieve(self, request, pk=None):
        """
        Retrieve an User according to its id.
        """
        return self.basic_retrieve(request, pk)
        
        
    @list_route(methods=['get'])
    def me(self, request):
        """
        Retrieve the data of the current user.
        """
        return self.serialized_response(self)
    
    
    #*********************************************************************************************#
    #**                                  Write actions                                          **#
    #*********************************************************************************************#
        
        
    # def perform_create(self, serializer):
        # from sigma_core.models.cluster import Cluster
        # from sigma_core.models.group import Group
        # serializer.save()
        # # Create related GroupMember associations
        # # TODO: Looks like a hacky-way to do this.
        # # But how to do it properly ?
        # memberships = [GroupMember(group=Group(id=c), user=User(id=serializer.data['id']),) for c in serializer.data['clusters_ids']]
        # GroupMember.objects.bulk_create(memberships)
        

    # def update(self, request, pk=None):
        # """
        # Update the data of the specified user.
        # """
        # try:
            # user = User.objects.prefetch_related('clusters').get(pk=pk)
        # except User.DoesNotExist:
            # return Response(status=status.HTTP_404_NOT_FOUND)

        # # I can update my own profile, or another's profile if I'm a sigma/cluster admin
        # if not (request.user.is_sigma_admin() or int(pk) == request.user.id or request.user.is_admin_of_one_cluster(user.clusters.all())):
            # return Response(status=status.HTTP_403_FORBIDDEN)

        # # Names edition is allowed to sigma/clusters admins only
        # if (request.data['lastname'] != user.lastname or request.data['firstname'] != user.firstname) and not request.user.is_sigma_admin() and not request.user.is_admin_of_one_cluster(user.clusters.all()):
            # return Response('You cannot change your lastname or firstname', status=status.HTTP_400_BAD_REQUEST)

        # return super(UserViewSet, self).update(request, pk)

    # def destroy(self, request, pk=None):
        # if not request.user.is_sigma_admin() and int(pk) != request.user.id:
            # return Response(status=status.HTTP_403_FORBIDDEN)
        # super().destroy(request, pk)


    @list_route(methods=['put'])
    def change_password(self, request):
        """
        Allow current user to change his password.
        ---
        omit_serializer: true
        parameters_strategy:
            form: replace
        parameters:
            - name: old_password
              type: string
            - name: password
              type: string
        """
        # PASSWORD_MIN_LENGTH = 8

        # user = request.user
        # data = request.data
        # if not user.check_password(data['old_password']):
            # return Response("Wrong password", status=status.HTTP_403_FORBIDDEN)
        # if len(data['password']) < PASSWORD_MIN_LENGTH:
            # return Response("'password' must be at least %d characters long" % PASSWORD_MIN_LENGTH, status=status.HTTP_400_BAD_REQUEST)

        # user.set_password(data['password'])
        # user.save()
        return Response('Password successfully changed', status=status.HTTP_200_OK)

        
    #Dangerous to send a password in clear...
    @list_route(methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        """
        Reset current user's password and send him an email with the new one.
        ---
        omit_serializer: true
        parameters_strategy:
            form: replace
        parameters:
            - name: email
              type: string
        """
        # email = request.data.get('email')
        # if email == '':
            # return Response("'email' field cannot be empty", status=status.HTTP_400_BAD_REQUEST)

        # try:
            # user = User.objects.get(email=email)
        # except User.DoesNotExist:
            # return Response('No user found with this email', status=status.HTTP_404_NOT_FOUND)

        # password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(10))

        # mail = reset_mail.copy()
        # mail['recipient_list'] = [user.email]
        # mail['message'] = mail['message'].format(email=user.email, password=password, name=user.get_full_name())
        # send_mail(**mail)

        # user.set_password(password)
        # user.save()

        return Response('Password reset', status=status.HTTP_200_OK)
