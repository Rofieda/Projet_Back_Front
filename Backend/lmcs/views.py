from django.shortcuts import render
from rest_framework.views import APIView
from .models import Projet ,Chercheur ,Encadrement,Conf_journal ,Publication , ChecheursEncadrements , ChecheursProjets
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProjetListSerializer,EncadrementSerializerByChercheur,ProjetSerializerByChercheur,PublicationSerializerByChercheur,PublicationSerializer,ConfJournalCreat,EncadrementCreatSerializer,ProjetCreatSerializer ,ProjetDetailSerializer,ChercheurCreat,EncadrementListSerializer,EncadrementDetailSerializer ,ChercheurDetailSerializer ,ChercheurListSerializer  ,ConfJournalListSerializer ,ConfJournalDetailSerializer
from rest_framework import generics , permissions, status
from django.contrib.auth import authenticate, login ,logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.db import connection
from accounts.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated



    


class ProjetListAPIview(generics.ListAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetListSerializer

class ProjetDetailAPIview(generics.RetrieveAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetDetailSerializer



class EncadrementListAPIview(generics.ListAPIView):
    queryset=Encadrement.objects.all()
    serializer_class=EncadrementListSerializer    

class EncadrementDetailAPIview(generics.RetrieveAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementDetailSerializer
  

class ChercheurListAPIview(generics.ListAPIView):
    queryset = Chercheur.objects.all()
    serializer_class = ChercheurListSerializer

class ChercheurDetailAPIview(generics.RetrieveAPIView):# for show details for each chercheur 
    queryset = Chercheur.objects.all()
    serializer_class = ChercheurDetailSerializer

class ChercheurCreatAPIview(generics.CreateAPIView):
    queryset=Chercheur.objects.all()
    serializer_class=ChercheurCreat



class ConfJournalListAPIview(generics.ListAPIView): #pour gerer l'affichage de la list des confjournal 
    queryset = Conf_journal.objects.all()
    serializer_class = ConfJournalListSerializer

class ConfJournalDetailAPIview(generics.RetrieveAPIView):# for show details for each chercheur 
    queryset = Conf_journal.objects.all()
    serializer_class = ConfJournalDetailSerializer 
    
class ConfJournalCreatAPIview(generics.CreateAPIView):
    queryset = Conf_journal.objects.all()
    serializer_class = ConfJournalCreat


class PublicationCreateAPIView(APIView):
    def post(self, request):
        # Assuming the request contains data for the new publication
        data = request.data

        # Extract data for the new publication
        annee = data.get('annee')
        titre_publication = data.get('titre_publication')
        volume = data.get('volume')
        citations = data.get('citations')
        lien_publie = data.get('lien_publie')
        nombre_page = data.get('nombre_page')
        rang_chercheur = data.get('rang_chercheur')
        chercheur_id = data.get('chercheur_id')  # Manually provided Chercheur ID

        try:
            # Retrieve Chercheur using provided Chercheur ID
            chercheur = Chercheur.objects.get(id_chercheur=chercheur_id)
        except Chercheur.DoesNotExist:
            return Response({"error": "Chercheur with provided ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve Conf_journal using provided acronym
        acronym = data.get('conf_journal_acronym')
        conf_journal = Conf_journal.objects.filter(acronyme=acronym).first()
        if not conf_journal:
            return Response({"error": "Conf_journal with provided acronym not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the publication with annee value assigned
        publication = Publication(
            id_chercheur=chercheur,
            Conf_Journal_id=conf_journal,  # Assigning the Conf_journal object directly
            annee=annee,
            titre_publication=titre_publication,
            volume=volume,
            citations=citations,
            lien_publie=lien_publie,
            nombre_page=nombre_page,
            rang_chercheur=rang_chercheur
        )
        
        # Save the publication
        publication.save()

        # Serialize the created publication
        serializer = PublicationSerializer(publication)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class EncadrementCreatAPIview(generics.CreateAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementCreatSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        encadrement_data = {
            'type_encadrement': data.get('type_encadrement'),
            'intitule': data.get('intitule'),
            'role_chercheur': data.get('role_chercheur'),
            'role_chercheur2': data.get('role_chercheur2'),
            'annee_debut': data.get('annee_debut'),
            'annee_fin': data.get('annee_fin'),
            'nom_prenom_etd1': data.get('nom_prenom_etd1'),
            'nom_prenom_etd2': data.get('nom_prenom_etd2'),
        }
        chercheur_id = data.get('chercheur_id')

        # Vérifier si un encadrement avec le même intitulé existe déjà
        existing_encadrement = Encadrement.objects.filter(intitule=encadrement_data['intitule']).first()

        if existing_encadrement:
            # Si l'encadrement existe déjà, établir la relation entre ce encadrement et le chercheur
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO lmcs_checheursencadrements (chercheur_id, encadrement_id) VALUES (%s, %s)", [chercheur_id, existing_encadrement.id_encadrement])
            # Serializer l'encadrement existant pour renvoyer en réponse
            serializer = self.get_serializer(existing_encadrement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Si l'encadrement n'existe pas, créer un nouvel encadrement
            encadrement_serializer = self.get_serializer(data=encadrement_data)
            encadrement_serializer.is_valid(raise_exception=True)
            encadrement = encadrement_serializer.save()
            # Établir la relation entre le nouvel encadrement et le chercheur
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO lmcs_checheursencadrements (chercheur_id, encadrement_id) VALUES (%s, %s)", [chercheur_id, encadrement.id_encadrement])
            serializer = self.get_serializer(encadrement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)




class ProjetCreateAPIView(generics.CreateAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetCreatSerializer

    def create(self, request, *args, **kwargs):
        # Assuming the request contains data for the new projet
        data = request.data

        # Extract data for the new projet
        projet_data = {
            'titre_projet': data.get('titre_projet'),
            'chef_de_projet': data.get('chef_de_projet'),
            'domaine': data.get('domaine'),
            'annee_debut': data.get('annee_debut'),
            'annee_fin': data.get('annee_fin'),
        }

        # Manually provided Chercheur ID
        chercheur_id = data.get('chercheur_id')

        try:
            # Retrieve Chercheur using provided Chercheur ID
            chercheur = Chercheur.objects.get(id_chercheur=chercheur_id)
        except Chercheur.DoesNotExist:
            return Response({"error": "Chercheur with provided ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Projet with the same title exist in the projet table 
        existing_projet = Projet.objects.filter(titre_projet=projet_data['titre_projet']).first()
        projet = None  # to avoid the erreur 

        if existing_projet:
            # If Projet exists, establish the relationship with the chercheur
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO lmcs_checheursprojets (id_chercheur_id, id_projet_id) VALUES (%s, %s)", [chercheur_id, existing_projet.id_projet])
        else:
            # If Projet doesn't exist, create it
            projet_serializer = self.get_serializer(data=projet_data)
            projet_serializer.is_valid(raise_exception=True)
            projet = projet_serializer.save()

            # Establish the relationship with the chercheur
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO lmcs_checheursprojets (id_chercheur, id_projet) VALUES (%s, %s)", [chercheur_id, projet.id_projet])

        # Serialize the created Projet
        serializer = self.get_serializer(projet)

        return Response(serializer.data, status=status.HTTP_201_CREATED)




#chercheur id manually
class PublicationByChercheurAPIView12(generics.ListAPIView):
    serializer_class = PublicationSerializerByChercheur

    def get_queryset(self):
        chercheur_id = self.request.query_params.get('chercheur_id')
        if chercheur_id:
            return Publication.objects.filter(id_chercheur=chercheur_id)
        else:
            return Publication.objects.none()
        
class PublicationModifyAPIView(generics.UpdateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

class PublicationDeleteAPIView(generics.DestroyAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

class ProjetByChercheurAPIView(generics.ListAPIView):
    serializer_class = ProjetSerializerByChercheur

    def get_queryset(self):
        chercheur_id = self.request.query_params.get('chercheur_id')
        if chercheur_id:
            # Step 1: Retrieve all project IDs associated with the chercheur
            projet_ids = ChecheursProjets.objects.filter(id_chercheur=chercheur_id).values_list('id_projet', flat=True)
            # Step 2: Retrieve projects corresponding to the project IDs
            return Projet.objects.filter(id_projet__in=projet_ids)
        else:
            return Projet.objects.none()
        

#chercheur id using authentification 
class PublicationByChercheurAPIView(generics.ListAPIView):
    serializer_class = PublicationSerializerByChercheur
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the chercheur_id from the authenticated user
        chercheur_id = self.request.user.chercheur.id_chercheur if self.request.user.is_authenticated else None
        if chercheur_id:
            return Publication.objects.filter(id_chercheur=chercheur_id)
        else:
            return Publication.objects.none()

class PublicationModifyAPIView(generics.UpdateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

class PublicationDeleteAPIView(generics.DestroyAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]






class ProjetModifyAPIView(generics.UpdateAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializerByChercheur

class ProjetDeleteAPIView(generics.DestroyAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializerByChercheur


class EncadrementByChercheurAPIView(generics.ListAPIView):
    serializer_class = EncadrementSerializerByChercheur

    def get_queryset(self):
        chercheur_id = self.request.query_params.get('chercheur_id')
        if chercheur_id:
            # Step 1: Retrieve all project IDs associated with the chercheur
            encadrements_ids = ChecheursEncadrements.objects.filter(chercheur_id=chercheur_id).values_list('encadrement_id', flat=True)
            # Step 2: Retrieve projects corresponding to the project IDs
            return Encadrement.objects.filter(id_encadrement__in=encadrements_ids)
        else:
            return Encadrement.objects.none()
        

class EncadrementModifyAPIView(generics.UpdateAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementSerializerByChercheur

class EncadrementDeleteAPIView(generics.DestroyAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementSerializerByChercheur