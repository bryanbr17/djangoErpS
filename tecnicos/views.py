from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from .models import Tecnico, VacacionesTecnico, Especialidad, DocumentoTecnico
from .forms import TecnicoForm, VacacionesForm, DocumentoForm

@login_required
def tecnico_list(request):
    # Filtros de búsqueda
    search = request.GET.get('search', '')
    estado = request.GET.get('estado', '')
    especialidad = request.GET.get('especialidad', '')
    
    tecnicos = Tecnico.objects.select_related('usuario').prefetch_related('especialidades')
    
    if search:
        tecnicos = tecnicos.filter(
            usuario__first_name__icontains=search
        ) | tecnicos.filter(
            usuario__last_name__icontains=search
        ) | tecnicos.filter(
            codigo_empleado__icontains=search
        )
    
    if estado:
        tecnicos = tecnicos.filter(estado=estado)
    
    if especialidad:
        tecnicos = tecnicos.filter(especialidades__id=especialidad)
    
    tecnicos = tecnicos.order_by('codigo_empleado')
    
    # Para los filtros
    especialidades = Especialidad.objects.filter(activa=True)
    estados = Tecnico.ESTADO_CHOICES
    
    # Formulario vacío para el modal
    form = TecnicoForm()
    
    context = {
        'tecnicos': tecnicos,
        'especialidades': especialidades,
        'estados': estados,
        'search': search,
        'estado_selected': estado,
        'especialidad_selected': especialidad,
        'form': form,
    }
    
    return render(request, 'tecnicos/list.html', context)

@login_required
def tecnico_detail(request, pk):
    tecnico = get_object_or_404(Tecnico, pk=pk)
    documentos = tecnico.documentos.all()
    vacaciones = tecnico.vacaciones.all()[:5]
    
    context = {
        'tecnico': tecnico,
        'documentos': documentos,
        'vacaciones': vacaciones,
    }
    return render(request, 'tecnicos/detail.html', context)

@login_required
def tecnico_create(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Crear usuario
                    user = User.objects.create_user(
                        username=form.cleaned_data['codigo_empleado'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email']
                    )
                    
                    # Crear técnico
                    tecnico = form.save(commit=False)
                    tecnico.usuario = user
                    tecnico.save()
                    form.save_m2m()  # Para las especialidades
                    
                    messages.success(request, f'Técnico {tecnico.nombre_completo} creado exitosamente.')
                    return redirect('tecnicos:detail', pk=tecnico.pk)
            except Exception as e:
                messages.error(request, f'Error al crear el técnico: {str(e)}')
    else:
        form = TecnicoForm()
    
    return render(request, 'tecnicos/form.html', {
        'form': form,
        'title': 'Nuevo Técnico',
        'action': 'Crear'
    })

@login_required
def tecnico_edit(request, pk):
    tecnico = get_object_or_404(Tecnico, pk=pk)
    
    if request.method == 'POST':
        form = TecnicoForm(request.POST, request.FILES, instance=tecnico)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Actualizar usuario
                    user = tecnico.usuario
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.email = form.cleaned_data['email']
                    user.save()
                    
                    # Actualizar técnico
                    tecnico = form.save()
                    
                    messages.success(request, f'Técnico {tecnico.nombre_completo} actualizado exitosamente.')
                    return redirect('tecnicos:detail', pk=tecnico.pk)
            except Exception as e:
                messages.error(request, f'Error al actualizar el técnico: {str(e)}')
    else:
        # Inicializar formulario con datos del usuario
        initial_data = {
            'first_name': tecnico.usuario.first_name,
            'last_name': tecnico.usuario.last_name,
            'email': tecnico.usuario.email,
        }
        form = TecnicoForm(instance=tecnico, initial=initial_data)
    
    return render(request, 'tecnicos/form.html', {
        'form': form,
        'tecnico': tecnico,
        'title': f'Editar Técnico - {tecnico.nombre_completo}',
        'action': 'Actualizar'
    })

@login_required
def vacaciones_detail(request, pk):
    vacacion = get_object_or_404(VacacionesTecnico, pk=pk)
    return render(request, 'tecnicos/vacaciones_detail.html', {'vacacion': vacacion})

@login_required
def vacaciones_create(request, tecnico_id):
    tecnico = get_object_or_404(Tecnico, pk=tecnico_id)
    
    if request.method == 'POST':
        form = VacacionesForm(request.POST)
        if form.is_valid():
            vacacion = form.save(commit=False)
            vacacion.tecnico = tecnico
            vacacion.save()
            
            messages.success(request, 'Solicitud de vacaciones creada exitosamente.')
            return redirect('tecnicos:detail', pk=tecnico.pk)
    else:
        form = VacacionesForm()
    
    return render(request, 'tecnicos/vacaciones_form.html', {
        'form': form,
        'tecnico': tecnico,
        'title': f'Nueva Solicitud de Vacaciones - {tecnico.nombre_completo}'
    })

@login_required
def documento_upload(request, tecnico_id):
    tecnico = get_object_or_404(Tecnico, pk=tecnico_id)
    
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.tecnico = tecnico
            documento.save()
            
            messages.success(request, 'Documento subido exitosamente.')
            return redirect('tecnicos:detail', pk=tecnico.pk)
    else:
        form = DocumentoForm()
    
    return render(request, 'tecnicos/documento_form.html', {
        'form': form,
        'tecnico': tecnico,
        'title': f'Subir Documento - {tecnico.nombre_completo}'
    })

@login_required
def tecnico_delete(request, pk):
    tecnico = get_object_or_404(Tecnico, pk=pk)

    if request.method == 'POST':
        tecnico.delete()
        messages.success(request, f'Técnico {tecnico.nombre_completo} eliminado exitosamente.')
        return redirect('tecnicos:list')

    context = {
        'tecnico': tecnico,
        'title': f'Eliminar Técnico - {tecnico.nombre_completo}'
    }

    return render(request, 'tecnicos/delete_confirm.html', context)
