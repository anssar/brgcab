from django.contrib import admin

from .models import Brigadier, Car, Driver, Crew, MenuLink, ControlPair, CrewGroup, Service, BrigadierGroupPair

class CarAdmin(admin.ModelAdmin):
    search_fields = ('car_id',)
    list_filter = ('owner_model',)
    ordering = ('-car_id', )

class BrigadierAdmin(admin.ModelAdmin):
    list_filter = ('group',)
    ordering = ('login', )

admin.site.register(Brigadier, BrigadierAdmin)
admin.site.register(Crew)
admin.site.register(BrigadierGroupPair)
admin.site.register(Car, CarAdmin)
admin.site.register(Driver)
admin.site.register(MenuLink)
admin.site.register(ControlPair)
admin.site.register(CrewGroup)
admin.site.register(Service)