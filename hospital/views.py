from django.http import HttpResponseRedirect
from django.shortcuts import render

# My Imports
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from hospital.models import Patient


# Function to render the front page
def frontend(request):
    return render(request, 'frontend.html')


# ----- ====== BACKEND SECTION ===== -----
# Function to render the back page
@cache_control(no_cache=True, must_revalidade=True, no_store=True)
@login_required(login_url='login')
def backend(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_patient_list = Patient.objects.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q) | Q(age__icontains=q) | Q(
                gender__icontains=q) | Q(note__icontains=q)
        ).order_by('-created_at')
    else:
        all_patient_list = Patient.objects.all().order_by('-created_at')

    paginator = Paginator(all_patient_list, 10)
    page = request.GET.get('page')
    all_patient = paginator.get_page(page)
    return render(request, 'backend.html', {'patients': all_patient})


# Function to Add new patient
@cache_control(no_cache=True, must_revalidade=True, no_store=True)
@login_required(login_url='login')
def add_patient(request):
    if request.method == "POST":
        if request.POST.get('name') and request.POST.get('phone') and request.POST.get('email') and request.POST.get(
                'age') or request.POST.get('gender') and request.POST.get('note'):
            patient = Patient()
            patient.name = request.POST.get('name')
            patient.phone = request.POST.get('phone')
            patient.email = request.POST.get('email')
            patient.age = request.POST.get('age')
            patient.gender = request.POST.get('gender')
            patient.note = request.POST.get('note')
            patient.save()
            messages.success(request, "Patient added successfully!")
            return HttpResponseRedirect(reverse('backend'))
        else:
            messages.error(request, "Enter data correctly.")
            return HttpResponseRedirect(reverse('backend'))

    return render(request, 'add.html')


# Function to view Patient individually
@cache_control(no_cache=True, must_revalidade=True, no_store=True)
@login_required(login_url='login')
def patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if patient != None:
        return render(request, 'edit.html', {'patient': patient})


# Function to delete Patient individually
@cache_control(no_cache=True, must_revalidade=True, no_store=True)
@login_required(login_url='login')
def delete_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.delete()
    messages.success(request, f'{patient.name} deleted successfully!')
    return HttpResponseRedirect(reverse('backend'))



# Function to edit Patient
@cache_control(no_cache=True, must_revalidade=True, no_store=True)
@login_required()
def edit_patient(request):
    if request.method == "POST":
        patient_id = request.POST.get('id')
        patient = Patient.objects.get(id=patient_id)
        if patient != None:
            patient.name = request.POST.get('name')
            patient.phone = request.POST.get('phone')
            patient.email = request.POST.get('email')
            patient.age = request.POST.get('age')
            patient.gender = request.POST.get('gender')
            patient.note = request.POST.get('note')
            patient.save()
            messages.success(request, f"{patient.name} updated successfully!")
            return HttpResponseRedirect(reverse('backend'))
        else:
            messages.error(request, "Enter data correctly.")
            return HttpResponseRedirect(reverse('backend'))
