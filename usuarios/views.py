from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib.auth.models import User


def login(request):
    form = LoginForms()
    return render(request, "usuarios/login.html", {'form': form})

def cadastro(request):
    form = CadastroForms()
    
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        
        
        #Verifica se o formulário é válido
        if form.is_valid():
            
            #Verifica se as senhas são iguais 
            if form["senha_1"].value() != form["senha_2"].value():
                return redirect('cadastro') 
            
            #Se forem iguais, as novas variáveis recebem os dados
            nome = form["nome_cadastro"].value()
            email = form["email"].value()
            senha = form["senha_1"].value()
            
            #Verifica se o nome já existe no db
            if User.objects.filter(username=nome).exists():
                return redirect('cadastro') 
            
            
            #criando o usuário
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            #Salva o novo usuário no db
            usuario.save()
            return redirect('login')
                
            
    
    return render(request, "usuarios/cadastro.html", {'form': form})
    
