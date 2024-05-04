from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail


from accounts.serializers import UserRegisterSerializer, LoginSerializer, AddUserSerializer, UserSerializer, \
    PasswordResetRequestSerializer, SetNewPasswordSerializer
#, LoginSerializer, \
   # PasswordResetRequestSerializer, SetNewPasswordSerializer, AddUserSerializer, UserSerializer
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework.generics import DestroyAPIView
from lmcs.models import Chercheur
from .permissions import IsAdminUser


from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
from rest_framework.generics import UpdateAPIView

from django.core.exceptions import ObjectDoesNotExist
from accounts.serializers import UserRegisterSerializer, LoginSerializer, AddUserSerializer, UserSerializer, \
    PasswordResetRequestSerializer, SetNewPasswordSerializer, LogoutUserSerializer
#, LoginSerializer, \
   # PasswordResetRequestSerializer, SetNewPasswordSerializer, AddUserSerializer, UserSerializer
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework.generics import DestroyAPIView
from lmcs.models import Chercheur
from .permissions import IsAdminUser
from .serializers import UserSerializer, ChercheurSerializer


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # Extract the user's role from the validated data
        role = serializer.validated_data.get('role')
        # Add the role to the response data
        response_data = serializer.data
        response_data['role'] = role
        return Response(response_data, status=status.HTTP_200_OK)
        
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Perform logout actions here
        # For example, clear user session
        request.session.clear()

        # Optionally, you can also perform other cleanup tasks

        return Response({"detail": "Déconnexion réussie.."}, status=status.HTTP_200_OK)



class AddUserView(CreateAPIView):
    serializer_class = AddUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = serializer.save()

        # Vérifier si l'utilisateur ajouté a le rôle "chercheur"
        if user.role == 'chercheur':
            try:
                # Rechercher le chercheur correspondant dans la table Chercheur
                chercheur = Chercheur.objects.get(email=user.email)
                user.chercheur_id = chercheur.id_chercheur  # Assigner l'ID du chercheur à chercheur_id dans le modèle User
            except ObjectDoesNotExist:
                pass

        # Vérifier si l'utilisateur ajouté a le rôle "admin"
        if user.role == 'admin':
            user.is_superuser = True

        user.save()

        # Envoyer un email à l'utilisateur ajouté
        self.send_email_to_user(user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_email_to_user(self, user):
        subject = 'Bienvenue à LMCS'
        full_name = f"{user.first_name} {user.last_name}"
        message = f'Bonjour {full_name},\n\nVous avez été ajouté à LMCSQUEST avec succès. Pour vous connecter, utilisez simplement cette adresse e-mail et utilisez les deux premières lettres de votre prénom comme mot de passe : LMCS_lesdeuxpremiereslettredevotreprenomenminiscule.'
        from_email = 'your_email@example.com'
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])

class ListUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Vous n'êtes pas authentifié."}, status=401)

        if request.user.is_superuser or request.user.role in ['admin']:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Vous n'avez pas la permission d'effectuer cette action."}, status=403)






class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Nous vous avons envoyé les codes pour réinitialiser votre mot de passe sous forme http://127.0.0.1:8000/api/v1/auth/password-reset-confirm/<code de confirmation>/<code de autorisation>/   copie code de confirmation et code de confirmation pour se identifier et confirmer la rénisialisation de mot de passe  '}, status=status.HTTP_200_OK)
        # return Response({'message':'user with that email does not exist'}, status=status.HTTP_400_BAD_REQUEST


class PasswordResetConfirm(GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'credentials is valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':"La réinitialisation du mot de passe a réussi"}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        success_message = serializer.save()  # Get success message
        return Response({"detail": success_message}, status=status.HTTP_204_NO_CONTENT)


class BloqueruserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            # Check permissions for user modification
            if request.user.is_superuser or (request.user.role == 'admin' and request.user != user):
                is_active = request.data.get('is_active')
                if is_active is not None:
                    user.is_active = is_active
                    user.save()

                    # If the user is a chercheur and is_active is set to False, update the statut in the Chercheur model
                    if user.role == 'chercheur' and not is_active:
                        chercheur = user.chercheur
                        chercheur.statut = 'Bloqué'
                        chercheur.save()

                    # Get the updated user data
                    updated_user = self.get_serializer(user).data
                    return Response({"detail": "L'état d'activation de l'utilisateur a été modifié avec succès.",
                                     "user": updated_user}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Veuillez fournir une valeur pour is_active."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"detail": "Vous n'avez pas la permission de modifier l'état d'activation de cet utilisateur."},
                    status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

class DebloqueruserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            # Vérifier les autorisations pour la modification de l'utilisateur
            if request.user.is_superuser or (request.user.role == 'admin' and request.user != user):
                is_active = request.data.get('is_active')
                if is_active is not None:
                    user.is_active = is_active
                    user.save()

                    # Si l'utilisateur est un chercheur et que is_active est défini sur True, mettre à jour le statut dans le modèle Chercheur
                    if user.role == 'chercheur' and is_active:
                        chercheur = user.chercheur
                        chercheur.statut = 'activé'
                        chercheur.save()

                    return Response({"detail": "L'état d'activation de l'utilisateur a été modifié avec succès."},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Veuillez fournir une valeur pour is_active."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Vous n'avez pas la permission de modifier l'état d'activation de cet utilisateur."},
                                status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

class GestionUserView1(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            # Vérifier les autorisations pour la modification de l'utilisateur
            if request.user.is_superuser or (request.user.role == 'admin' and request.user != user):
                # Inverser l'état de l'utilisateur
                user.is_active = not user.is_active
                user.save()

                # Mettre à jour le statut du chercheur si nécessaire
                if user.role == 'chercheur':
                    chercheur = user.chercheur
                    if not user.is_active:
                        chercheur.statut = 'Bloqué'
                    else:
                        chercheur.statut = 'activé'
                    chercheur.save()

                # Récupérer les données mises à jour de l'utilisateur
                updated_user_serializer = self.serializer_class(user, context=self.get_serializer_context())
                return Response({"detail": "L'état d'activation de l'utilisateur a été modifié avec succès.",
                                 "user": updated_user_serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Vous n'avez pas la permission de modifier l'état d'activation de cet utilisateur."},
                                status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)


class GestionUserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            # Vérifier les autorisations pour la modification de l'utilisateur
            if request.user.is_superuser or (request.user.role == 'admin' and request.user != user):
                # Inverser l'état de l'utilisateur
                user.is_active = not user.is_active
                user.save()

                # Mettre à jour le statut du chercheur si nécessaire
                if user.role == 'chercheur':
                    chercheur = user.chercheur
                    if not user.is_active:
                        chercheur.statut = 'Bloqué'
                    else:
                        chercheur.statut = 'activé'
                    chercheur.save()

                # Récupérer les données mises à jour de l'utilisateur
                updated_user_serializer = self.serializer_class(user, context=self.get_serializer_context())

                # Créer un message de notification
                notification_message = "Votre compte a été activé." if user.is_active else "Votre compte a été bloqué."

                return Response({
                    "detail": "L'état d'activation de l'utilisateur a été modifié avec succès.",
                    "user": updated_user_serializer.data,
                    "notification_message": notification_message
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Vous n'avez pas la permission de modifier l'état d'activation de cet utilisateur."},
                                status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
