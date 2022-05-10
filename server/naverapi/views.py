from .modules.Preprossor import preprosessor, sentiment_analysis

# Create your views here.
# Preprosessing
def index(request):
    result = sentiment_analysis(request)
    return result

def index2(request):
    result = preprosessor(request)
    return result