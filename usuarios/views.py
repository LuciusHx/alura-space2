from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib.auth.models import User

#biblioteca para validação de login (bom que só isso aqui)
from django.contrib import auth
from django.contrib import messages

def login(request):
    form = LoginForms()
    
    #criando login
    if request.method == 'POST': #POST == Create no CRUD
        form = LoginForms(request.POST)
        
        
        #Verificar se o formulário é válido
        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()
            
        #"Função" para verificiar se o usuário existe no db
        usuario = auth.authenticate(
            request,
            username=nome,
            password=senha,
        )
        #Se o usuário existir, ele é redirecionado para o index.html (TRUE)
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f'{nome} logado com sucesso!')
            return redirect('index')
        #Se não, ele terá que fazer o login novamente
        else:
            messages.error(request, 'Erro ao efetuar login.')
            return redirect('login')
    
    
    return render(request, "usuarios/login.html", {'form': form})

def cadastro(request):
    
    form = CadastroForms()
    
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        
        
        #Verifica se o formulário é válido
        if form.is_valid():
            
            #Verifica se as senhas são iguais 
            
            
            #Se forem iguais, as novas variáveis recebem os dados
            nome = form["nome_cadastro"].value()
            email = form["email"].value()
            senha = form["senha_1"].value()
            
            #Verifica se o nome já existe no db
            if User.objects.filter(username=nome).exists():
                messages.error(request, "O usuário já existe.")
                return redirect('cadastro') 
            
            
            #criando o usuário
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            #Salva o novo usuário no db
            usuario.save()
            messages.success(request, f'{nome} cadastrado com sucesso!')
            return redirect('login')

    return render(request, "usuarios/cadastro.html", {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')