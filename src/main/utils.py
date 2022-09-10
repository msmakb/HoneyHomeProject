
def getUserBaseTemplate(request):
    group = request.user.groups.all()[0].name
    base = ""
    for i in str(group).split(' '):
        base += i.lower()
        if str(group).split(' ')[-1] != i:
            base += '_'
    base += '/base.html'
    return base