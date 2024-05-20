from django.shortcuts import render, get_object_or_404, redirect
from apps.galeria.models import Fotografia
from apps.galeria.forms import FotografiaForms
from django.contrib import messages



def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
        
    
    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)
    return render(request, 'galeria/index.html', {"cards": fotografias})

def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})

def buscar(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    
    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)
    if 'buscar' in request.GET:
        buscar_nome = request.GET['buscar']
        if buscar_nome:
            fotografias = fotografias.filter(nome__icontains=buscar_nome)
    
    return render(request, "galeria/buscar.html", {"cards": fotografias})

def nova_imagem(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    form = FotografiaForms()
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova fotografia cadastrada!')
            return redirect(index)
    return render(request, 'galeria/nova_imagem.html', {'form':form})

def editar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    form = FotografiaForms(instance=fotografia)
    
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fotografia editada com sucesso!')
            return redirect(index)

    return render(request, 'galeria/editar_imagem.html', {'form':form, 'foto_id':foto_id})


def deletar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    fotografia.delete()
    messages.success(request, 'Apagado com sucesso!')
    return redirect('index')

def filtro(request, categoria):
    if categoria == "TODOS":
        fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)
    else:
        fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True, categoria=categoria)
    
    # Debugging prints
    print(f"Categoria: {categoria}")
    print(f"Fotografias encontradas: {fotografias.count()}")
    
    if not fotografias.exists():
        messages.error(request, f'Nenhuma fotografia encontrada para a categoria: {categoria}')
    
    return render(request, "galeria/index.html", {"cards": fotografias})
'''    if categoria == "TODOS":
        fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)
        return render(request, "galeria/index.html", {"cards": fotografias})
    
    
    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True, categoria=categoria)
    return render(request, 'galeria/index.html', {"cards": fotografias})
'''
