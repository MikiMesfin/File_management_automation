from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import File
from .utils import FileOrganizer
import os
from django.conf import settings
from django.core.files import File as DjangoFile

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'status': 'error', 'message': 'No file was uploaded'}, status=400)
            
        uploaded_file = request.FILES['file']
        if not uploaded_file:
            return JsonResponse({'status': 'error', 'message': 'Empty file'}, status=400)
        
        # Create media directory if it doesn't exist
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
            
        # Create temp directory
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        # Save the file temporarily
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        try:
            with open(temp_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Organize the file
            organizer = FileOrganizer(settings.MEDIA_ROOT)
            new_path = organizer.organize_file(temp_path)
            
            # Save file information to database
            file_obj = File.objects.create(
                file=os.path.relpath(new_path, settings.MEDIA_ROOT),
                original_name=uploaded_file.name,
                file_type=uploaded_file.content_type,
                size=uploaded_file.size,
                organized_path=new_path
            )
            
            return JsonResponse({'status': 'success', 'path': new_path})
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error processing file: {str(e)}'
            }, status=500)
        finally:
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return render(request, 'organizer/upload.html')

def file_list(request):
    files = File.objects.all().order_by('-upload_date')
    return render(request, 'organizer/file_list.html', {'files': files})
