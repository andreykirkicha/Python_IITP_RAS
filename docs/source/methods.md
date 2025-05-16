# Interpolation methods

This project has several interpolation methods implemented. It includes:
- Bilinear interpolation
- Nearest neighbour interpolation

## Bilinear interpolation

This method is used for interpolating functions of two variables (e.g., x and y) using repeated linear interpolation. It is usually applied to functions sampled on a 2D rectilinear grid.

Suppose you have a rectangular grid with points $(x_1, y_1)$, $(x_2, y_1)$, $(x_1, y_2)$, $(x_2, y_2)$, and you want to estimate the value at point $(x, y)$ where $x_1 <= x <= x_2$ and $y_1 <= y <= y_2$. The known values at these points are:

- $f(x_1,y_1) = Q_{11}$
- $f(x_2,y_1) = Q_{21}$
- $f(x_1,y_2) = Q_{12}$
- $f(x_2,y_2) = Q_{22}$

Then, 

$$ f(x, y) = \frac{(x_2 - x)(y_2 - y)}{(x_2 - x_1)(y_2 - y_1)}Q_{11} + \frac{(x - x_1)(y_2 - y)}{(x_2 - x_1)(y_2 - y_1)}Q_{21} + \frac{(x_2 - x)(y - y_1)}{(x_2 - x_1)(y_2 - y_1)}Q_{12} + \frac{(x - x_1)(y - y_1)}{(x_2 - x_1)(y_2 - y_1)}Q_{22}. $$

``` {eval-rst}
.. automodule:: interpolation.methods
  :members:
  :undoc-members:
  :show-inheritance:
```