from django.shortcuts import render, get_object_or_404, redirect
from .models import Sala, Agendamento
from .forms import AgendamentoForm
from .models import Agendamento
from django.contrib.auth.decorators import login_required

def listar_salas(request):
    salas = Sala.objects.all()
    return render(request, 'salas/listar_salas.html', {'salas': salas})

def detalhes_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    agendamentos = sala.agendamento_set.all()  # Agendamentos relacionados à sala
    return render(request, 'salas/detalhes_sala.html', {'sala': sala, 'agendamentos': agendamentos})

def agendar_sala(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o agendamento no banco
            return redirect('listar_salas')  # Redireciona para a lista de salas
    else:
        form = AgendamentoForm()
    return render(request, 'salas/agendar_sala.html', {'form': form})

def listar_agendamentos(request):
    """
    Lista todos os agendamentos ordenados por data e horário de início.
    """
    agendamentos = Agendamento.objects.select_related('sala').order_by('data', 'horario_inicio')
    return render(request, 'salas/listar_agendamentos.html', {'agendamentos': agendamentos})


def listar_meus_agendamentos(request):
    """
    Lista apenas os agendamentos do usuário autenticado.
    """
    if request.user.is_authenticated:  # Verifica se o usuário está logado
        agendamentos = Agendamento.objects.filter(
            usuario=request.user  # Filtra pelos agendamentos do usuário logado
        ).select_related('sala').order_by('data', 'horario_inicio')
    else:
        agendamentos = []  # Se não estiver logado, retorna lista vazia
    
    return render(request, 'salas/listar_meus_agendamentos.html', {'agendamentos': agendamentos})

@login_required
def editar_agendamento(request, pk):
    """
    Permite que o usuário edite um agendamento próprio.
    """
    agendamento = get_object_or_404(Agendamento, pk=pk, usuario=request.user)  # Garante que o usuário seja o dono
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('listar_meus_agendamentos')
    else:
        form = AgendamentoForm(instance=agendamento)
    return render(request, 'salas/editar_agendamento.html', {'form': form})

@login_required
def excluir_agendamento(request, pk):
    """
    Permite que o usuário exclua um agendamento próprio.
    """
    agendamento = get_object_or_404(Agendamento, pk=pk, usuario=request.user)
    if request.method == 'POST':
        agendamento.delete()
        return redirect('listar_meus_agendamentos')
    return render(request, 'salas/confirmar_exclusao.html', {'agendamento': agendamento})
