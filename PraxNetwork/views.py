from django.shortcuts import render


def vueapp(request):
	c = {'app_id' : '0'}
	if '/networkexplorer' in request.path:
		c = {'app_id' : '1'}
	return render(request, 'vue_app.html', c)


