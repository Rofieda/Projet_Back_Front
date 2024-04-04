from django.shortcuts import render
from rest_framework.views import APIView
from .models import Projet, Chercheur, Encadrement, Conf_journal, Publication, ChecheursEncadrements, ChecheursProjets
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProjetListSerializer, EncadrementSerializerByChercheur, ProjetSerializerByChercheur, \
    PublicationSerializerByChercheur, PublicationSerializer, ConfJournalCreat, EncadrementCreatSerializer, \
    ProjetCreatSerializer, ProjetDetailSerializer, ChercheurCreat, EncadrementListSerializer, \
    EncadrementDetailSerializer, ChercheurDetailSerializer, ChercheurListSerializer, ConfJournalListSerializer, \
    ConfJournalDetailSerializer, PublicationSearchSerializer, EncadrementSearchSerializer, ProjetSearchSerializer, \
    Conf_JournSerializerByChercheur
from rest_framework import generics, permissions, status
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.db import connection
from accounts.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ChercheurSearchSerializer
from rest_framework import generics, permissions


# ____________________________________________________________________________________________
class ProjetListAPIview(generics.ListAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetListSerializer


# ____________________________________________________________________________________________
class ProjetDetailAPIview(generics.RetrieveAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetDetailSerializer


# ____________________________________________________________________________________________
class EncadrementListAPIview(generics.ListAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementListSerializer


# ____________________________________________________________________________________________
class EncadrementDetailAPIview(generics.RetrieveAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementDetailSerializer


# ____________________________________________________________________________________________
class ChercheurListAPIview(generics.ListAPIView):
    queryset = Chercheur.objects.all()
    serializer_class = ChercheurListSerializer


# ____________________________________________________________________________________________
class ChercheurDetailAPIview(generics.RetrieveAPIView):  # for show details for each chercheur
    queryset = Chercheur.objects.all()
    serializer_class = ChercheurDetailSerializer


# ____________________________________________________________________________________________
class ChercheurCreatAPIview(generics.CreateAPIView):
    queryset = Chercheur.objects.all()
    serializer_class = ChercheurCreat


# ____________________________________________________________________________________________
class ConfJournalListAPIview(generics.ListAPIView):  # pour gerer l'affichage de la list des confjournal
    queryset = Conf_journal.objects.all()
    serializer_class = ConfJournalListSerializer


# ____________________________________________________________________________________________
class ConfJournalDetailAPIview(generics.RetrieveAPIView):  # for show details for each chercheur
    queryset = Conf_journal.objects.all()
    serializer_class = ConfJournalDetailSerializer


# ____________________________________________________________________________________________
class ConfJournalCreatAPIview(generics.CreateAPIView):
    queryset = Conf_journal.objects.all()
    serializer_class = ConfJournalCreat
    permission_classes = [IsAuthenticated]


# ____________________________________________________________________________________________
class PublicationCreateAPIView1234567(APIView):
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
        # get the connected chercheur id
        chercheur_id = self.request.user.chercheur.id_chercheur if self.request.user.is_authenticated else None

        try:
            # Retrieve Chercheur using provided Chercheur ID
            chercheur = Chercheur.objects.get(id_chercheur=chercheur_id)
        except Chercheur.DoesNotExist:
            return Response({"error": "Chercheur does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve Conf_journal using provided acronym
        acronym = data.get('conf_journal_acronym')
        conf_journ = data.get('conf_journ')
        type = data.get('type')
        conf_journal = Conf_journal.objects.filter(acronyme=acronym).first()
        if not conf_journal:
            return Response({"error": "Conf_journal with provided acronym not found."},
                            status=status.HTTP_400_BAD_REQUEST)

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


# _______________________________________________________________________________________________
class PublicationCreateAPIView(APIView):
    def post(self, request):
        data = request.data

        # Extract data for the new publication
        annee = data.get('annee')
        titre_publication = data.get('titre_publication')
        volume = data.get('volume')
        citations = data.get('citations')
        lien_publie = data.get('lien_publie')
        nombre_page = data.get('nombre_page')
        rang_chercheur = data.get('rang_chercheur')

        # Get the connected chercheur id
        chercheur_id = self.request.user.chercheur.id_chercheur if self.request.user.is_authenticated else None

        try:
            # Retrieve Chercheur using provided Chercheur ID
            chercheur = Chercheur.objects.get(id_chercheur=chercheur_id)
        except Chercheur.DoesNotExist:
            return Response({"error": "Chercheur does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve Conf_journal using provided acronym
        acronym = data.get('conf_journal_acronym')
        conf_journ = data.get('conf_journ')
        type = data.get('type')
        conf_journal = Conf_journal.objects.filter(acronyme=acronym).first()
        if not conf_journal:
            return Response({"error": "Conf_journal with provided acronym not found."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if a publication with the same chercheur_id, conf_journal, and titre_publication exists
        existing_publication = Publication.objects.filter(
            id_chercheur=chercheur,
            Conf_Journal_id=conf_journal,
            titre_publication=titre_publication
        ).exists()

        if existing_publication:
            return Response(
                {"error": "Publication with the same chercheur, conf_journal, and titre_publication already exists."},
                status=status.HTTP_400_BAD_REQUEST)

        # Create the publication with annee value assigned
        publication = Publication(
            id_chercheur=chercheur,
            Conf_Journal_id=conf_journal,
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


# ____________________________________________________________________________________________
class EncadrementCreatAPIviewFirst(generics.CreateAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementCreatSerializer
    permission_classes = [IsAuthenticated]

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
        chercheur_id = self.request.user.chercheur.id_chercheur if self.request.user.is_authenticated else None

        # Vérifier si un encadrement avec le même intitulé existe déjà
        existing_encadrement = Encadrement.objects.filter(intitule=encadrement_data['intitule']).first()
        chercheur1 = data.get('chercheur1')
        chercheur2 = data.get('chercheur2')
        if existing_encadrement:
            # Si l'encadrement existe déjà, établir la relation entre ce encadrement et le chercheur
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO lmcs_checheursencadrements (chercheur_id, encadrement_id) VALUES (%s, %s)",
                               [chercheur_id, existing_encadrement.id_encadrement])
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
                cursor.execute("INSERT INTO lmcs_checheursencadrements (chercheur_id, encadrement_id) VALUES (%s, %s)",
                               [chercheur_id, encadrement.id_encadrement])
            serializer = self.get_serializer(encadrement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# ____________________________________________________________________________________________

class EncadrementCreatAPIview(generics.CreateAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementCreatSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        # Check if the user is authenticated and retrieve their corresponding chercheur id
        chercheur_id = None
        if request.user.is_authenticated:
            chercheur = request.user.chercheur
            if chercheur:
                chercheur_id = chercheur.id_chercheur

        # If chercheur_id is not None, it means the user is a chercheur
        if chercheur_id:
            # Use the same logic implemented previously for chercheurs
            # ...

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
            # chercheur_id = self.request.user.chercheur.id_chercheur if self.request.user.is_authenticated else None

            # Vérifier si un encadrement avec le même intitulé existe déjà
            existing_encadrement = Encadrement.objects.filter(intitule=encadrement_data['intitule']).first()
            chercheur1 = data.get('chercheur1')
            chercheur2 = data.get('chercheur2')
            if existing_encadrement:
                # Si l'encadrement existe déjà, établir la relation entre ce encadrement et le chercheur
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO lmcs_checheursencadrements (chercheur_id, encadrement_id) VALUES (%s, %s)",
                        [chercheur_id, existing_encadrement.id_encadrement])
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
                    cursor.execute(
                        "INSERT INTO lmcs_checheursencadrements (chercheur_id, encadrement_id) VALUES (%s, %s)",
                        [chercheur_id, encadrement.id_encadrement])
                serializer = self.get_serializer(encadrement)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            # If chercheur_id is None, it means the user is an assistant
            # Retrieve encadrement data from request
            encadrement_data = {
                'type_encadrement': data.get('type_encadrement'),
                'intitule': data.get('intitule'),
                'annee_debut': data.get('annee_debut'),
                'annee_fin': data.get('annee_fin'),
                'nom_prenom_etd1': data.get('nom_prenom_etd1'),
                'nom_prenom_etd2': data.get('nom_prenom_etd2'),
                'role_chercheur': data.get('role_chercheur'),
                'role_chercheur2': data.get('role_chercheur2'),
            }

            # Check if encadrement with the same title exists
            existing_encadrement = Encadrement.objects.filter(intitule=encadrement_data['intitule']).first()
            chercheur1 = data.get('chercheur1')
            chercheur2 = data.get('chercheur2')

            try:
                chercheur1_id = Chercheur.objects.get(nom_chercheur=chercheur1.split()[0],
                                                      prenom_chercheur=chercheur1.split()[1]).id_chercheur
            except Chercheur.DoesNotExist:
                return Response({"error": "Chercheur 1 does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                chercheur2_id = Chercheur.objects.get(nom_chercheur=chercheur2.split()[0],
                                                      prenom_chercheur=chercheur2.split()[1]).id_chercheur
            except Chercheur.DoesNotExist:
                return Response({"error": "Chercheur 2 does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            # chercheur1_id = Chercheur.objects.filter(nom_chercheur=chercheur1.split()[0], prenom_chercheur=chercheur1.split()[1]).first().id_chercheur
            # chercheur2_id = Chercheur.objects.filter(nom_chercheur=chercheur2.split()[0], prenom_chercheur=chercheur2.split()[1]).first().id_chercheur

            if existing_encadrement:
                # If encadrement exists, establish relations between chercheurs and encadrement
                # Retrieve chercheur ids using their full names
                # chercheur1_id = Chercheur.objects.filter(nom_chercheur=chercheur1.split()[0], prenom_chercheur=chercheur1.split()[1]).first().id_chercheur
                # chercheur2_id = Chercheur.objects.filter(nom_chercheur=chercheur2.split()[0], prenom_chercheur=chercheur2.split()[1]).first().id_chercheur

                # Check if relations already exist
                if not ChecheursEncadrements.objects.filter(chercheur_id=chercheur1_id,
                                                            encadrement_id=existing_encadrement.id_encadrement).exists():
                    ChecheursEncadrements.objects.create(chercheur_id=chercheur1_id,
                                                         encadrement_id=existing_encadrement.id_encadrement)
                if not ChecheursEncadrements.objects.filter(chercheur_id=chercheur2_id,
                                                            encadrement_id=existing_encadrement.id_encadrement).exists():
                    ChecheursEncadrements.objects.create(chercheur_id=chercheur2_id,
                                                         encadrement_id=existing_encadrement.id_encadrement)

                serializer = self.get_serializer(existing_encadrement)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If encadrement does not exist, create new encadrement
                encadrement_serializer = self.get_serializer(data=encadrement_data)
                encadrement_serializer.is_valid(raise_exception=True)
                encadrement = encadrement_serializer.save()

                # Retrieve chercheur ids using their full names
                # chercheur1_id = Chercheur.objects.filter(nom_chercheur=chercheur1.split()[0], prenom_chercheur=chercheur1.split()[1]).first().id_chercheur
                # chercheur2_id = Chercheur.objects.filter(nom_chercheur=chercheur2.split()[0], prenom_chercheur=chercheur2.split()[1]).first().id_chercheur

                # Establish relations between chercheurs and encadrement
                ChecheursEncadrements.objects.create(chercheur_id=chercheur1_id,
                                                     encadrement_id=encadrement.id_encadrement)
                ChecheursEncadrements.objects.create(chercheur_id=chercheur2_id,
                                                     encadrement_id=encadrement.id_encadrement)

                serializer = self.get_serializer(encadrement)
                return Response(serializer.data, status=status.HTTP_201_CREATED)


# ____________________________________________________________________________________________
class ProjetCreateAPIViewfirstfff(generics.CreateAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetCreatSerializer
    permission_classes = [IsAuthenticated]

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
        chercheur_id = self.request.user.chercheur.id_chercheur if self.request.user.is_authenticated else None

        # try:
        # Retrieve Chercheur using provided Chercheur ID
        #   chercheur = Chercheur.objects.get(id_chercheur=chercheur_id)
        # except Chercheur.DoesNotExist:
        #   return Response({"error": "Chercheur with provided ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Projet with the same title exist in the projet table
        existing_projet = Projet.objects.filter(titre_projet=projet_data['titre_projet']).first()
        projet = None  # to avoid the erreur

        if existing_projet:
            # If Projet exists, establish the relationship with the chercheur
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO lmcs_checheursprojets (id_chercheur_id, id_projet_id) VALUES (%s, %s)",
                               [chercheur_id, existing_projet.id_projet])
        else:
            # If Projet doesn't exist, create it
            projet_serializer = self.get_serializer(data=projet_data)
            projet_serializer.is_valid(raise_exception=True)
            projet = projet_serializer.save()

            # Establish the relationship with the chercheur
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO lmcs_checheursprojets (id_chercheur_id, id_projet_id) VALUES (%s, %s)",
                               [chercheur_id, projet.id_projet])

        # Serialize the created Projet
        serializer = self.get_serializer(projet)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ____________________________________________________________________________________________

class ProjetCreateAPIView22(generics.CreateAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetCreatSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data

        # Manually provided Chercheur ID
        chercheur_id = None
        if request.user.is_authenticated:
            chercheur = request.user.chercheur
            if chercheur:
                chercheur_id = chercheur.id_chercheur

        if chercheur_id:  # the chercheur will create the project
            data = request.data

            # Extract data for the new projet
            projet_data = {
                'titre_projet': data.get('titre_projet'),
                'chef_de_projet': data.get('chef_de_projet'),
                'domaine': data.get('domaine'),
                'annee_debut': data.get('annee_debut'),
                'annee_fin': data.get('annee_fin'),
            }

            #
            chercheur_id = self.request.user.chercheur.id_chercheur if self.request.user.is_authenticated else None

            # Check if Projet with the same title exist in the projet table
            existing_projet = Projet.objects.filter(titre_projet=projet_data['titre_projet']).first()
            projet = None  # to avoid the erreur

            if existing_projet:
                # If Projet exists, establish the relationship with the chercheur
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO lmcs_checheursprojets (id_chercheur_id, id_projet_id) VALUES (%s, %s)",
                                   [chercheur_id, existing_projet.id_projet])
            else:
                # If Projet doesn't exist, create it
                projet_serializer = self.get_serializer(data=projet_data)
                projet_serializer.is_valid(raise_exception=True)
                projet = projet_serializer.save()

                # Establish the relationship with the chercheur
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO lmcs_checheursprojets (id_chercheur_id, id_projet_id) VALUES (%s, %s)",
                                   [chercheur_id, projet.id_projet])

            # Serialize the created Projet
            serializer = self.get_serializer(projet)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            data = request.data

            # Assistant creating the projet
            # Extract projet and chercheur data from the request
            titre_projet = data.get('titre_projet')
            chef_de_projet = data.get('chef_de_projet')
            domaine = data.get('domaine')
            annee_debut = data.get('annee_debut')
            annee_fin = data.get('annee_fin')
            membres = data.get('membres', [])

            existing_projet = Projet.objects.filter(titre_projet=titre_projet).first()
            projet = None  # to avoid the erreur

            if existing_projet:
                pass
            else:
                projet = Projet.objects.create(titre_projet=titre_projet,
                                               chef_de_projet=chef_de_projet,
                                               domaine=domaine,
                                               annee_debut=annee_debut,
                                               annee_fin=annee_fin)

            # Establish relationships between chercheurs and projet
            cpt = 0
            for membre in membres:

                nom_chercheur, prenom_chercheur = membre.split()
                chercheur = Chercheur.objects.filter(nom_chercheur=nom_chercheur,
                                                     prenom_chercheur=prenom_chercheur).first()
                if chercheur:
                    cpt += 1
                    # Chercheur exists, establish the relationship
                    ChecheursProjets.objects.create(id_chercheur_id=chercheur, id_projet_id=projet)
                else:
                    if cpt == 0:
                        return Response({"error": "You should add at least one chercheur"},
                                        status=status.HTTP_400_BAD_REQUEST)

            # Return the response
            serializer = self.get_serializer(projet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# ____________________________________________________________________________________________
class ProjetCreateAPIView(generics.CreateAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetCreatSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        projet_data = {
            'titre_projet': data.get('titre_projet'),
            'chef_de_projet': data.get('chef_de_projet'),
            'domaine': data.get('domaine'),
            'annee_debut': data.get('annee_debut'),
            'annee_fin': data.get('annee_fin'),
        }

        # Get the connected user
        user = self.request.user

        if hasattr(user, 'chercheur') and user.chercheur is not None:  # Check if the user is a researcher
            chercheur_id = user.chercheur.id_chercheur
            existing_projet = Projet.objects.filter(titre_projet=projet_data['titre_projet']).first()
            members = data.get('members', [])
            if existing_projet:
                # If the project exists, establish the relationship with the researcher
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO lmcs_checheursprojets (id_chercheur_id, id_projet_id) VALUES (%s, %s)",
                                   [chercheur_id, existing_projet.id_projet])
            else:
                # If the project doesn't exist, create it
                projet_serializer = self.get_serializer(data=projet_data)
                projet_serializer.is_valid(raise_exception=True)
                projet = projet_serializer.save()

                # Establish the relationship with the researcher
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO lmcs_checheursprojets (id_chercheur_id, id_projet_id) VALUES (%s, %s)",
                                   [chercheur_id, projet.id_projet])

            serializer = self.get_serializer(projet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  # User is an assistant
            members = data.get('members', [])
            if not members:
                return Response({"error": "At least one member should be specified"},
                                status=status.HTTP_400_BAD_REQUEST)

            existing_projet = Projet.objects.filter(titre_projet=projet_data['titre_projet']).first()

            if existing_projet:
                # If the project exists, establish relationships with specified members
                for member_name in members:
                    try:
                        chercheur = Chercheur.objects.get(nom_chercheur=member_name.split()[0],
                                                          prenom_chercheur=member_name.split()[1])
                        if not ChecheursProjets.objects.filter(id_chercheur_id=chercheur.id_chercheur,
                                                               id_projet_id=existing_projet.id_projet).exists():
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "INSERT INTO lmcs_checheursprojets (id_chercheur_id, id_projet_id) VALUES (%s, %s)",
                                    [chercheur.id_chercheur, existing_projet.id_projet])
                    except Chercheur.DoesNotExist:
                        return Response({"error": f"Chercheur '{member_name}' does not exist"},
                                        status=status.HTTP_400_BAD_REQUEST)
            else:
                # If the project doesn't exist, create it and establish relationships with specified members
                projet_serializer = self.get_serializer(data=projet_data)
                projet_serializer.is_valid(raise_exception=True)
                existing_projet = projet_serializer.save()

                for member_name in members:
                    member_name = member_name.strip()  # Remove extra spaces
                    member_parts = member_name.split()
                    if len(member_parts) < 2:
                        return Response({"error": f"Invalid member name: {member_name}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    first_name = member_parts[0]
                    last_name = member_parts[1]

                    try:
                        # Searching for the chercheur using both first name and last name
                        chercheur = Chercheur.objects.get(nom_chercheur=first_name, prenom_chercheur=last_name)
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO lmcs_checheursprojets (id_chercheur_id, id_projet_id) VALUES (%s, %s)",
                                [chercheur.id_chercheur, existing_projet.id_projet])
                    except Chercheur.DoesNotExist:
                        return Response({"error": f"Chercheur '{member_name}' does not exist"},
                                        status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(existing_projet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# ____________________________________________________________________________________________

class ProjetByChercheurAPIView(generics.ListAPIView):
    serializer_class = ProjetSerializerByChercheur
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the chercheur_id from the authenticated user
        chercheur_id = self.request.user.chercheur.id_chercheur if self.request.user.is_authenticated else None
        if chercheur_id:
            # Step 1: Retrieve all project IDs associated with the chercheur
            projet_ids = ChecheursProjets.objects.filter(id_chercheur=chercheur_id).values_list('id_projet', flat=True)
            # Step 2: Retrieve projects corresponding to the project IDs
            return Projet.objects.filter(id_projet__in=projet_ids)
        else:
            return Projet.objects.none()


# chercheur id using authentification
class PublicationByChercheurAPIView(generics.ListAPIView):
    serializer_class = PublicationSerializerByChercheur

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
    permission_classes = [IsAuthenticated]


class PublicationDeleteAPIView(generics.DestroyAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [IsAuthenticated]


class ProjetModifyAPIView(generics.UpdateAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializerByChercheur
    permission_classes = [IsAuthenticated]


class ProjetDeleteAPIView(generics.DestroyAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializerByChercheur
    permission_classes = [IsAuthenticated]


class EncadrementByChercheurAPIView(generics.ListAPIView):
    serializer_class = EncadrementSerializerByChercheur
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chercheur_id = self.request.user.chercheur.id_chercheur if self.request.user.is_authenticated else None
        if chercheur_id:
            # Step 1: Retrieve all project IDs associated with the chercheur
            encadrements_ids = ChecheursEncadrements.objects.filter(chercheur_id=chercheur_id).values_list(
                'encadrement_id', flat=True)
            # Step 2: Retrieve projects corresponding to the project IDs
            return Encadrement.objects.filter(id_encadrement__in=encadrements_ids)
        else:
            return Encadrement.objects.none()


class EncadrementModifyAPIView(generics.UpdateAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementSerializerByChercheur
    permission_classes = [IsAuthenticated]


class EncadrementDeleteAPIView(generics.DestroyAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementSerializerByChercheur
    permission_classes = [IsAuthenticated]


class ConfjournModify(generics.UpdateAPIView):
    queryset = Conf_journal.objects.all()
    serializer_class = Conf_JournSerializerByChercheur
    permission_classes = [IsAuthenticated]

####################################################RECHEZRCHE##################################################################
class ChercheurSearchAPIView(generics.ListAPIView):
    serializer_class = ChercheurSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Chercheur.objects.all()

        # Filter by grade_ensignement
        grade_ensignement = self.request.GET.get('grade_ensignement')
        if grade_ensignement:
            queryset = queryset.filter(grade_ensignement=grade_ensignement)



        # Filter by établissement
        etablissement = self.request.GET.get('etablissement')
        if etablissement:
            queryset = queryset.filter(etablissement=etablissement)

        # Filter by diplome
        diplome = self.request.GET.get('diplome')
        if diplome:
            queryset = queryset.filter(diplome=diplome)

        # Filter by sexe
        sexe = self.request.GET.get('sexe')
        if sexe:
            queryset = queryset.filter(sexe=sexe)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Aucun résultat trouvé pour les filtres spécifiés."},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PublicationSearchAPIView(generics.ListAPIView):
    serializer_class = PublicationSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Publication.objects.all()

        # Filtrer par type
        p_type = self.request.GET.get('p_type')
        if p_type:
            queryset = queryset.filter(Conf_Journal_id__p_type=p_type)

        # Filtrer par acronyme
        acronyme = self.request.GET.get('acronyme')
        if acronyme:
            queryset = queryset.filter(Conf_Journal_id__acronyme=acronyme)

        # Filtrer par année
        annee = self.request.GET.get('annee')
        if annee:
            queryset = queryset.filter(annee=annee)

        # Filtrer par mot-clé
        mot_cle = self.request.GET.get('mot_cle')
        if mot_cle:
            queryset = queryset.filter(titre_publication__icontains=mot_cle)

        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Aucun résultat trouvé pour les filtres spécifiés."},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EncadrementSearchAPIView(generics.ListAPIView):
    serializer_class = EncadrementSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Encadrement.objects.all()

        # Filtrer par date de début
        date_debut = self.request.GET.get('date_debut')
        if date_debut:
            queryset = queryset.filter(annee_debut=date_debut)

        # Filtrer par date de fin
        date_fin = self.request.GET.get('date_fin')
        if date_fin:
            queryset = queryset.filter(annee_fin=date_fin)

        # Filtrer par type
        type_encadrement = self.request.GET.get('type_encadrement')
        if type_encadrement:
            queryset = queryset.filter(type_encadrement=type_encadrement)

        # Filtrer par mot-clé
        mot_cle = self.request.GET.get('mot_cle')
        if mot_cle:
            queryset = queryset.filter(intitule__icontains=mot_cle)

        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Aucun résultat trouvé pour les filtres spécifiés."},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProjetSearchAPIView(generics.ListAPIView):
    serializer_class = ProjetSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Projet.objects.all()

        # Filtrer par date de début
        date_debut = self.request.GET.get('date_debut')
        if date_debut:
            queryset = queryset.filter(annee_debut=date_debut)

        # Filtrer par date de fin
        date_fin = self.request.GET.get('date_fin')
        if date_fin:
            queryset = queryset.filter(annee_fin=date_fin)

        # Filtrer par domaine
        domaine = self.request.GET.get('domaine')
        if domaine:
            queryset = queryset.filter(domaine=domaine)

        # Filtrer par mot-clé
        mot_cle = self.request.GET.get('mot_cle')
        if mot_cle:
             queryset = queryset.filter(titre_projet__icontains=mot_cle)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Aucun résultat trouvé pour les filtres spécifiés."},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
