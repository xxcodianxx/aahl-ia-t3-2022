import random
import util

import matplotlib.pyplot as plt
import numpy as np

from numpy.polynomial.polynomial import Polynomial

data = util.read_data()

# points = list(filter(
#     lambda point: 1.5 < point[0] < 2.4, 
#     zip(data['timestamp'], data['right_y'])
# ))

points = list(zip(data['timestamp'], data['head_y']))

# split into x and y
xs = [point[0] for point in points]
ys = [point[1] for point in points]

# plot original data
plt.scatter(xs, ys, linestyle='dashed', c='lightgray')

DEGREE = 2
THRESHOLD_Y = 0.02 # head=0.02 right=0.1

data_domain = (min(xs), max(xs))
data_range = data_domain[1] - data_domain[0]

def fit_for_bound(lower_bound, upper_bound):
    # plt.axvline(lower_bound, c='lightgray')
    # plt.axvline(upper_bound, c='lightgray')

    # restrict domain to bounds
    domain = lambda point: lower_bound < point[0] < upper_bound
    subset = list(filter(domain, points))
    
    if len(subset) == 0:
        print('AHHHHHH')
        return

    s_xs = [point[0] for point in subset]
    s_ys = [point[1] for point in subset]

    # fit a quadratic
    poly = np.polyfit(s_xs, s_ys, DEGREE)

    equation = str(Polynomial([round(c, 2) for c in poly])).replace("**", "^")
    plt.plot(s_xs, np.polyval(poly, s_xs), label=equation)

def division_partition(number):
    step_size = data_range / number

    for n in range(number):
        # calculate lower and upper bound
        lower_bound = data_domain[0] + n * step_size
        upper_bound = lower_bound + step_size
        fit_for_bound(lower_bound, upper_bound)

def peaks_partition():
    peaks = []
    
    # first scan

    for i in range(len(points)):
        if i-1 < 0: continue
        if i+1 >= len(points): continue

        cur = points[i]
        last = points[i-1]
        next = points[i+1]

        if ((cur[1]-next[1]) > 0) == ((cur[1]-last[1]) > 0):
            peaks.append(cur[0])

    # deduplicate
    unique_peaks = []
    last_peak = 0
    for peak in peaks:
        if abs(last_peak - peak) > 0.1:
            unique_peaks.append(peak)
        last_peak = peak

    for peak in unique_peaks:
        plt.axvline(peak, linestyle='dashed', c='lightgray')

    sub = []
    for i in range(len(unique_peaks)):
        c = unique_peaks[i]

        if i-1 < 0:
            n = unique_peaks[i+1]
            sub.append((data_domain[0], (n+c)/2))
            continue
        else:
            l = unique_peaks[i-1]

        if i+1 >= len(unique_peaks):
            sub.append(((c+l)/2, data_domain[1]))
            continue
        else:
            n = unique_peaks[i+1]

        sub.append(((l+c)/2, (n+c)/2))

    for (low, high) in sub:
        fit_for_bound(low, high)

peaks_partition()
# division_partition(4)

plt.legend()
plt.ylabel('Height (cm)')
plt.xlabel('Time (s)')
plt.show()