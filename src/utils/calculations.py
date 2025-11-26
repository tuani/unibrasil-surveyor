import math
from typing import Tuple, List

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

def ccw(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> bool:
    return (p3[1] - p1[1]) * (p2[0] - p1[0]) > (p2[1] - p1[1]) * (p3[0] - p1[0])

def segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float],
                       p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
    if p1 == p3 or p1 == p4 or p2 == p3 or p2 == p4:
        return False
    return (ccw(p1, p3, p4) != ccw(p2, p3, p4) and 
            ccw(p1, p2, p3) != ccw(p1, p2, p4))

def two_opt_swap(route: List[int], i: int, j: int) -> List[int]:
    if i >= j or i < 0 or j >= len(route):
        return route.copy()
    return route[:i+1] + route[i+1:j+1][::-1] + route[j+1:]

def has_crossings(coords_list: List[Tuple[float, float]]) -> bool:
    n = len(coords_list)
    if n < 4:
        return False
    for i in range(n - 1):
        for j in range(i + 2, n - 1):
            if segments_intersect(coords_list[i], coords_list[i+1],
                                 coords_list[j], coords_list[j+1]):
                return True
    return False

def remove_crossings_2opt(route_ids: List[int], 
                         get_coords_func,
                         max_iterations: int = 10,
                         force_complete: bool = False) -> List[int]:
    if len(route_ids) < 4:
        return route_ids.copy()
    
    coords_list = [get_coords_func(route_id) for route_id in route_ids]
    
    if not force_complete:
        has_any_crossing = False
        for i in range(len(route_ids) - 2):
            for j in range(i + 2, len(route_ids) - 1):
                if segments_intersect(coords_list[i], coords_list[i+1],
                                      coords_list[j], coords_list[j+1]):
                    has_any_crossing = True
                    break
            if has_any_crossing:
                break
        
        if not has_any_crossing:
            return route_ids.copy()
    
    iteration = 0
    max_iters = max_iterations if not force_complete else 10000
    consecutive_no_improvement = 0
    
    while iteration < max_iters:
        improved = False
        
        for i in range(len(route_ids) - 2):
            for j in range(i + 2, len(route_ids) - 1):
                if segments_intersect(coords_list[i], coords_list[i+1],
                                      coords_list[j], coords_list[j+1]):
                    route_ids = two_opt_swap(route_ids, i, j)
                    coords_list = [get_coords_func(route_id) for route_id in route_ids]
                    improved = True
                    consecutive_no_improvement = 0
                    break
            if improved:
                break
        
        if not improved:
            if force_complete:
                has_crossing = False
                for i in range(len(route_ids) - 2):
                    for j in range(i + 2, len(route_ids) - 1):
                        if segments_intersect(coords_list[i], coords_list[i+1],
                                              coords_list[j], coords_list[j+1]):
                            has_crossing = True
                            break
                    if has_crossing:
                        break
                
                if not has_crossing:
                    break
                else:
                    consecutive_no_improvement += 1
                    if consecutive_no_improvement > 100:
                        for i in range(len(route_ids) - 2):
                            for j in range(i + 2, len(route_ids) - 1):
                                if segments_intersect(coords_list[i], coords_list[i+1],
                                                      coords_list[j], coords_list[j+1]):
                                    route_ids = two_opt_swap(route_ids, i, j)
                                    coords_list = [get_coords_func(route_id) for route_id in route_ids]
                                    consecutive_no_improvement = 0
                                    break
                            if consecutive_no_improvement == 0:
                                break
            else:
                break
        
        iteration += 1
    
    if force_complete:
        has_crossing = False
        for i in range(len(route_ids) - 2):
            for j in range(i + 2, len(route_ids) - 1):
                if segments_intersect(coords_list[i], coords_list[i+1],
                                      coords_list[j], coords_list[j+1]):
                    has_crossing = True
                    break
            if has_crossing:
                break
        
        if has_crossing:
            for _ in range(1000):
                for i in range(len(route_ids) - 2):
                    for j in range(i + 2, len(route_ids) - 1):
                        if segments_intersect(coords_list[i], coords_list[i+1],
                                              coords_list[j], coords_list[j+1]):
                            route_ids = two_opt_swap(route_ids, i, j)
                            coords_list = [get_coords_func(route_id) for route_id in route_ids]
                            break
                    else:
                        continue
                    break
                else:
                    break
    
    return route_ids
