from rest_framework import serializers 
from .models import Chercheur , Projet , Encadrement ,Conf_journal ,Publication
from django.urls import reverse

class ProjetListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta: 
        model = Projet
        fields = ['titre_projet', 'domaine', 'annee_debut','detail_url']

    def get_detail_url(self, obj):
        return reverse('Projet_detail', kwargs={'pk': obj.pk})  # Generates URL for detail view

class ProjetDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Projet
        exclude = ['id_projet']

class ProjetCreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = '__all__'



class ChercheurDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model =Chercheur 
        exclude = ['id_chercheur']

class ChercheurListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta: 
        model = Chercheur 
        fields = ['nom_chercheur', 'grade_ensignement', 'email', 'equipe', 'detail_url']

    def get_detail_url(self, obj):
        return reverse('Chercheur_detail', kwargs={'pk': obj.pk})  # Generates URL for detail view
    


class EncadrementDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model =Encadrement
        exclude = ['id_encadrement']

class EncadrementCreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encadrement
        fields = '__all__'

class EncadrementListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta: 
        model = Encadrement 
        fields = ['intitule', 'type_encadrement', 'annee_debut', 'annee_fin','detail_url']

    def get_detail_url(self, obj):
        return reverse('Encadrement_detail', kwargs={'pk': obj.pk})  # Generates URL for detail view
    

class ConfJournalListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta: 
        model = Conf_journal
        fields = ['acronyme', 'nom', 'periodicite','detail_url']

    def get_detail_url(self, obj):
        return reverse('Conf_journal_detail', kwargs={'pk': obj.pk})



class ConfJournalDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model =Conf_journal 
        exclude = ['Conf_Journal_id']


class ChercheurCreat(serializers.ModelSerializer):
    class Meta : 
        model = Chercheur
        fields ='__all__'

class ConfJournalCreat(serializers.ModelSerializer):
    class Meta : 
        model =Conf_journal
        fields='__all__'


class PublicationSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Publication
        fields ='__all__'




class PublicationSerializerByChercheur(serializers.ModelSerializer):
    modify_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = ['annee', 'titre_publication', 'volume', 'citations', 'modify_url', 'delete_url']

    def get_modify_url(self, obj):
        return reverse('publication_modify', kwargs={'pk': obj.pk})

    def get_delete_url(self, obj):
        return reverse('publication_delete', kwargs={'pk': obj.pk})
    


class ProjetSerializerByChercheur(serializers.ModelSerializer):
    modify_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()

    class Meta:
        model = Projet
        fields = ['titre_projet', 'chef_de_projet', 'domaine', 'annee_debut', 'annee_fin', 'modify_url', 'delete_url']

    def get_modify_url(self, obj):
        return reverse('projet_modify', kwargs={'pk': obj.pk})

    def get_delete_url(self, obj):
        return reverse('projet_delete', kwargs={'pk': obj.pk})
    


class EncadrementSerializerByChercheur(serializers.ModelSerializer):
    modify_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()

    class Meta:
        model = Encadrement
        fields = ['type_encadrement', 'intitule', 'role_chercheur', 'role_chercheur2', 'annee_fin', 'modify_url', 'delete_url']

    def get_modify_url(self, obj):
        return reverse('encadrement_modify', kwargs={'pk': obj.pk})

    def get_delete_url(self, obj):
        return reverse('encadrement_delete', kwargs={'pk': obj.pk})