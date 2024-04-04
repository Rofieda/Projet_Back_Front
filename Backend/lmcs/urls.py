from django.urls import path , include 
from rest_framework.routers import DefaultRouter 
from . import views 

#router = DefaultRouter()
#router.register(r'chercheurs', ProjetsListCreateAPIView)

urlpatterns =[
   
    path('ChercheursList/', views.ChercheurListAPIview.as_view(), name='Chercheur_list'),  # Chercheur list API endpoint
    path('ChercheursList/<int:pk>/', views.ChercheurDetailAPIview.as_view(), name='Chercheur_detail'),
    path('ProjetsList/', views.ProjetListAPIview.as_view(), name='Projet_list'),  # Projet list API endpoint
    path('ProjetsList/<int:pk>/', views.ProjetDetailAPIview.as_view(), name='Projet_detail'),  # Projet detail API endpoint
    path('EncadrementsList/', views.EncadrementListAPIview.as_view(), name='Encadrement_list'),  # Encadrement list API endpoint
    path('EncadrementsList/<int:pk>/', views.EncadrementDetailAPIview.as_view(), name='Encadrement_detail'),  # Encadrement detail API endpoint
    path('Conf_journalsList/', views.ConfJournalListAPIview.as_view(), name='Conf_journal_list'),  # Conf_journal list API endpoint
    path('Conf_journalsList/<int:pk>/', views.ConfJournalDetailAPIview.as_view(), name='Conf_journal_detail'),  # Conf_journal detail API endpoint
    path('ChercheurCreat/' , views.ChercheurCreatAPIview.as_view() , name ='ChercheurCreat'),
    path('ConfJournalCreat/', views.ConfJournalCreatAPIview.as_view(), name='ConfJournalCreat'),
    path('ProjetCreat/',views.ProjetCreateAPIView.as_view(),name='ProjetCreat'),
    path('EncadrementCreat/',views.EncadrementCreatAPIview.as_view(),name='EncadrementCreat'),
    path('publicationsCreate/', views.PublicationCreateAPIView.as_view(), name='publication_create'),
    path('publicationsByChercheur/', views.PublicationByChercheurAPIView.as_view() , name='publication_by_chercheur'),
    path('publications/<int:pk>/modify/', views.PublicationModifyAPIView.as_view(), name='publication_modify'),
    path('publications/<int:pk>/delete/', views.PublicationDeleteAPIView.as_view(), name='publication_delete'),


    path('modifierconf_journ/<int:pk>',views.ConfjournModify.as_view(),name='Conf_Journ_Modify'), 


    path('projetByChercheur/', views.ProjetByChercheurAPIView.as_view(), name='projet_by_chercheur'),
    path('projet/<int:pk>/modify/', views.ProjetModifyAPIView.as_view(), name='projet_modify'),
    path('projet/<int:pk>/delete/', views.ProjetDeleteAPIView.as_view(), name='projet_delete'),

   
    path('encadrementByChercheur/', views.EncadrementByChercheurAPIView.as_view(), name='encadrement_by_chercheur'),
    path('encadrement/<int:pk>/modify/', views.EncadrementModifyAPIView.as_view(), name='encadrement_modify'),
    path('encadrement/<int:pk>/delete/', views.EncadrementDeleteAPIView.as_view(), name='encadrement_delete'),

    #Recherche:
    path('chercheur-search/', views.ChercheurSearchAPIView.as_view(), name='chercheur-search'),
    path('encadrements/search/', views.EncadrementSearchAPIView.as_view(), name='encadrement_search'),
    path('projets/search/', views.ProjetSearchAPIView.as_view(), name='projet_search'),
   #publication_detail:
    path('publication/<int:pk>/', views.PublicationDetailView.as_view(), name='publication_detail'),
]
    

