from math import radians, cos, sin, sqrt, atan2

# Haversine distance between two points (lat/lon in degrees)
def haversine(coord1, coord2):
    R = 6371000  # meters
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# Compute total length of polyline
def polyline_length(polyline):
    total = 0
    for i in range(len(polyline)-1):
        total += haversine(polyline[i], polyline[i+1])
    return total

# Interpolate position along polyline
def interpolate_position(polyline, alpha):
    if alpha <= 0:
        return polyline[0]
    if alpha >= 1:
        return polyline[-1]

    total_len = polyline_length(polyline)
    target = alpha * total_len
    accumulated = 0

    for i in range(len(polyline)-1):
        seg_len = haversine(polyline[i], polyline[i+1])
        if accumulated + seg_len >= target:
            ratio = (target - accumulated) / seg_len
            lat = polyline[i][0] + ratio * (polyline[i+1][0] - polyline[i][0])
            lon = polyline[i][1] + ratio * (polyline[i+1][1] - polyline[i][1])
            return lat, lon
        accumulated += seg_len

    return polyline[-1]
