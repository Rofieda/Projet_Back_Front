from rest_framework import serializers 
from .models import Chercheur , Projet , Encadrement ,Conf_journal ,Publication,ChecheursEncadrements
from django.urls import reverse

class ProjetListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta: 
        model = Projet
        fields = ['titre_projet', 'domaine', 'annee_debut','annee_fin','detail_url']

    def get_detail_url(self, obj):
        return reverse('Projet_detail', kwargs={'pk': obj.pk})  # Generates URL for detail view

class ProjetDetailSerializer(serializers.ModelSerializer):
    membre_liste = serializers.SerializerMethodField()

    class Meta: 
        model = Projet
        fields = ['titre_projet', 'chef_de_projet', 'domaine', 'annee_debut', 'annee_fin', 'membre_liste']

    def get_membre_liste(self, obj):
        membres = Chercheur.objects.filter(checheursprojets__id_projet=obj)
        return [{'nom_complet': f"{membre.nom_chercheur} {membre.prenom_chercheur}"} for membre in membres]
     

class ProjetDetailSerializerSecond(serializers.ModelSerializer):
    
    class Meta: 
        model = Projet
        fields = ['titre_projet', 'chef_de_projet', 'domaine', 'annee_debut', 'annee_fin']

     


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
        fields = ['nom_chercheur', 'grade_recherche', 'email', 'equipe', 'detail_url']

    def get_detail_url(self, obj):
        return reverse('Chercheur_detail', kwargs={'pk': obj.pk})  # Generates URL for detail view
    


class EncadrementDetailSerializer(serializers.ModelSerializer):
    chercheur1 = serializers.SerializerMethodField()
    chercheur2 = serializers.SerializerMethodField()
    
    class Meta: 
        model = Encadrement
        fields = ['intitule', 'type_encadrement', 'annee_debut', 'annee_fin', 'nom_prenom_etd1', 'nom_prenom_etd2', 'chercheur1', 'role_chercheur', 'chercheur2', 'role_chercheur2']

    def get_chercheur1(self, obj):
        chercheur_encadrement = ChecheursEncadrements.objects.filter(encadrement=obj).first()
        if chercheur_encadrement:
            chercheur = chercheur_encadrement.chercheur
            return f"{chercheur.nom_chercheur} {chercheur.prenom_chercheur}"
        return None

    def get_chercheur2(self, obj):
        chercheur_encadrement = ChecheursEncadrements.objects.filter(encadrement=obj).last()
        if chercheur_encadrement:
            chercheur = chercheur_encadrement.chercheur
            return f"{chercheur.nom_chercheur} {chercheur.prenom_chercheur}"
        return None
        
class EncadrementDetailSerializerSecond(serializers.ModelSerializer):
    
    class Meta: 
        model = Encadrement
        fields = ['intitule', 'type_encadrement', 'annee_debut', 'annee_fin', 'nom_prenom_etd1', 'nom_prenom_etd2', 'role_chercheur', 'role_chercheur2']

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


class PublicationModifySerializer(serializers.ModelSerializer):
    acronyme = serializers.SerializerMethodField()
    chercheur = serializers.SerializerMethodField()
    class Meta : 
        model = Publication
        fields =['titre_publication','annee','acronyme', 'lien_publie','chercheur' , 'rang_chercheur' , 'volume','nombre_page','citations']
    
    def get_chercheur(self, obj):
        chercheur_id = obj.id_chercheur_id
        chercheur = Chercheur.objects.get(id_chercheur=chercheur_id)
        return f"{chercheur.nom_chercheur} {chercheur.prenom_chercheur}"

    def get_acronyme(self, obj):
        conf_journal_id = obj.Conf_Journal_id_id
        conf_journal = Conf_journal.objects.get(Conf_Journal_id=conf_journal_id)
        return conf_journal.acronyme

    



#_____________________________________________________________________________

class PublicationSerializerByChercheur(serializers.ModelSerializer):
    modify_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()
    conf_journal_acronyme = serializers.SerializerMethodField()
    conf_journal_type = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = ['id','titre_publication', 'conf_journal_type', 'annee','conf_journal_acronyme', 'citations','modify_url', 'delete_url']

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
        fields = ['id_projet','titre_projet', 'domaine', 'annee_debut', 'annee_fin', 'modify_url', 'delete_url']

    def get_modify_url(self, obj):
        return reverse('projet_modify', kwargs={'pk': obj.pk})

    def get_delete_url(self, obj):
        return reverse('projet_delete', kwargs={'pk': obj.pk})
    

class EncadrementSerializerByChercheur(serializers.ModelSerializer):
    modify_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()

    class Meta:
        model = Encadrement
        fields = ['id_encadrement','intitule', 'type_encadrement', 'annee_debut', 'annee_fin', 'modify_url', 'delete_url']

    def get_modify_url(self, obj):
        return reverse('encadrement_modify', kwargs={'pk': obj.pk})

    def get_delete_url(self, obj):
        return reverse('encadrement_delete', kwargs={'pk': obj.pk})
    

class Conf_JournSerializerByChercheur(serializers.ModelSerializer):
    class Meta:
        model =Conf_journal
        exclude = ['Conf_Journal_id']



#----------------------- MERIEM --------------------------------------------

        
class ChercheurSearchSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class Meta:
        model = Chercheur
        fields = [  'id_chercheur','nom_chercheur', 'prenom_chercheur', 'grade_ensignement', 'email', 'equipe' ,'detail_url']

    def get_detail_url(self, obj):
        return reverse('Chercheur_detail', kwargs={'pk': obj.pk})


