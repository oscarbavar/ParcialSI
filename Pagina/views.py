from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import PaginaForm
from .models import Pagina

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('descripcion')
            except IntegrityError:
                form = AuthenticationForm(request, data=request.POST)
                return render(request, 'iniciarsesion.html', {"form": form, "error": "Usuario ya existe."})
        return render(request, 'registro.html', {"form": UserCreationForm(), "error": "Contraseñas no coinciden."})

@login_required
def descripcion(request):
    products = Pagina.objects.filter(usuario=request.user)
    return render(request, 'descripcion.html', {"products": products})

@login_required
def crear(request):
    if request.method == "GET":
        form = PaginaForm()
        return render(request, 'crear.html', {"form": form})
    elif request.method == "POST":
        form = PaginaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_product = form.save(commit=False)
                new_product.usuario = request.user
                new_product.save()
                return redirect('descripcion')
            except ValueError:
                error = "Error al guardar el producto."
        else:
            error = "Formulario no válido."
        
        return render(request, 'crear.html', {"form": form, "error": error})

def home(request):
    products = Pagina.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html', context)

@login_required
def cerrarsesion(request):
    logout(request)
    return redirect('home')

def iniciarsesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'iniciarsesion.html', {'form': form, 'error': 'Usuario y/o contraseña incorrectos.'})
        else:
            return render(request, 'iniciarsesion.html', {'form': form, 'error': 'Usuario y/o contraseña incorrectos.'})
    else:
        form = AuthenticationForm()
        return render(request, 'iniciarsesion.html', {'form': form})

@login_required
def detalle(request, product_id):
    product = get_object_or_404(Pagina, pk=product_id, usuario=request.user)
    
    if request.method == 'GET':
        form = PaginaForm(instance=product)
        return render(request, 'detalle.html', {'product': product, 'form': form})
    
    elif request.method == 'POST':
        form = PaginaForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('descripcion')
        else:
            return render(request, 'detalle.html', {'product': product, 'form': form})