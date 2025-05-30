from django.urls import path
from . import views

urlpatterns = [
    path('designs/', views.design_list, name='design_list'),

    path('design_search/', views.design_search, name='design_search'),

    path('design/<int:design_id>/', views.design_detail, name='design_detail'), 

    #path('add_protein/', views.add_protein, name='add_protein'),
    #path('add_protein/sucesso/', views.add_protein, name='upload_sucesso'),
    
    path('insert_assay/', views.insert_assay, name='insert_assay'),
    
    #path('upload_results/<int:design_id>/<int:technique_id>/', views.upload_results, name='upload_results'),


   #path('test/', views.test, name='test'),


]




