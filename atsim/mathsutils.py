import numpy as np


def double_sigmoid(x, a, b, width):

    low_x = width * (1 / 4)
    high_x = width * (3 / 4)

    x_low_idx = (x < low_x)
    x_mid_idx = (x >= low_x) & (x < high_x)
    x_high_idx = (x >= high_x)

    x1 = x[x_low_idx]
    x2 = x[x_mid_idx]
    x3 = x[x_high_idx]

    y = np.empty_like(x)

    y[x_low_idx] = sigmoid(x1, a, b, 0, 0.5)
    y[x_mid_idx] = sigmoid(x2, a, b, width / 2, -0.5)
    y[x_high_idx] = sigmoid(x3, a, b, width, -1.5)

    return y


def single_sigmoid(x, a, b, width):

    return sigmoid(x, a, b, width / 2, 0)


def sigmoid(x, a, b, c, d):
    """
        `a` scales curve along y
        `b` sharpness of S bend
        `c` displaces curve along x
        `d` displaces curve along y

    """

    e_arg = -b * (x - c)
    f = np.empty_like(e_arg)

    lo_idx = np.where(e_arg < -50)[0]
    hi_idx = np.where(e_arg < +50)[0]

    lim_lo_idx = e_arg < -50
    lim_hi_idx = e_arg > 50
    lim_idx = np.logical_or(lim_lo_idx, lim_hi_idx)
    not_lim_idx = np.logical_not(lim_idx)

    f[not_lim_idx] = 1 / (1 + np.exp(e_arg[not_lim_idx]))
    f[lim_lo_idx] = 1
    f[lim_hi_idx] = 0

    return a * (f - d)


def fit_quad(x, y):
    """
    Fit x and y data to a quadratic and get the minimum point

    Returns
    -------
    tuple
        poly1d, min_x, min_y

    """

    # Validation
    if len(x) != len(y):
        raise ValueError('x and y must have the same length')
    if len(x) < 3:
        raise ValueError('x and y must be of at least length 3.')

    z = np.polyfit(x, y, 2)
    p1d = np.poly1d(z)
    dpdx = np.polyder(p1d)
    min_x = -dpdx[0] / dpdx[1]
    min_y = p1d(min_x)

    return p1d, min_x, min_y


def linear(x, m=1, c=0):
    return m * x + c
