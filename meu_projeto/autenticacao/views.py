from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.contrib.auth import logout, get_user_model
from .models import Usuario, Carro
from .forms import RegistroForm, CarroForm
from django.views.generic import TemplateView

User = get_user_model()


def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = RegistroForm()

    return render(request, 'autenticacao/registrar.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            user = None

        if user and user.password == password:
            request.session['user_id'] = user.id
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('formulario')
        else:
            messages.error(request, 'Credenciais invalidas. Verifique seu nome de usuario e senha.')
    return render(request, 'autenticacao/login.html')


def listar_carros(request):
    carros = Carro.objects.all()
    return render(request, 'autenticacao/listar_carros.html', {'carros': carros})

def criar_carro(request):
    if request.method == 'POST':
        form = CarroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_carros')
    else:
        form = CarroForm()
    return render(request, 'autenticacao/criar_carro.html', {'form': form})

def editar_carro(request, pk):
    carro = get_object_or_404(Carro, pk=pk)
    if request.method == 'POST':
        form = CarroForm(request.POST, instance=carro)
        if form.is_valid():
            form.save()
            return redirect('listar_carros')
    else:
        form = CarroForm(instance=carro)
    return render(request, 'autenticacao/editar_carro.html', {'form': form})

def deletar_carro(request, pk):
    carro = get_object_or_404(Carro, pk=pk)
    if request.method == 'POST':
        carro.delete()
        return redirect('listar_carros')
    return render(request, 'autenticacao/deletar_carro.html', {'carro': carro})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

def chat(request):
    return render(request, 'autenticacao/chat.html')

def formulario_view(request):
    return render(request, 'autenticacao/formulario.html')

class RegistrarView(TemplateView):
    template_name = 'autenticacao/registrar.html'
