from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required 

# Create your views here.
@login_required
def notificatios_views(request):
    notification = Notification.objects.filter(user=request.user, read=False)
    return render(request, 'notification/notification.html', {'notifications': notification})
