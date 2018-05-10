from .models import Crew, Driver, Car, ControlPair, Brigadier, CrewGroup, Service, BrigadierGroupPair
from .taximaster.api import get_crew_info, get_driver_info, get_car_info, get_crews_info, get_drivers_info


def updateCrewsInfo(brigadier):
    address = brigadier.group.service.address
    port = brigadier.group.service.port
    api_key = brigadier.group.service.api_key
    crews = []
    crews_tmp = Crew.objects.all()
    for c in crews_tmp:
        if c.brigadier.group.service.name == brigadier.group.service.name:
            crews.append(c)
    for crew in crews:        
        answer = get_crew_info(address, port, api_key, crew.crew_id)
        if answer['code'] == 0:
            driver_answer = get_driver_info(address, port, api_key, answer['data']['driver_id'])
            if driver_answer['code'] != 0:
                continue
            try:
                driver = Driver.objects.get(driver_id=answer['data']['driver_id'])
                driver.name = driver_answer['data']['name']
                driver.mobile_phone = driver_answer['data']['mobile_phone']
                driver.is_dismissed = driver_answer['data']['is_dismissed']
                driver.balance = driver_answer['data']['balance']
                driver.is_locked = driver_answer['data']['is_locked']
            except:
                driver = Driver(driver_id=answer['data']['driver_id'], name=driver_answer['data']['name'],
                                mobile_phone=driver_answer['data']['mobile_phone'], password='----',
                                is_locked=driver_answer['data']['is_locked'], balance=driver_answer['data']['balance'], 
                                is_dismissed=driver_answer['data']['is_dismissed'])
            driver.save()
            car_answer = get_car_info(address, port, api_key, answer['data']['car_id'])
            if car_answer['code'] != 0:
                continue
            try:
                car = Car.objects.get(car_id=answer['data']['car_id'])
                car.code = car_answer['data']['code']
                car.mark = car_answer['data']['mark']
                car.color = car_answer['data']['color']
                car.gos_number = car_answer['data']['gos_number']
                car.is_locked = car_answer['data']['is_locked']
            except:
                car = Car(code=car_answer['data']['code'], mark=car_answer['data']['mark'], 
                         color=car_answer['data']['color'], gos_number=car_answer['data']['gos_number'],
                          car_id=car_answer['data']['car_id'], is_locked=car_answer['data']['is_locked'],
                        owner_driver=driver, owner_model='driver')
            car.save()
            crew.driver = driver
            crew.online = answer['data']['online']
            crew.car = car
            crew.crew_state_id = answer['data']['crew_state_id']
            crew.code = answer['data']['code']
            crew.save()

def uniqCrews():
    crews_tmp = Crew.objects.all()
    crews = []
    for crew in crews_tmp:
        if (crew.crew_id, crew.brigadier.group.service) in crews:
            crew.delete()
        else:
            crews.append((crew.crew_id, crew.brigadier.group.service))
    drivers_tmp = Driver.objects.all()
    drivers = []
    for driver in drivers_tmp:
        try:
            if (driver.driver_id, Crew.objects.get(driver=driver).brigadier.group.service) in drivers:
                driver.delete()
            else:
                drivers.append((driver.driver_id, Crew.objects.get(driver=driver).brigadier.group.service))
        except:
            driver.delete()
    cars_tmp = Car.objects.all()
    cars = []
    for car in cars_tmp:
        try:
            if (car.car_id, Crew.objects.get(car=car).brigadier.group.service) in cars:
                car.delete()
            else:
                cars.append((car.car_id, Crew.objects.get(car=car).brigadier.group.service))
        except:
            car.delete()

def repairCars():
    cars = Car.objects.all()
    for i in cars:
        i.creation_service = Service.objects.get(name='fishka')
        i.save()

def repairDrivers():
    drivers = Driver.objects.all()
    for i in drivers:
        i.creation_service = Service.objects.get(name='fishka')
        i.save()

def repairBrigadiers():
    brigadiers = Brigadier.objects.all()
    for i in brigadiers:
        i.service = i.group.service
        i.save()   

def createBrigadierGroupPairs():
    brigadiers = Brigadier.objects.all()
    for i in brigadiers:
        bgp = BrigadierGroupPair(brigadier=i, group=i.group)
        bgp.save()
        if i.additional_group:
            bgp = BrigadierGroupPair(brigadier=i, group=i.additional_group)
            bgp.save()