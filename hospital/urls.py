from django.urls import path, include
from . import views

urlpatterns = [
    # Path to the frontend page
    path('', views.frontend, name='frontend'),
    # Path to login / logout
    path('acc/', include('django.contrib.auth.urls')),


    # ----- ====== BACKEND SECTION ===== -----
    # Path to the backend page
    path('backend/', views.backend, name='backend'),
    # Path to Add patient
    path('add_patient/', views.add_patient, name='add_patient'),
    # Path to Edit patient individually
    path('patient/<str:patient_id>/', views.patient, name='patient'),
]
# from django.contrib.auth.urls