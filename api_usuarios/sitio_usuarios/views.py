import csv
import logging
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Usuario
from .forms import UploadFileForm

# Configura el registro de errores
logger = logging.getLogger(__name__)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_users, updated_users = handle_uploaded_file(request.FILES['file'])
                return render(request, 'success.html', {
                    'new_users': new_users,
                    'updated_users': updated_users
                })
            except Exception as e:
                logger.error(f"Error uploading file: {e}")
                return HttpResponse("Error uploading file", status=500)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    new_users = []
    updated_users = []
    try:
        # Abre el archivo en modo texto
        file = f.read().decode('utf-8').splitlines()
        reader = csv.reader(file)
        next(reader)  # Saltar la primera fila (encabezado)
        for row in reader:
            user, created = Usuario.objects.update_or_create(
                nombre_cuenta=row[4],
                defaults={
                    'nombre': row[0],
                    'apellido_paterno': row[1],
                    'apellido_materno': row[2],
                    'edad': int(row[3]),  # Convertir edad a entero
                    'contraseña': row[5],
                }
            )
            if created:
                new_users.append(user)
            else:
                updated_users.append(user)
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise
    return new_users, updated_users

def success(request):
    return render(request, 'success.html')
