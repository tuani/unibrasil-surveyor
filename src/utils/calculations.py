import math
from typing import Tuple

def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    R = 6371
    return R * c

def calculate_flight_angle(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    
    angle_rad = math.atan2(delta_lon, delta_lat)
    angle_deg = math.degrees(angle_rad)
    
    if angle_deg < 0:
        angle_deg += 360
        
    return angle_deg

def calculate_effective_speed(speed: int, wind_speed: int, wind_direction: str, 
                            flight_angle: float) -> float:
    wind_angles = {
        "N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5,
        "E": 90, "ESE": 112.5, "SE": 135, "SSE": 157.5,
        "S": 180, "SSW": 202.5, "SW": 225, "WSW": 247.5,
        "W": 270, "WNW": 292.5, "NW": 315, "NNW": 337.5
    }
    
    wind_angle_rad = math.radians(wind_angles.get(wind_direction, 0))
    flight_angle_rad = math.radians(flight_angle)
    
    drone_x = speed * math.sin(flight_angle_rad)
    drone_y = speed * math.cos(flight_angle_rad)
    
    wind_x = wind_speed * math.sin(wind_angle_rad)
    wind_y = wind_speed * math.cos(wind_angle_rad)
    
    effective_x = drone_x + wind_x
    effective_y = drone_y + wind_y
    
    return math.sqrt(effective_x**2 + effective_y**2)

def calculate_autonomy(speed: int, base_autonomy: int = 5000, 
                      correction_factor: float = 0.93) -> float:
    if speed <= 36:
        return base_autonomy * correction_factor
    else:
        return base_autonomy * (36 / speed) ** 2 * correction_factor