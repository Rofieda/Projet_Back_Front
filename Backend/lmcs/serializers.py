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
        fields =['annee', 'titre_publication', 'volume','lien_publie','nombre_page', 'rang_chercheur']


    



#_____________________________________________________________________________

class PublicationSerializerByChercheur(serializers.ModelSerializer):
    modify_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()
    conf_journal_acronyme = serializers.SerializerMethodField()
    conf_journal_type = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = ['titre_publication', 'conf_journal_type', 'annee','conf_journal_acronyme', 'citations','modify_url', 'delete_url']

    def get_modify_url(self, obj):
        return reverse('publication_modify', kwargs={'pk': obj.pk})

    def get_delete_url(self, obj):
        return reverse('publication_delete', kwargs={'pk': obj.pk})
    
    def get_conf_journal_acronyme(self, obj):
        conf_journal = obj.Conf_Journal_id
        return conf_journal.acronyme if conf_journal else ''

    def get_conf_journal_type(self, obj):
        conf_journal = obj.Conf_Journal_id
        return conf_journal.p_type if conf_journal else ''


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
        fields = ['intitule', 'type_encadrement', 'annee_debut', 'annee_fin', 'modify_url', 'delete_url']

    def get_modify_url(self, obj):
        return reverse('encadrement_modify', kwargs={'pk': obj.pk})

    def get_delete_url(self, obj):
        return reverse('encadrement_delete', kwargs={'pk': obj.pk})
    

class Conf_JournSerializerByChercheur(serializers.ModelSerializer):
    class Meta:
        model =Conf_journal
        exclude = ['Conf_Journal_id']



#############################################RECHERCHE######################################################
class ChercheurSearchSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class Meta:
        model = Chercheur
        fields = ['nom_chercheur', 'prenom_chercheur', 'grade_ensignement', 'email', 'projet' ,'detail_url']

    def get_detail_url(self, obj):
        return reverse('Chercheur_detail', kwargs={'pk': obj.pk})


class PublicationSearchSerializer(serializers.ModelSerializer):
    p_type = serializers.SerializerMethodField()
    acronyme = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = ['titre_publication', 'p_type', 'annee', 'acronyme', 'citations', 'detail_url']

    def get_p_type(self, obj):
        return obj.Conf_Journal_id.p_type if obj.Conf_Journal_id else None

    def get_acronyme(self, obj):
        return obj.Conf_Journal_id.acronyme if obj.Conf_Journal_id else None

    def get_detail_url(self, obj):
        return reverse('publication_detail', kwargs={'pk': obj.pk})

class EncadrementSearchSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class Meta:
        model = Encadrement
        fields = ['intitule', 'type_encadrement',  'annee_debut','annee_fin' , 'detail_url']

    def get_detail_url(self, obj):
        return reverse('Encadrement_detail', kwargs={'pk': obj.pk})


class ProjetSearchSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class Meta:
        model = Projet
        fields = ['titre_projet', 'annee_debut', 'annee_fin' , 'detail_url']

    def get_detail_url(self, obj):
        return reverse('Projet_detail', kwargs={'pk': obj.pk})

class PublicationDetailSerializer(serializers.ModelSerializer):
    acronyme = serializers.CharField(source='Conf_Journal_id.acronyme', read_only=True)
    nom = serializers.CharField(source='Conf_Journal_id.nom', read_only=True)
    p_type = serializers.CharField(source='Conf_Journal_id.p_type', read_only=True)
    periodicite = serializers.CharField(source='Conf_Journal_id.periodicite', read_only=True)
    lien = serializers.CharField(source='Conf_Journal_id.lien', read_only=True)
    core_classification = serializers.CharField(source='Conf_Journal_id.core_classification', read_only=True)
    scimago_classification = serializers.CharField(source='Conf_Journal_id.scimago_classification', read_only=True)
    qualis_classification = serializers.CharField(source='Conf_Journal_id.qualis_classification', read_only=True)
    dgrsdt_classification = serializers.CharField(source='Conf_Journal_id.dgrsdt_classification', read_only=True)

    class Meta:
        model = Publication
        fields = ['titre_publication', 'acronyme', 'nom', 'p_type', 'periodicite', 'lien', 'core_classification',
                  'scimago_classification', 'qualis_classification', 'dgrsdt_classification', 'annee', 'volume',
                  'citations', 'lien_publie', 'nombre_page', 'rang_chercheur']
