from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Brigadier, Car, Driver, Crew, MenuLink, ControlPair, CrewGroup, BrigadierGroupPair
from .utils import generateCode, generatePassword, tryLoad, getCrewsOnlineForGroup, updateDriversInfo, loadMoreCrews, getCrewById, getCarById, getDriverById, ComparableCode
from .debugTools import updateCrewsInfo, uniqCrews, repairCars, repairDrivers, createBrigadierGroupPairs, repairBrigadiers
from .taximaster.api import create_car, create_driver, create_crew, update_crew_info, get_crews_info, get_cars_info, get_drivers_info, get_crew_groups_list, get_crew_info, update_driver_info, get_car_info, get_driver_info


def nopage(request):
    return redirect('/')

def login(request):
    #createBrigadierGroupPairs()
    #repairBrigadiers()
    auth = request.session.get('auth')
    if auth is None:
        return render(request, 'login.html')
    return redirect('/drivers/')

def signin(request):
    login  = str.strip(request.POST.get('login', ''))
    password = str.strip(request.POST.get('pass', ''))
    try:
        brigadier = Brigadier.objects.get(login=login)
    except:
        return render(request, 'error.html', {'message': 'Бригадира не существует!'})
    if brigadier.password != password:
        return render(request, 'error.html', {'message': 'Неверный пароль!'})
    request.session['auth'] = brigadier.pk
    return redirect('/drivers/')

def signout(request):
    if 'auth' in request.session:
        del request.session['auth']
    return redirect('/login/')

def drivers(request):
    auth = request.session.get('auth')
    if auth is None:
        return redirect('/')
    try:
        brigadier = Brigadier.objects.get(pk=auth)
        #uniqCrews()
        #repairCars()
        #repairDrivers()
        updateDriversInfo(brigadier)
        crews = []
        crews_tmp = Crew.objects.filter(brigadier=brigadier)
        for c in crews_tmp:
            if not c.driver.is_dismissed:
                crews.append(c)
        pairs = ControlPair.objects.filter(chief=brigadier)
        for p in pairs:
            crews_tmp = Crew.objects.filter(brigadier=p.subordinate)
            for c in crews_tmp:
                if not c.driver.is_dismissed:
                    crews.append(c)
        crews = sorted(crews, key=lambda crew:(crew.static_priority, ComparableCode(crew.code)), reverse=True)
    except :
        return redirect('/signout/')
    return render(request, 'drivers.html', {'crews': crews})

def drivers_online(request):
    auth = request.session.get('auth')
    if auth is None:
        return redirect('/')
    try:
        brigadier = Brigadier.objects.get(pk=auth)
        crews = []
        #crews = getCrewsOnlineForGroup(brigadier.group)
        #crews_a = getCrewsOnlineForGroup(brigadier.additional_group)
        #crews.extend(crews_a)
        pairs = BrigadierGroupPair.objects.filter(brigadier=Brigadier.objects.get(pk=auth))
        for p in pairs:
            crews.extend(getCrewsOnlineForGroup(p.group))
        crews = sorted(crews, key=lambda crew:ComparableCode(crew.code), reverse=True)
    except IndexError:
        return redirect('/signout/')
    return render(request, 'drivers_online.html', {'crews': crews})

def make_driver(request):
    auth = request.session.get('auth')
    if auth is None:
        return render(request, 'error.html', {'message': 'Вы не авторизованы!'})
    cars = []
    cars_b = Car.objects.filter(owner_brigadier=Brigadier.objects.get(pk=auth))
    for c in cars_b:
        cars.append(c)
    pairs = ControlPair.objects.filter(chief=Brigadier.objects.get(pk=auth))
    for p in pairs:
        cars_tmp = Car.objects.filter(owner_brigadier=p.subordinate)
        for c in cars_tmp:
            cars.append(c)
    groups = []
    pairs = BrigadierGroupPair.objects.filter(brigadier=Brigadier.objects.get(pk=auth))
    for p in pairs:
        groups.append(p.group)
    return render(request, 'create_driver.html', {'cars': cars, 'groups': groups})

