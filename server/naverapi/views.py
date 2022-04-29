from .modules.Preprossor import preprosessor, service

# Create your views here.
# Preprosessing
def index(request):
    result = service(request)
    return result

def index2(request):
    result = preprosessor(request)
    return result