class PublicationSearchSerializer(serializers.ModelSerializer):
    p_type = serializers.SerializerMethodField()
    acronyme = serializers.SerializerMethodField()
    chercheur_nom = serializers.CharField(source='id_chercheur.nom_chercheur', read_only=True)
    chercheur_prenom = serializers.CharField(source='id_chercheur.prenom_chercheur',read_only=True)
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = [ 'id','titre_publication', 'p_type', 'annee', 'acronyme', 'rang_chercheur','citations','chercheur_prenom', 'chercheur_nom','detail_url']

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
        fields = ['id_encadrement','intitule', 'type_encadrement',  'annee_debut','annee_fin' , 'detail_url']

    def get_detail_url(self, obj):
        return reverse('Encadrement_detail', kwargs={'pk': obj.pk})


class ProjetSearchSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    class Meta:
        model = Projet
        fields = ['id_projet','titre_projet', 'annee_debut','domaine','annee_fin' , 'detail_url']

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
    chercheur_nom = serializers.CharField(source='id_chercheur.nom_chercheur', read_only=True)  # Ajout du nom du chercheur
    chercheur_prenom = serializers.CharField(source='id_chercheur.prenom_chercheur', read_only=True)  # Ajout du prénom du chercheur

    class Meta:
        model = Publication
        fields = ['id','titre_publication', 'acronyme', 'nom', 'p_type', 'periodicite', 'lien', 'core_classification',
                  'scimago_classification', 'qualis_classification', 'dgrsdt_classification', 'annee', 'volume',
                  'citations', 'lien_publie', 'nombre_page', 'rang_chercheur', 'chercheur_nom', 'chercheur_prenom']

#######################################################"Chercheur_Plus_Cite#######################################################

class ChercheurProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chercheur
        fields = ['id_chercheur', 'nom_chercheur', 'prenom_chercheur', 'etablissement', 'diplome', 'email', 'tel', 'dblp_lien', 'research_gate_lien', 'google_scholar_lien', 'site_web', 'grade_ensignement', 'grade_recherche', 'Qualite', 'h_index', 'sexe', 'equipe', 'statut']

class PublicationCiteSerializer(serializers.ModelSerializer):
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
        fields = [ 'id','titre_publication', 'acronyme', 'nom', 'p_type', 'periodicite', 'lien', 'core_classification',
                  'scimago_classification', 'qualis_classification', 'dgrsdt_classification', 'annee', 'volume',
                  'citations', 'lien_publie', 'nombre_page']

class ChercheurNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chercheur
        fields = ['nom_chercheur', 'prenom_chercheur']


class PublicationCiteSerializer2(serializers.ModelSerializer):
    acronyme = serializers.CharField(source='Conf_Journal_id.acronyme', read_only=True)
    nom = serializers.CharField(source='Conf_Journal_id.nom', read_only=True)
    p_type = serializers.CharField(source='Conf_Journal_id.p_type', read_only=True)
    periodicite = serializers.CharField(source='Conf_Journal_id.periodicite', read_only=True)
    lien = serializers.CharField(source='Conf_Journal_id.lien', read_only=True)
    core_classification = serializers.CharField(source='Conf_Journal_id.core_classification', read_only=True)
    scimago_classification = serializers.CharField(source='Conf_Journal_id.scimago_classification', read_only=True)
    qualis_classification = serializers.CharField(source='Conf_Journal_id.qualis_classification', read_only=True)
    dgrsdt_classification = serializers.CharField(source='Conf_Journal_id.dgrsdt_classification', read_only=True)
    chercheur_nom = serializers.CharField(source='id_chercheur.nom_chercheur', read_only=True)
    chercheur_prenom = serializers.CharField(source='id_chercheur.prenom_chercheur',read_only=True)

    class Meta:
        model = Publication
        fields = [ 'id','titre_publication', 'acronyme', 'nom', 'p_type', 'periodicite', 'lien', 'core_classification',
                  'scimago_classification', 'qualis_classification', 'dgrsdt_classification', 'annee', 'volume',
                  'citations', 'lien_publie', 'nombre_page','chercheur_prenom','chercheur_nom','rang_chercheur']





class ChercheurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chercheur
        fields = ['nom_chercheur', 'prenom_chercheur']

class EncadrementSerializer(serializers.ModelSerializer):
    chercheurs = serializers.SerializerMethodField()

    def get_chercheurs(self, obj):
        chercheurs = ChecheursEncadrements.objects.filter(encadrement=obj)
        chercheurs_list = []
        for ce in chercheurs:
            chercheur_serializer = ChercheurSerializer(ce.chercheur)
            chercheurs_list.append(chercheur_serializer.data)
        return chercheurs_list

    class Meta:
        model = Encadrement
        fields = ['id_encadrement', 'type_encadrement', 'intitule', 'annee_debut', 'annee_fin', 'nom_prenom_etd1', 'nom_prenom_etd2', 'role_chercheur', 'role_chercheur2', 'chercheurs']
class ProjetSerializer(serializers.ModelSerializer):
    chercheurs = serializers.SerializerMethodField()

    def get_chercheurs(self, obj):
        chercheurs = ChecheursProjets.objects.filter(id_projet=obj)
        chercheurs_list = []
        for cp in chercheurs:
            chercheur_serializer = ChercheurSerializer(cp.id_chercheur)
            chercheurs_list.append(chercheur_serializer.data)
        return chercheurs_list

    class Meta:
        model = Projet
        fields = ['id_projet', 'titre_projet', 'chef_de_projet', 'domaine', 'annee_debut', 'annee_fin', 'chercheurs']


