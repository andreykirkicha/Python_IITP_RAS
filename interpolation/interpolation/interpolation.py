# F -- 2D array of function values
# x1, x2, y1, y2 -- points of known function values
# x, y -- point to interpolate in
def bilinear_interpolation(F, x, y, x1, x2, y1, y2):
    Q11 = F(x1, y1)
    Q12 = F(x1, y2)
    Q21 = F(x2, y1)
    Q22 = F(x2, y2)

    F_int = 1 / (x2 - x1) / (y2 - y1) * ((x2 - x) * (y2 - y) * Q11 +
                                         (x - x1) * (y2 - y) * Q21 + 
                                         (x2 - x) * (y - y1) * Q12 + 
                                         (x - x1) * (y - y1) * Q22)

    return F_int