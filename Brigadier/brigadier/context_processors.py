from .models import MenuLink, Brigadier

def menu(request):
    links = MenuLink.objects.filter(active=True)
    try:
        brigadier = Brigadier.objects.get(pk=request.session.get('auth'))
    except:
        return {'links': []}
    rlinks = []
    for link in links:
        if link.link == '/drivers-online/':
            if brigadier.drivers_online_menu:
                rlinks.append(link)
        else:
            rlinks.append(link)
    return {'links': rlinks}

def login(request):
    try:
        brigadier = Brigadier.objects.get(pk=request.session.get('auth'))
    except:
        return {'login': ''}
    if len(brigadier.login) <= 15:
        return {'login': '[' + brigadier.login + ']'}
    else:
        return {'login': '[' + brigadier.login[:12] + '...]'}