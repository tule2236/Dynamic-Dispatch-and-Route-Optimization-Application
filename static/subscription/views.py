from subscription.models import Page
from .form import NameForm
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static



# urlpatterns = [url(r'^page', views.page,  name = 'page') ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



# def get_name(request):
# 	if request.method == 'POST':
# 		form = NameForm(request.POST)
# 		if form.is_valid():
# 			return HttpResponse('Hello')
# 	else: 
# 		form = NameForm()
# 	return render(request, 'subscription/name.html', {'form': form})