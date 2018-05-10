from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=128)
    port = models.IntegerField()
    address = models.CharField(max_length=128)
    api_key = models.CharField(max_length=128)

    def __str__(self):
        return '{}'.format(self.name)


class CrewGroup(models.Model):
    group_id = models.IntegerField()
    name = models.CharField(max_length=128)
    service = models.ForeignKey(Service)

    def __str__(self):
        return '{} | {}'.format(self.name, self.service.name)


class MenuLink(models.Model):
    link = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    class_name = models.CharField(max_length=128)
    active = models.BooleanField()

    def __str__(self):
        return '{}'.format(self.name)


class Brigadier(models.Model):
    login = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    group = models.ForeignKey(CrewGroup, related_name='%(class)s_group')
    service = models.ForeignKey(Service, null=True, blank=True)
    additional_group = models.ForeignKey(CrewGroup, blank=True, null=True,
                                         related_name='%(class)s_additional_group')
    drivers_online_menu = models.BooleanField()

    def __str__(self):
        return '{} | {} | {}'.format(self.login, self.group.name, self.group.service.name)


class ControlPair(models.Model):
    chief = models.ForeignKey(Brigadier, related_name='%(class)s_chief')	
    subordinate = models.ForeignKey(Brigadier, related_name='%(class)s_subordinate')

    def __str__(self):
        return '{}->{}'.format(self.chief.login, self.subordinate.login)


class BrigadierGroupPair(models.Model):
    brigadier = models.ForeignKey(Brigadier)
    group = models.ForeignKey(CrewGroup)

    def __str__(self):
        return '{}<=>{}'.format(self.brigadier.login, self.group.name)

class Driver(models.Model):
    name = models.CharField(max_length=256)
    password = models.CharField(max_length=128)
    mobile_phone = models.CharField(max_length=128)
    driver_id = models.IntegerField()
    is_locked = models.BooleanField(editable=False)
    balance = models.IntegerField(editable=False)
    is_dismissed = models.BooleanField(editable=False)
    creation_service = models.ForeignKey(Service, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Car(models.Model):
    code = models.CharField(max_length=128, editable=False)
    mark = models.CharField(max_length=128)
    color = models.CharField(max_length=128)
    gos_number = models.CharField(max_length=128)
    car_id = models.IntegerField()
    is_locked = models.BooleanField(editable=False)
    owner_driver = models.ForeignKey(Driver, blank=True, null=True)
    owner_brigadier = models.ForeignKey(Brigadier, blank=True, null=True)
    owner_model = models.CharField(max_length=128, choices=(('driver', 'driver'),('brigadier', ('brigadier'))))
    creation_service = models.ForeignKey(Service, null=True)

    @staticmethod
    def create(service=None, code=None, mark=None, color=None, gos_number=None,
               car_id=None, is_locked=False, owner_driver=None, owner_brigadier=None,
               owner_model='driver'):
        try:
            car = Car.objects.filter(car_id=car_id).filter(creation_service=service)
            car.code = code
            car.mark = mark
            car.color = color
            car.gos_number = gos_number
            car.is_locked = is_locked
            car.save()
            return car
        except:
            pass
        if owner_model == 'driver':
            car = Car(code=code, mark=mark, color=color, gos_number=gos_number,
                      car_id=car_id, is_locked=is_locked, owner_driver=owner_driver,
                      owner_model=owner_model, creation_service=service)
            car.save()
            return car
        if owner_model == 'brigadier':
            car = Car(code=code, mark=mark, color=color, gos_number=gos_number,
                      car_id=car_id, is_locked=is_locked, owner_brigadier=owner_brigadier,
                      owner_model=owner_model, creation_service=service)
            car.save()
            return car


    @property
    def owner(self):
        if self.owner_model == 'driver':
            return self.owner_driver
        return self.owner_brigadier

    def __str__(self):
        return '{} | {} {} {}'.format(self.car_id, self.mark, self.color, self.gos_number)


class Crew(models.Model):
    driver = models.ForeignKey(Driver)
    car = models.ForeignKey(Car)
    brigadier = models.ForeignKey(Brigadier)
    online = models.BooleanField(editable=False)
    group = models.ForeignKey(CrewGroup, null=True, blank=True)
    crew_id = models.IntegerField()
    crew_state_id = models.IntegerField(editable=False)
    code = models.CharField(max_length=128)
    static_priority = models.CharField(max_length=128)

    def __str__(self):
        return '{} {}'.format(self.driver.name, self.car.mark)
