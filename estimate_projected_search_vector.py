import sys

import matplotlib.pyplot as plt
import numpy.random
import sklearn.decomposition


def generate_points_in_high_dimension_space(p, n):
    """Generate p points in an n-dimensional space"""
    return numpy.random.rand(p, n)


def dimensionally_reduce_points(high_d_points, n, algorithm="PCA"):
    """Reduce the dimension of the points in the high-dimensional space to n"""
    if algorithm == "PCA":
        pca = sklearn.decomposition.PCA(n)
        return list(zip(pca.fit_transform(high_d_points), high_d_points))


def euclidean_distance(point1, point2):
    """Calculate the Euclidean distance between two points"""
    return numpy.linalg.norm(point1 - point2)


def find_k_closest_points(reference_point, low_d_high_d_points, k=None):
    """Find the k closest points to the reference point"""
    indexed_distance = [(i, euclidean_distance(reference_point, point[1]), point[0], point[1]) for i, point in
                        enumerate(low_d_high_d_points)]
    k_closest_points = sorted(indexed_distance, key=lambda x: x[1])
    if k is not None:
        return k_closest_points[:k]
    return k_closest_points


def estimate_projected_search_vector(closest_points):
    """Estimate the projected search vector in the low-dimensional space"""
    total_weighted_distances = sum([1 / point[1] for point in closest_points])
    print(f"{total_weighted_distances = }")
    return sum([point[2] / point[1] for point in closest_points]) / total_weighted_distances


def main():
    # we have two spaces: an N-D space (N >> 2) and a 2-D space
    n = 50
    # given k points in the N-D space that are close to some reference point
    # and given the corresponding k points in the 2-D space,
    # estimate the dimension-reduced point in the 2-D space that corresponds to the reference point
    # first, let us some take some P points in the N-D space where P >> N
    high_d_points = generate_points_in_high_dimension_space(p=100, n=n)
    # high_d_points = numpy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # print(high_d_points)
    # then we dimensionally reduce them
    low_d_high_d_points = dimensionally_reduce_points(high_d_points, n=2)  # optional: choose the algorithm to use
    # print(f"{low_d_high_d_points = }")
    all_low_d_points = [point[0] for point in low_d_high_d_points]
    print(f"{all_low_d_points = }")
    # next for a reference point we find the k closest points in the N-D space
    reference_point = generate_points_in_high_dimension_space(p=n, n=1)
    # reference_point = numpy.array([1, 0.2, 0])
    # print(f"{reference_point = }")
    closest_points = find_k_closest_points(reference_point, low_d_high_d_points, k=10)
    all_low_d_closest_points = [point[2] for point in closest_points]
    print(f"{all_low_d_closest_points = }")
    # print("index\teuclidean_distance\t2-D\tN-D")
    # for points in closest_points:
    #     print("\t".join(map(lambda p: f"{str(p):<20}", points)))
    # now we find the reference point in the low-D space
    reference_point_low_d = estimate_projected_search_vector(closest_points)
    print(f"{reference_point_low_d = }")

    # plt.style.use('_mpl-gallery')

    # plot
    fig, ax = plt.subplots()

    fig.set_size_inches(7, 7)

    x = [point[0] for point in all_low_d_points]
    y = [point[1] for point in all_low_d_points]
    x_closest = [point[0] for point in all_low_d_closest_points]
    y_closest = [point[1] for point in all_low_d_closest_points]

    # all points
    ax.scatter(x, y, s=10, c='grey', alpha=0.5)
    # closest points
    ax.scatter(x_closest, y_closest, s=10, c='blue', alpha=0.5)
    # reference point
    ax.scatter(reference_point_low_d[0], reference_point_low_d[1], s=20, c='red', alpha=1.0)

    plt.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
