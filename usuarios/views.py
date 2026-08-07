from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as django_logout
from inventario.forms import RegistroBomberoForm
from inventario.models import UsuarioBombero

def registro_bombero(request):
    if request.method == 'POST':
        form = RegistroBomberoForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Si aún no hay ningún jefe aprobado en el sistema,
            # el primer jefe registrado se aprueba automáticamente.
            if user.rol == 'jefe' and not UsuarioBombero.objects.filter(
                rol='jefe', is_approved=True
            ).exclude(id=user.id).exists():
                user.is_approved = True
                user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroBomberoForm()
    return render(request, 'registration/registro.html', {'form': form})


def cerrar_sesion(request):
    django_logout(request)
    return redirect('login')