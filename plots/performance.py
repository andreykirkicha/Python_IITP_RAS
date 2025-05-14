import timeit
from matplotlib import pyplot as plt
from PIL import Image

from interpolation import methods

bilinear_interpolation = methods.bilinear_interpolation
nearest_neighbour_interpolation = methods.nearest_neighbour_interpolation


def performance_scale_factor(file_path, method, method_name):
    image = Image.open(file_path)

    interpolation = method
    scale_factor_list = [0.1, 0.5, 1, 2]
    T_list = []
    n = 1

    print(f">>> Method: {method_name}\n")

    for scale_factor in scale_factor_list:
        print("    Scale factor: ", scale_factor)
        T = timeit.timeit(lambda: interpolation(image, scale_factor), number=n) / n
        T_list.append(T)
        print(f"    Execution time: {T:.3f} ({n} iterations)\n")

    return scale_factor_list, T_list


file_path = "example/example.jpg"
interpolation_methods = {'Bilinear interpolation': bilinear_interpolation, 
                         'Nearest neighbour interpolation': nearest_neighbour_interpolation}

print(">>> Testing performance...")

fig = plt.figure()
for method_name, interpolation in interpolation_methods.items():
    scale_factor_list, T_list = performance_scale_factor(file_path, interpolation, method_name)
    plt.plot(scale_factor_list, T_list, 'o-', label=method_name)

plt.xlabel("Scale factor")
plt.ylabel("Time, s")
plt.title("Performance of interpolation methods on different scale factors")
plt.grid()
plt.legend()
plt.savefig("plots/performance_scale_factor.jpg")