def create(request):
    auth = request.session.get('auth')
    if auth is None:
        return redirect('/')
    surname = str.strip(request.POST.get('surname', '')).capitalize()
    firstname = str.strip(request.POST.get('firstname', '')).capitalize()
    patronymic = str.strip(request.POST.get('patronymic', '')).capitalize()
    phone = str.strip(request.POST.get('phone', ''))
    gos_number = str.strip(request.POST.get('gos_number', ''))
    mark = request.POST.get('mark', '')
    color = request.POST.get('color', '')
    brigadier_car = request.POST.get('brigadier_car', '')
    group = request.POST.get('group', '')
    if not all([surname, firstname, patronymic, phone, group]):
        return render(request, 'error.html', {'message': 'Не все поля заполнены!'})
    if not all([mark, color, gos_number]) and not all([brigadier_car]):
        return render(request, 'error.html', {'message': 'Не все поля заполнены!'})
    brigadier = Brigadier.objects.get(pk=auth)
    address = brigadier.group.service.address
    port = brigadier.group.service.port
    api_key = brigadier.group.service.api_key

    if brigadier_car != '':
        car = getCarById(int(brigadier_car.split('|')[0]), brigadier.group.service)
        code = car.code
        car_id = car.car_id
    else:
        code = generateCode(mark, color, gos_number)
        answer = create_car(address, port, api_key, code, mark, color, gos_number)
        if answer['code'] != 0:
            return render(request, 'error.html', {'message': answer['descr']})
        car_id = answer['data']['car_id']

    password=generatePassword()
    answer = create_driver(address, port, api_key, surname + ' ' + firstname + ' ' + patronymic, car_id, password)
    if answer['code'] != 0:
        return render(request, 'error.html', {'message': answer['descr']})
    driver_id = answer['data']['driver_id']
    answer = update_driver_info(address, port, api_key, driver_id, {'mobile_phone': phone})
    if answer['code'] != 0:
        return render(request, 'error.html', {'message': answer['descr']})
    driver = Driver(name=surname + ' ' + firstname + ' ' + patronymic, mobile_phone=phone,
                    password=password, driver_id=driver_id, is_locked=False, balance=0, 
                    is_dismissed=False, creation_service=brigadier.group.service)
    driver.save()

    if brigadier_car == '':
        car = Car(gos_number=gos_number, code=code, mark=mark, color=color, car_id=car_id,
                  is_locked=False, owner_driver=driver, owner_model='driver', 
                  creation_service=brigadier.group.service)
        car.save()
    answer = create_crew(address, port, api_key, driver_id, car_id, int(group.split('|')[0]))
    if answer['code'] != 0:
        return render(request, 'error.html', {'message': answer['descr']})
    crew_id = answer['data']['crew_id']
    answer = update_crew_info(address, port, api_key, crew_id, {'code': str(driver_id)})
    if answer['code'] != 0:
        return render(request, 'error.html', {'message': answer['descr']})
    crew = Crew(car=car, driver=driver, brigadier=Brigadier.objects.get(pk=auth),
                online=False, crew_id=crew_id, crew_state_id=0, code=str(driver_id),
                static_priority=0, 
                group=CrewGroup.objects.filter(service=brigadier.group.service).get(group_id=int(group.split('|')[0])))
    crew.save()
    loadMoreCrews(crew_id, Brigadier.objects.get(pk=auth).group)
    return redirect('/drivers/driver/' + str(crew.pk) + '/')

