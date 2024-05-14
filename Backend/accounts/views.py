from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from rest_framework.generics import UpdateAPIView

from django.core.exceptions import ObjectDoesNotExist
from accounts.serializers import  LoginSerializer, AddUserSerializer, UserSerializer, \
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
from rest_framework.generics import RetrieveAPIView
from django.core.mail import send_mail



class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer
#fonction de se connecter
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # Extract the user's role from the validated data
        role = serializer.validated_data.get('role')
        # Add the role to the response data
        response_data = serializer.data
        response_data['role'] = role
        return Response(response_data, status=status.HTTP_200_OK)






class AddUserView(CreateAPIView):
    serializer_class = AddUserSerializer
    permission_classes = [IsAuthenticated]
#fonction pour ajouter un utilisateur par ladmin
    def perform_create(self, serializer):
        # Vérifie si l'utilisateur actuel est superutilisateur ou admin
        if not (self.request.user.is_superuser or self.request.user.role == 'admin'):
            raise PermissionDenied("Vous n'avez pas la permission d'effectuer cette action.")

        user = serializer.save()

        # Logique supplémentaire basée sur le rôle de l'utilisateur
        if user.role == 'chercheur':
            try:
                # Recherche du Chercheur correspondant à l'e-mail de l'utilisateur
                chercheur = Chercheur.objects.get(email=user.email)
                user.chercheur_id = chercheur.id_chercheur
                user.save()  # Sauvegarde de l'ID du chercheur dans l'utilisateur
            except ObjectDoesNotExist:
                pass  # Gérer le cas où aucun chercheur correspondant n'est trouvé
        elif user.role == 'admin':
            user.is_superuser = True
            user.save()

        # Envoi d'un e-mail à l'utilisateur
        self.send_email_to_user(user)

    # Méthode pour envoyer un e-mail à l'utilisateur
    def send_email_to_user(self, user):
        subject = 'Bienvenue à LMCS'
        full_name = f"{user.first_name} {user.last_name}"
        message = f'Bonjour {full_name},\n\nVous avez été ajouté à LMCSQUEST avec succès.\n\n Pour vous connecter, utilisez simplement cette adresse e-mail et utilisez les deux premières lettres de votre prénom comme mot de passe : \n\nLMCS_2024_lesdeuxpremiereslettredevotreprenomenminiscule.'
        from_email = 'llmcsquest@gmail.com'
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class ListUsersView(APIView):
    #fonction pour afficher la liste des utilisateurs
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
#demande de réinitialisation de mot de passe par mail
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Nous vous avons envoyé les codes pour réinitialiser votre mot de passe sous forme http://127.0.0.1:8000/api/v1/auth/password-reset-confirm/<code de confirmation>/<code de autorisation>/   copie code de confirmation et code de confirmation pour se identifier et confirmer la rénisialisation de mot de passe  '}, status=status.HTTP_200_OK)



class PasswordResetConfirm(GenericAPIView):
#fonction de confirmation de mot de passe
    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'credentials is valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(GenericAPIView):#fonction pour changer le mot de passe
    serializer_class=SetNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':"La réinitialisation du mot de passe a réussi"}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):#fonction pour la déconnexion
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        success_message = serializer.save()
        return Response({"detail": success_message}, status=status.HTTP_204_NO_CONTENT)




class GestionUserView(UpdateAPIView):#fonction pour bloquer ou débloquer un utilisateurs
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
                if user.role == 'chercheur' and user.chercheur is not None:
                    chercheur = user.chercheur
                    if not user.is_active:
                        chercheur.statut = 'Non_Actif'
                    else:
                        chercheur.statut = 'Actif'
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


class UserProfileAPIView(RetrieveAPIView):#afficher un utilisateur par son id
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
