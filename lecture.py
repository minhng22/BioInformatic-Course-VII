import inline as inline
import numpy
import random
"""
Find Euclid distance of 2 points v and w in d-dimensions
"""
def euclid_distance(v_coordinator: list, w_coordinator: list, d: int) -> float:
    eu_clid_distance = 0
    for i in range(d):
        eu_clid_distance += numpy.square(v_coordinator[i] - w_coordinator[i])
    return numpy.sqrt(eu_clid_distance)


def find_min_dis(data_point_coordinator: list, centers: list, m: int) -> float:
    d = 0
    for i in range(len(centers)):
        if i == 0:
            d = euclid_distance(data_point_coordinator, centers[i], m)
        else:
            if euclid_distance(data_point_coordinator, centers[i], m) < d:
                d = euclid_distance(data_point_coordinator, centers[i], m)
    return d


def find_md_point(data_point_coordinator: list, centers: list, m: int) -> list:
    d, d_co = 0, []
    for i in range(len(centers)):
        if i == 0:
            d = euclid_distance(data_point_coordinator, centers[i], m)
            d_co = centers[i]
        else:
            if euclid_distance(data_point_coordinator, centers[i], m) < d:
                d = euclid_distance(data_point_coordinator, centers[i], m)
                d_co = centers[i]
    return d_co


def find_max_distance(data_points_coordinators: list, centers: list, m: int) -> float:
    d_max = 0
    for i in range(len(data_points_coordinators)):
        local_d = find_min_dis(data_points_coordinators[i], centers, m)
        if i == 0:
            d_max = local_d
        else:
            if local_d > d_max:
                d_max = local_d
    return d_max


def find_max_distance_data_point(data_points_coordinators: list, centers: list, m: int) -> list:
    d_max, d_max_val = [], 0
    for i in range(len(data_points_coordinators)):
        local_d = find_min_dis(data_points_coordinators[i], centers, m)
        if i == 0:
            d_max_val, d_max = local_d, data_points_coordinators[0]
        else:
            if local_d > d_max_val:
                d_max_val = local_d
                d_max = data_points_coordinators[i]
    return d_max


def father_first_travel (data_point_coordinators: list, k: int, m: int) -> list:
    centers = []
    while len(centers) < k:
        centers.append(find_max_distance_data_point(data_point_coordinators, centers, m))
    return centers


def father_first_travel_with_file_read() -> list:
    f, i, k, m, datas = open('./week_1/father_first_travel.txt'), 0, 0, 0, []
    for line in f:
        if i == 0:
            k = int(line.split(' ')[0])
            m = int(line.split(' ')[1])
        else:
            d = []
            for j in range (m):
                d.append(float(line.split(' ')[j]))
            datas.append(d)
        i += 1
    return father_first_travel(datas, k, m)


def father_first_travel_with_print() -> None:
    ls = father_first_travel_with_file_read()
    for datas in ls:
        for d in datas:
            print(d, end = " ")
        print("")


def find_distortion (data_points_coordinators: list, centers: list, m: int) -> float:
    distortion = 0
    for data_point_coordinators in data_points_coordinators:
        distortion += numpy.square(find_min_dis(data_point_coordinators, centers, m))
    return distortion / len(data_points_coordinators)


def find_squared_distortion_with_print () -> None:
    i, f, k, m, datas, centers = 0, open('./week_1/squared_distortion.txt'), 0, 0, [], []
    for line in f:
        if i == 0:
            k = int(line.split(' ')[0])
            m = int(line.split(' ')[1])
        elif 0 < i < k + 1:
            d = []
            for j in range(m):
                d.append(float(line.split(' ')[j]))
            centers.append(d)
        elif i > k +1:
            c = []
            for j in range(m):
                c.append(float(line.split(' ')[j]))
            datas.append(c)
        i += 1
    print(find_distortion(datas, centers, m))


def lloyd_with_print() -> None:
    f, i, points, k, m = open('./week_1/lloyd_dataset.txt'), 0, [], 0, 0
    for line in f:
        if i == 0:
            k = int(line.split(' ')[0])
            m = int(line.split(' ')[1])
        else:
            p = []
            line = line.split(' ')
            for j in range (m):
                p.append(float(line[j]))
            points.append(p)
        i += 1
    centers = lloy_expands(10, points, k, m)
    for center in centers:
        for c_point in center:
            print(str(round(c_point, 3)), end = " ")
        print("")


def lloy_expands(N: int, points: list, k: int, m: int) -> list:
    c = lloyd(points, k, m)
    min_distortion = find_distortion(points, c, m)
    min_distortion_centers = c.copy()
    for i in range(N):
        c = lloyd(points, k, m)
        d = find_distortion(points, c, m)
        if min_distortion > d:
            min_distortion = d
            min_distortion_centers = c.copy()
        print(min_distortion_centers)
    return min_distortion_centers


def lloyd(points: list, k: int, m: int) -> list:
    centers = random_points(points, k)
    while not centers == clusters_to_centers(centers_to_clusters(centers.copy(), m, points)):
        centers = clusters_to_centers(centers_to_clusters(centers.copy(), m, points)).copy()
    return centers


def random_points(points: list, k: int) -> list:
    ls = random.sample(range(0, len(points)), k)
    return [points[l] for l in ls]


def centers_to_clusters(centers: list, m: int, points: list) -> dict:
    clusters = dict()
    for c in centers:
        clusters[point_to_str(c)] = []
    for point in points:
        md_center = find_md_point(point, centers, m)
        clusters[point_to_str(md_center)].append(point)
    return clusters


def clusters_to_centers (clusters: dict) -> list:
    return [centers_of_gravity(clusters[c_key]) for c_key in clusters.keys()]


def point_to_str(cs: list) -> str:
    c_str = ""
    for c in range(len(cs)):
        c_str += str(cs[c])
        if c != len(cs) - 1: c_str += ";"
    return c_str


def str_to_point(cs: str) -> list:
    return cs.split(";")


def centers_of_gravity(points: list) -> list:
    c = []
    for i in range(len(points[0])):
        c_at_i = 0
        for j in points:
            c_at_i += j[i]
        c.append(c_at_i / len(points))
    return c


"""
Lloyd with numpy
"""
import numpy as np
import seaborn as sns; sns.set()

"""returns k centroids from the initial points"""
def initialize_centroids(points, k):
    centroids = points.copy()
    np.random.shuffle(centroids)
    return centroids[:k]


"""returns an array containing the index to the nearest centroid for each point"""
def closest_centroid(points, centroids):
    distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
    return np.argmin(distances, axis=0)


"""returns the new centroids assigned from the points closest to them"""
def move_centroids(points, closest, centroids):
    return np.array([points[closest == k].mean(axis=0) for k in range(centroids.shape[0])])


def find_k_means_with_print():
    f, i, points, k, m = open('./week_1/lloyd_dataset.txt'), 0, [], 0, 0
    for line in f:
        if i == 0:
            k = int(line.split(' ')[0])
            m = int(line.split(' ')[1])
        else:
            p = []
            line = line.split(' ')
            for j in range(m):
                p.append(float(line[j]))
            p = tuple(p)
            points.append(p)
        i += 1

    points = np.vstack(points)
    centroids = find_k_means_util(points, k)
    print(centroids)


def find_k_means_util(points, k) -> list:
    centroids = initialize_centroids(points, k)
    closest = closest_centroid(points, centroids)
    while not centroids.any() == move_centroids(points, closest, centroids).any():
        centroids = move_centroids(points, closest, centroids)
    return centroids
