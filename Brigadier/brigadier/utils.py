import random

from .models import Crew, Driver, Car, ControlPair, Brigadier, CrewGroup
from .taximaster.api import get_crew_info, get_driver_info, get_car_info, get_crews_info, get_drivers_info


class ComparableCode():
    def __init__(self, code):
        self.code = code
    def __lt__(self, other):
        return (not self.__gt__(other)) and (not self.__eq__(other))
    def __gt__(self, other):
        other_int_part, other_str_part = self.__partition(other.code)
        self_int_part, self_str_part = self.__partition(self.code)
        if self_int_part == other_int_part:
            return self_str_part > other_str_part
        else:
            return self_int_part > other_int_part
    def __eq__(self, other):
        try:
            return self.code == other.code
        except:
            return False
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __partition(self, code):
        int_part = 0
        index = 0
        while True:
            try:
                int_part = 10 * int_part + int(code[index])
                index += 1
            except:
                break
        return int_part, code[index:] 


def generateCode(mark, color, gos_number):
    return gos_number + " " + mark + " " + color

def generatePassword():
    password = str(random.randrange(1000, 10000))
    return password

def getCrewById(crewId, service):
    crews = Crew.objects.filter(crew_id = crewId)
    crew = None
    for c in crews:
        if c.brigadier.group.service == service:
            crew = c
    return crew

def getDriverById(driverId, service):
    try:
        return Driver.objects.filter(driver_id=driverId).filter(creation_service=service)[0]
    except IndexError:
        pass

def getCarById(carId, service):
    try:
        return Car.objects.filter(car_id=carId).filter(creation_service=service)[0]
    except IndexError:
        pass

def loadNewCrew(crew_id, service, brigadier):
    #load crew info from service
    answer = get_crew_info(service.address, service.port, service.api_key, crew_id)
    if answer['code'] != 0:
        return False
    #load driver info from service
    driver_answer = get_driver_info(service.address, service.port, service.api_key, answer['data']['driver_id'])
    if driver_answer['code'] != 0:
        return False
    driver = getDriverById(answer['data']['driver_id'], service)
    #if driver exist
    if driver is not None:
        driver.name = driver_answer['data']['name']
        driver.mobile_phone = driver_answer['data']['mobile_phone']
        driver.is_dismissed = driver_answer['data']['is_dismissed']
        driver.balance = driver_answer['data']['balance']
        driver.is_locked = driver_answer['data']['is_locked']
    #if driver not exist
    else:
        driver = Driver(driver_id=answer['data']['driver_id'], name=driver_answer['data']['name'],
                        mobile_phone=driver_answer['data']['mobile_phone'], password='----',
                        is_locked=driver_answer['data']['is_locked'], balance=driver_answer['data']['balance'], 
                        is_dismissed=driver_answer['data']['is_dismissed'],
                        creation_service=service)
    driver.save()
    #load car info from service
    car_answer = get_car_info(service.address, service.port, service.api_key, answer['data']['car_id'])
    if car_answer['code'] != 0:
        return False
    car = getCarById(answer['data']['car_id'], service)
    #if car exist
    if car is not None:
        car.code = car_answer['data']['code']
        car.mark = car_answer['data']['mark']
        car.color = car_answer['data']['color']
        car.gos_number = car_answer['data']['gos_number']
        car.is_locked = car_answer['data']['is_locked']
    #if car not exist
    else:
        car = Car.create(code=car_answer['data']['code'], mark=car_answer['data']['mark'], 
                  color=car_answer['data']['color'], gos_number=car_answer['data']['gos_number'],
                  car_id=car_answer['data']['car_id'], is_locked=car_answer['data']['is_locked'],
                  owner_driver=driver, owner_model='driver', service=service)
    car.save()
    #create new crew in database
    crew = Crew(driver=driver, car=car, brigadier=brigadier, online=answer['data']['online'],
                crew_state_id = answer['data']['crew_state_id'], crew_id=crew_id,
                code=answer['data']['code'], static_priority=answer['data']['common_priority'],
                group=CrewGroup.objects.filter(service=service).get(group_id=answer['data']['crew_group_id']))
    crew.save()
    return True

def tryLoad(brigadier, crew_id, service=None):
    #init vars
    if service is None:
        service = brigadier.group.service
    try:
        crew_id = int(crew_id)
    except:
        try:
            crew_id = int(crew_id[:-1])
        except:
            return False
    #try to get crew
    crew = getCrewById(crew_id, service)
    #if crew exist
    if crew is not None:
        #if it is tmp crew
        if crew.brigadier.login == 'system.dummy':
            crew.brigadier = brigadier
            crew.save()
        #success result if crew exist
        return True
    #if crew not exist
    return loadNewCrew(crew_id, service, brigadier)
    

def getCrewsOnlineForGroup(group):
    #init vars
    crews = []
    try:
        address = group.service.address
        port = group.service.port
        api_key = group.service.api_key
    except:
        return crews
    try:
        dummy = Brigadier.objects.get(login='system.dummy')
    except:
        return crews
    #load crews from service
    answer = get_crews_info(address, port, api_key)
    if answer['code'] != 0:
        return crews
    #iterate crews
    for crew in answer['data']['crews_info']:
        #if this crew in group
        if crew['crew_group_id'] == group.group_id:
            #try load this crew on dummy (if it already in database ok too)
            success = tryLoad(dummy, crew['crew_id'], service=group.service)
            #if crew was loaded
            if success:
                if crew['online'] or crew['crew_state_id'] == 9 or crew['crew_state_id'] == 3:
                    crew_a = getCrewById(crew['crew_id'], group.service)
                    if crew_a is not None:
                        crews.append(crew_a)
    return crews

def updateDriversInfo(brigadier):
    address = brigadier.group.service.address
    port = brigadier.group.service.port
    api_key = brigadier.group.service.api_key
    answer = get_drivers_info(address, port, api_key)
    if answer['code'] != 0:
        return
    crews_tmp = Crew.objects.all()
    drivers = {}
    for crew in crews_tmp:
        if crew.brigadier.group.pk == brigadier.group.pk:
            drivers[crew.driver.driver_id] = crew.driver
    for d in answer['data']['drivers_info']:
        if d['driver_id'] in drivers:
            drivers[d['driver_id']].is_dismissed = d['is_dismissed']
            drivers[d['driver_id']].save()

def getMainBrigadiersForGroup(group):
    tmp = Brigadier.objects.filter(group=group)
    mainBrigadiers = []
    for i in tmp:
        cp = ControlPair.objects.filter(subordinate=i)
        if len(cp) == 0:
            mainBrigadiers.append(i)
    return mainBrigadiers

def loadMoreCrews(crew_id, group):
    mainBrigadiers = getMainBrigadiersForGroup(group)
    for i in range(1, 21):
        crew = getCrewById(crew_id - i, group.service)
        if crew is None:
            answer = get_crew_info(group.service.address, group.service.port,
                                   group.service.api_key, crew_id - i)
            if answer['code'] != 0:
                continue
            if answer['data']['crew_group_id'] == group.group_id:
                for b in mainBrigadiers:
                    tryLoad(b, crew_id - i)
