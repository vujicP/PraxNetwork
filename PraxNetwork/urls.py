from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from PraxNetwork.views import vueapp
from tastypie.api import Api

from .resources.datadoc import DataDocResource
from .resources.sequence import SequenceResource
from .resources.step import StepResource
from .resources.interpretation import InterpretationResource
from .resources.code import CodeResource
from .resources.concept import ConceptResource



v1_api = Api(api_name='res')
v1_api.register(DataDocResource())
v1_api.register(SequenceResource())
v1_api.register(StepResource())
v1_api.register(InterpretationResource())
v1_api.register(CodeResource())
v1_api.register(ConceptResource())

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', vueapp, name='default'),
    path(r'seqanalysis/', vueapp, name='default'),
    path(r'networkexplorer/', vueapp, name='networkexp'),
    path(r'api/', include(v1_api.urls)),
]
