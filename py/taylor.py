import random
import sys
import util

import matplotlib.pyplot as plt
import numpy as np

from numpy.polynomial.polynomial import Polynomial

data = util.read_data()

# points = list(filter(
#     lambda point: 1.5 < point[0] < 2.4, 
#     zip(data['timestamp'], data['right_y'])
# ))

points = list(zip(data['timestamp'], data[sys.argv[1]]))

# split into x and y
xs = [point[0] for point in points]
ys = [point[1] for point in points]

# plot original data
plt.scatter(xs, ys, lineright_manualstyle='dashed', c='lightgray')

DEGREE = int(sys.argv[2])

data_domain = (min(xs), max(xs))
data_domain_size = data_domain[1] - data_domain[0]

data_range = (min(ys), max(ys))

def fit_for_bound(lower_bound, upper_bound, degree=None):
    plt.axvline(lower_bound, c='lightblue', linestyle='dotted')
    plt.axvline(upper_bound, c='lightblue', linestyle='dotted')

    # restrict domain to bounds
    domain = lambda point: lower_bound < point[0] < upper_bound
    subset = list(filter(domain, points))
    
    if len(subset) == 0:
        print('AHHHHHH')
        return

    s_xs = [point[0] for point in subset]
    s_ys = [point[1] for point in subset]

    # fit a polynomial
    poly = np.polyfit(s_xs, s_ys, degree or DEGREE)

    equation = str(Polynomial([round(c, 2) for c in poly])).replace("**", "^").replace(' x', 'x').replace('x^1 ', 'x ')
    plt.plot(xs, np.polyval(poly, xs), label=equation)

def division_partition(number):
    step_size = data_domain_size / number

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
            # if ((cur[1]-next[1]) < 0):
            #     continue
            peaks.append(cur[0])

    # deduplicate
    unique_peaks = []
    last_peak = 0
    for peak in peaks:
        if abs(last_peak - peak) > 0.1: # 0.25
            unique_peaks.append(peak)
        last_peak = peak

    for peak in unique_peaks:
        plt.axvline(peak, linestyle='dashed', c='pink')

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

# peaks_partition()
# division_partition(6)
# fit_for_bound(0.0, 0.89)
# fit_for_bound(0.89, 1.525)
fit_for_bound(1.6, 1.9, 2)
# fit_for_bound(1.8, 2.4)
fit_for_bound(1.9, 2.3, 3)

plt.legend()
plt.ylabel('Height (cm)')
plt.xlabel('Time (s)')
plt.title(f'Manually selected polynomial fit for vertical right foot displacement crest')
# plt.title('Bad fit for a quadratic')
plt.xlim(data_domain)
plt.ylim(data_range)
# plt.xlim([1.5, 2.5])
plt.show()