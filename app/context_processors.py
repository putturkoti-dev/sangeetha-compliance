from .models import Branch

def global_filters(request):
    try:
        states = Branch.objects.values_list('state', flat=True).distinct()
        branch_list = Branch.objects.values_list('branch', flat=True)
    except:
        states = []
        branch_list = []

    return {
        'states': states,
        'branch_list': branch_list,
    }