def driver(request, crew_pk): 
    auth = request.session.get('auth')
    if auth is None:
        return redirect('/')

    brigadier = Brigadier.objects.get(pk=auth)
    address = brigadier.group.service.address
    port = brigadier.group.service.port
    api_key = brigadier.group.service.api_key

    try:
        crew = Crew.objects.get(pk=crew_pk)
        answer = get_crew_info(address, port, api_key, crew.crew_id)
        if answer['code'] != 0:
            return render(request, 'error.html', {'message': answer['descr']})

        driver_answer = get_driver_info(address, port, api_key, answer['data']['driver_id'])
        if driver_answer['code'] != 0:
            return render(request, 'error.html', {'message': driver_answer['descr']})
        driver = getDriverById(answer['data']['driver_id'], brigadier.group.service)
        if driver is not None:
            driver.name = driver_answer['data']['name']
            driver.mobile_phone = driver_answer['data']['mobile_phone']
            driver.is_dismissed = driver_answer['data']['is_dismissed']
            driver.balance = driver_answer['data']['balance']
            driver.is_locked = driver_answer['data']['is_locked']
        else:
            driver = Driver(driver_id=answer['data']['driver_id'], name=driver_answer['data']['name'],
                            mobile_phone=driver_answer['data']['mobile_phone'], password=generatePassword(),
                            is_locked=driver_answer['data']['is_locked'], balance=driver_answer['data']['balance'], 
                            is_dismissed=driver_answer['data']['is_dismissed'],
                            creation_service=brigadier.group.service)
        driver.save()

        car_answer = get_car_info(address, port, api_key, answer['data']['car_id'])
        if car_answer['code'] != 0:
            return render(request, 'error.html', {'message': car_answer['descr']})
        car = getCarById(answer['data']['car_id'], brigadier.group.service)
        if car is not None:
            car.code = car_answer['data']['code']
            car.mark = car_answer['data']['mark']
            car.color = car_answer['data']['color']
            car.gos_number = car_answer['data']['gos_number']
            car.is_locked = car_answer['data']['is_locked']
        else:
            car = Car.create(code=car_answer['data']['code'], mark=car_answer['data']['mark'], 
                      color=car_answer['data']['color'], gos_number=car_answer['data']['gos_number'],
                      car_id=car_answer['data']['car_id'], is_locked=car_answer['data']['is_locked'],
                      owner_driver=driver, owner_model='driver', service=brigadier.group.service)
        car.save()

        crew.driver = driver
        crew.online = answer['data']['online']
        crew.crew_state_id = answer['data']['crew_state_id']
        crew.code = answer['data']['code']
        crew.static_priority = answer['data']['common_priority']
        crew.car = car
        crew.group = CrewGroup.objects.filter(service=brigadier.group.service).get(group_id=answer['data']['crew_group_id'])
        crew.save()
    except:
        return render(request, 'error.html', {'message': 'Водителя не существует!'})
    groups = []
    current_group = crew.group
    groups.append(current_group)
    pairs = BrigadierGroupPair.objects.filter(brigadier=Brigadier.objects.get(pk=auth))
    for p in pairs:
        if p.group.pk != current_group.pk:
            groups.append(p.group)

    return render(request, 'driver_info.html', {'crew': crew, 'groups': groups})

def saveName(request, crew_pk):
    auth = request.session.get('auth')
    name = ' '.join([str.capitalize(x) for x in str.strip(request.POST.get('name', '')).split(' ') if x])
    phone = str.strip(request.POST.get('phone', ''))
    group = str.strip(request.POST.get('group', ''))
    if not all([name, phone, group]):
        return render(request, 'error.html', {'message': 'Не все поля заполнены!'})
    if auth is None:
        return redirect('/')
    brigadier = Brigadier.objects.get(pk=auth)
    address = brigadier.group.service.address
    port = brigadier.group.service.port
    api_key = brigadier.group.service.api_key
    try:
        crew = Crew.objects.get(pk=crew_pk)
        driver = crew.driver
        answer = update_driver_info(address, port, api_key, driver.driver_id, {'mobile_phone': phone, 'name': name})
        if answer['code'] != 0:
            return render(request, 'error.html', {'message': answer['descr']})
        driver.name = name
        driver.mobile_phone = phone
        driver.save()
        answer = update_crew_info(address, port, api_key, crew.crew_id, {'crew_group_id': int(group.split('|')[0])})
        if answer['code'] != 0:
            return render(request, 'error.html', {'message': answer['descr']})
        crew.group = CrewGroup.objects.filter(service=brigadier.group.service).get(group_id=int(group.split('|')[0]))
        crew.save()
    except IndexError:
        return render(request, 'error.html', {'message': 'Водителя не существует!'})
    return redirect('/' + request.path.split('/')[1] + '/')

def regeneratePassword(request, crew_pk):
    auth = request.session.get('auth')
    if auth is None:
        return redirect('/')
    brigadier = Brigadier.objects.get(pk=auth)
    address = brigadier.group.service.address
    port = brigadier.group.service.port
    api_key = brigadier.group.service.api_key
    try:
        crew = Crew.objects.get(pk=crew_pk)
        driver = crew.driver
        password = generatePassword()
        answer = update_driver_info(address, port, api_key, driver.driver_id, {'password': password})
        if answer['code'] != 0:
            return render(request, 'error.html', {'message': answer['descr']})
        driver.password = password
        driver.save()
    except:
        return render(request, 'error.html', {'message': 'Водителя не существует!'})
    return redirect('/drivers/driver/' + str(crew.pk) + '/')

def changeCar(request, crew_pk):
    auth = request.session.get('auth')
    if auth is None:
        return redirect('/')
    brigadier = Brigadier.objects.get(pk=auth)
    address = brigadier.group.service.address
    port = brigadier.group.service.port
    api_key = brigadier.group.service.api_key
    try:
        crew = Crew.objects.get(pk=crew_pk)
        cars = []
        cars_d = Car.objects.filter(owner_driver=crew.driver)
        cars_b = Car.objects.filter(owner_brigadier=brigadier)
        for c in cars_b:
            cars.append(c)
        pairs = ControlPair.objects.filter(chief=brigadier)
        for p in pairs:
            cars_tmp = Car.objects.filter(owner_brigadier=p.subordinate)
            for c in cars_tmp:
                cars.append(c)
    except:
        return render(request, 'error.html', {'message': 'Водителя не существует!'})
    return render(request, 'change_car.html', {'cars': cars, 'cars_d': cars_d})

