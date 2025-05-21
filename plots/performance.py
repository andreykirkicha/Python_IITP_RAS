import timeit

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

from interpolation import methods

bilinear_interpolation = methods.bilinear_interpolation
nearest_neighbour_interpolation = methods.nearest_neighbour_interpolation
bicubic_interpolation = methods.bicubic_interpolation


def performance_scale_factor(file_path, interpolation_methods):
    image = Image.open(file_path)

    print(">>> Dependency on scale factor")

    scale_factor_list = [0.1, 0.5, 1, 2]
    n = 1

    plt.figure()

    for method_name, method in interpolation_methods.items():
        print(f">>> Method: {method_name}\n")
        T_list = []

        for scale_factor in scale_factor_list:
            if method == bicubic_interpolation and scale_factor > 0.5:
                T_list.append(np.inf)
                continue
            print("    Scale factor: ", scale_factor)
            T = (
                timeit.timeit(
                    lambda interpolation=method, ratio=scale_factor: interpolation(
                        image, ratio
                    ),
                    number=n,
                )
                / n
            )
            T_list.append(T)
            print(f"    Execution time: {T:.3f} ({n} iterations)\n")

        plt.plot(scale_factor_list, T_list, "o-", label=method_name)

    plt.xlabel("Scale factor")
    plt.ylabel("Time, s")
    plt.title("Performance of interpolation methods on different scale factors")
    plt.grid()
    plt.legend()
    plt.savefig("plots/performance_scale_factor.jpg")


if __name__ == "__main__":
    file_path = "example/example.jpg"
    interpolation_methods = {
        "Bilinear interpolation": bilinear_interpolation,
        "Nearest neighbour interpolation": nearest_neighbour_interpolation,
        "Bicubic interpolation": bicubic_interpolation,
    }

    print(">>> Testing performance...\n")

    performance_scale_factor(file_path, interpolation_methods)
