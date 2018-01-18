# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 15:56:19 2018

@author: shan

A permutation test applied to a hypothetical website change.

Case:
    A website design company would like to know if changes made
    to a splash page will impact clickthrough on to further pages.
    Take 1000 visitors and redirect 500 each to
    Splash A-Original and Splash B-Redesign.

Results observed of clickthrough rates to further pages:
    A: 45
    B: 67

Null hypothesis:
    The click-through rate is not affected by the redesign.
"""

import numpy as np

# Construct arrays clickthrough_A, clickthrough_B for simulated data
total_visitors = 1000
test_group = total_visitors/2
successful_A = 45
successful_B = 67

clickthrough_A = np.array([True] * int(successful_A) +
                          [False] * int(test_group-successful_A))
clickthrough_B = np.array([True] * int(successful_B) +
                          [False] * int(test_group-successful_B))

# Set a seed for reproducible pseudo-random data
np.random.seed(42)


def permutation_sample(data1, data2):
    """
    Generate a permutation sample from two data sets.
    Params: data1, data2
    """

    data = np.concatenate((data1, data2))
    permuted_data = np.random.permutation(data)

    perm_sample_1 = permuted_data[:len(data1)]
    perm_sample_2 = permuted_data[len(data1):]

    return perm_sample_1, perm_sample_2


def draw_perm_reps(data_1, data_2, func, size=1):
    """
    Generate multiple permutation replicates.
    Params: data_1, data_2, func, size
    """

    perm_replicates = np.empty(size)

    for _ in range(size):
        perm_sample_1, perm_sample_2 = permutation_sample(data_1, data_2)
        perm_replicates[_] = func(perm_sample_1, perm_sample_2)

    return perm_replicates


def diff_frac(data_A, data_B):
    """
    Calculate the fractional difference of click through rates
    Params: data_A, data_B
    """

    frac_A = np.sum(data_A) / len(data_A)
    frac_B = np.sum(data_B) / len(data_B)

    return frac_B - frac_A


diff_frac_obs = diff_frac(clickthrough_A, clickthrough_B)

# Permutation test of click through rates

perm_replicates = np.empty(10000)

for _ in range(len(perm_replicates)):
    perm_replicates[_] = draw_perm_reps(
            clickthrough_A, clickthrough_B, diff_frac)

p_value = np.sum(perm_replicates >= diff_frac_obs) / len(perm_replicates)

print('p-value:', p_value)

"""
A p-value of 0.016 is calculated, making this statistically significant.
The null hypothesis can be rejected and shows that the redesign had impact.
"""
