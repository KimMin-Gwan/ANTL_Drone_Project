from math import *

def calculate_distance(lat1, lon1, lat2, lon2):
    # 지구의 반경 (미터)
    R = 6371000.0

    # 위도 및 경도를 라디안으로 변환
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # 위도 및 경도 차이 계산
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # 하버사인 공식을 사용하여 거리 계산
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def calculate_bearing(lat1, lon1, lat2, lon2):
    # 위도 및 경도를 라디안으로 변환
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # 방위각 계산
    dlon = lon2_rad - lon1_rad
    y = sin(dlon) * cos(lat2_rad)
    x = cos(lat1_rad) * sin(lat2_rad) - sin(lat1_rad) * cos(lat2_rad) * cos(dlon)
    bearing = atan2(y, x)

    return (bearing + 2 * pi) % (2 * pi)  # 0에서 2pi로 범위 조정

def calculate_velocity(distance, time):
    velocity = distance / time
    return velocity

# 시작 위치 및 도착 위치의 GPS 좌표 (예시)
start_lat = 37.7749
start_lon = -122.4194
dest_lat = 34.0522
dest_lon = -118.2437

# 시작 위치와 도착 위치 사이의 거리 계산
distance = calculate_distance(start_lat, start_lon, dest_lat, dest_lon)

# 시작 위치와 도착 위치 사이의 방향 계산 (라디안 단위)
bearing = calculate_bearing(start_lat, start_lon, dest_lat, dest_lon)

# 속도를 계산할 때 사용할 시간 (예시: 1시간 동안 이동)
time = 3600  # 초 단위

# 계산된 거리, 방향 및 시간을 사용하여 속도 계산
velocity = calculate_velocity(distance, time)

print("Distance between start and destination:", distance, "meters")
print("Direction from start to destination (bearing):", degrees(bearing), "degrees")
print("Velocity needed to reach destination in", time, "seconds:", velocity, "m/s")
