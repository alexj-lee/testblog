---
title: "Sort rows of matrix for visualization"
description: "Sort the position of rows by their largets magnitude element."
date: "2023-06-09"
published: true
tags: 
    - bash
	- fasta
---

<br>

```py
import numpy as np
from scipy import optimize
def sort_matrix(matrix: np.ndarray, maximize: bool = False) -> np.ndarray:
	"""
	Sort the rows of a matrix by the position of their largest magnitude element.

	Parameters
	----------
	matrix : np.ndarray
		The matrix to sort.
	reverse : bool, optional
		Whether to sort in reverse. The default is False.
	"""

	if matrix.ndim != 2:
		raise ValueError("Matrix must be 2d.")

	nrow, ncol = matrix.shape

	row, col = optimize.linear_sum_assignment(matrix, maximize=maximize)

	sorted_rowcol = sorted(list(zip(row, col)), key=lambda el: matrix[el[0], el[1]], reverse=True)

	row = [el[0] for el in sorted_rowcol]
	col = [el[1] for el in sorted_rowcol]
	# assume nrows > ncol
	col_list = col
	for idx in range(max(matrix.shape)):
		if idx not in col_list:
			col_list.extend([idx])

	sort1 = matrix[np.array(row), :]
	sort2 = sort1[:, np.array(col_list)]

	# Get the indices of the largest magnitude element in each row.
	return sort2

```