def changeNewCar(request, crew_pk):
    auth = request.session.get('auth')
    if auth is None:
        return redirect('/')
    brigadier = Brigadier.objects.get(pk=auth)
    address = brigadier.group.service.address
    port = brigadier.group.service.port
    api_key = brigadier.group.service.api_key
    try:
        crew = Crew.objects.get(pk=crew_pk)
        gos_number = str.strip(request.POST.get('gos_number', ''))
        mark = request.POST.get('mark', '')
        color = request.POST.get('color', '')
        if not all([gos_number, mark, color]):
            return render(request, 'error.html', {'message': 'Не все поля заполнены!'})
        code = generateCode(mark, color, gos_number)

        answer = create_car(address, port, api_key, code, mark, color, gos_number)
        if answer['code'] != 0:
            return render(request, 'error.html', {'message': answer['descr']})
        car_id = answer['data']['car_id']
        car = Car(gos_number=gos_number, code=code, mark=mark, color=color, car_id=car_id,
                  is_locked=False, owner_driver=crew.driver, owner_model='driver',
                  creation_service=brigadier.group.service)
        car.save()
        answer = update_crew_info(address, port, api_key, crew.crew_id, {'car_id': car_id})
        if answer['code'] != 0:
            if answer['descr'] == 'Forbid update for crew online':
                return render(request, 'error.html', {'message': 
                "Экипаж находится на линии, для редактирования снимите экипаж с линии."})
            return render(request, 'error.html', {'message': answer['descr']})
        crew.car = car
        crew.save()
        driver = crew.driver
        answer = update_driver_info(address, port, api_key, driver.driver_id, {'car_id': car_id})
        if answer['code'] != 0:
            return render(request, 'error.html', {'message': answer['descr']})
        driver.save()
    except:
        return render(request, 'error.html', {'message': 'Водителя не существует!'})
    return redirect('/' + request.path.split('/')[1] + '/')

def changeExistCar(request, crew_pk):
    auth = request.session.get('auth')
    if auth is None:
        return redirect('/')
    brigadier = Brigadier.objects.get(pk=auth)
    address = brigadier.group.service.address
    port = brigadier.group.service.port
    api_key = brigadier.group.service.api_key
    try:
        crew = Crew.objects.get(pk=crew_pk)
        car_desc = request.POST.get('description', '')
        if car_desc == '':
            return render(request, 'error.html', {'message': 'Не все поля заполнены!'})
        try:
            if len(car_desc.split('|')) == 1:
                car = Car.objects.filter(owner_driver=crew.driver).filter(gos_number=car_desc.split(' ')[-1]).get(
                    mark=car_desc.split(' ')[0])
            else:
                car = getCarById(int(car_desc.split('|')[0]), brigadier.group.service)
        except :
            return render(request, 'error.html', {'message': 'Машины не существует!'})
        answer = update_crew_info(address, port, api_key, crew.crew_id, {'car_id': car.car_id})
        if answer['code'] != 0:
            if answer['descr'] == 'Forbid update for crew online':
                return render(request, 'error.html', {'message': 
                "Экипаж находится на линии, для редактирования снимите экипаж с линии."})
            return render(request, 'error.html', {'message': answer['descr']})
        crew.car = car
        crew.save()
        driver = crew.driver
        answer = update_driver_info(address, port, api_key, driver.driver_id, {'car_id': car.car_id})
        if answer['code'] != 0:
            return render(request, 'error.html', {'message': answer['descr']})
        driver.save()
    except:
        return render(request, 'error.html', {'message': 'Водителя не существует!'})
    return redirect('/' + request.path.split('/')[1] + '/')

@login_required(login_url='/admin/')
def load(request):
    return render(request, 'load.html', {'brigadiers': Brigadier.objects.all()})

@login_required(login_url='/admin/')
def loading(request):
    brigadier = int(str.strip(request.POST.get('brigadier', '')).split(' ')[-1])
    crews = str.strip(request.POST.get('crews', '')).split('\r\n')
    try:
        brigadier = Brigadier.objects.get(pk=brigadier)
    except:
        return render(request, 'error.html', {'message': 'бригадира не существует!'})
    for crew in crews:
        tryLoad(brigadier, crew)
    return redirect('/load/')
