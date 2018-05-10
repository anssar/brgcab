from .core import request

def ping(address, port, api_key):
    return request(address, port, api_key, address, port, api_key, 'ping', {})
    
def get_crew_groups_list(address, port, api_key):
    return request(address, port, api_key, 'get_crew_groups_list', {})
    
def get_crew_info(address, port, api_key, crew_id):
    return request(address, port, api_key, 'get_crew_info', {'crew_id': crew_id})

def get_crews_info(address, port, api_key):
    return request(address, port, api_key, 'get_crews_info', {})
    
def get_drivers_info(address, port, api_key):
    return request(address, port, api_key, 'get_drivers_info', {'locked_drivers': 'true',
    'dismissed_drivers': 'true'})

def get_driver_info(address, port, api_key, driver_id):
    return request(address, port, api_key, 'get_driver_info', {'driver_id': driver_id})

def get_car_info(address, port, api_key, car_id):
    return request(address, port, api_key, 'get_car_info', {'car_id': car_id})
    
def get_cars_info(address, port, api_key):
    return request(address, port, api_key, 'get_cars_info', {'locked_cars': 'true'})
    
def create_car(address, port, api_key, code, mark, color, gos_number):
    return request(address, port, api_key, 'create_car', {'code': code, 'mark': mark, 
    'color': color, 'gos_number': gos_number}, post=True, json=True)
    
def update_car_info(address, port, api_key, car_id, others):
    params = {'car_id': str(car_id)}
    params.update(others)
    return request(address, port, api_key, 'update_car_info', params, post=True, json=True)
    
def create_driver(address, port, api_key, name, car_id, password):
    return request(address, port, api_key, 'create_driver', {'car_id': car_id, 'name': name,
    'password': password}, post=True, json=True)
    
def update_driver_info(address, port, api_key, driver_id, others):
    params = {'driver_id': driver_id}
    params.update(others)
    return request(address, port, api_key, 'update_driver_info', params, post=True, json=True)
    
def create_crew(address, port, api_key, driver_id, car_id, crew_group_id):
    return request(address, port, api_key, 'create_crew', {'crew_group_id': crew_group_id,
    'driver_id': driver_id, 'car_id': car_id}, post=True, json=True)
    
def update_crew_info(address, port, api_key, crew_id, others):
    params = {'crew_id': crew_id}
    params.update(others)
    return request(address, port, api_key, 'update_crew_info', params, post=True, json=True)
