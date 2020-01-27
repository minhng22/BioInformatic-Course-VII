import numpy
"""
Find Euclid distance of 2 points v and w in d-dimensions
"""
def euclid_distance(v_coordinator: list, w_coordinator: list, d: int) -> float:
    eu_clid_distance = 0
    for i in range(d):
        eu_clid_distance += numpy.square(v_coordinator[i] - w_coordinator[i])
    return numpy.sqrt(eu_clid_distance)


def find_data_point_min_dis(data_point_coordinator: list, centers: list) -> float:
    d = 0
    for i in range(len(centers)):
        if i == 0:
            d = euclid_distance(data_point_coordinator, centers[i], 2)
        else:
            if euclid_distance(data_point_coordinator, centers[i], 2) < d:
                d = euclid_distance(data_point_coordinator, centers[i], 2)
    return d


def find_max_distance(data_points_coordinators: list, centers: list) -> float:
    d_max = 0
    for i in range(len(data_points_coordinators)):
        local_d = find_data_point_min_dis(data_points_coordinators[i], centers)
        if i == 0:
            d_max = local_d
        else:
            if local_d > d_max:
                d_max = local_d
    return d_max


def father_first_travel ()