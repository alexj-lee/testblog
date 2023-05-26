---
title: "Get top or bottom k elements from a numpy array"
description: "Using argpartition to extract the lowest or highest elements of an array."
date: "2023-05-25"
published: true
tags: 
    - python
    - numpy
---

<br>

Numpy has a function called `argpartition` which is quite helpful for finding the top or bottom k elements of an array. This snippet shows how to use it.

```py
import numpy as np
def get_extreme_k_elements(arr: np.ndarray, k: int, sort: bool = True, top: bool = True):
	"""
	Get the top or bottom k elements of an array.

	Parameters
	----------
	arr : np.ndarray
		The array to get the top or bottom k elements from.
	k : int 
		The number of elements to get.
	sort : bool, optional
		Whether to sort the elements. The default is True.
	top : bool, optional
		Whether to get the top or bottom k elements. The default is True.
	"""

	if k > len(arr):
		raise ValueError("k must be less than or equal to the length of arr.")
	if arr.ndim != 1:
		raise ValueError("arr must be 1d.")

	if top:
		# Get the indices of the top k elements.
		indices = np.argpartition(arr, -k)[-k:]

		if sort:
			# Sort the top k elements.
			indices = indices[np.argsort(arr[indices])][::-1]
	else:
		indices = np.argpartition(arr, k)[:k]
		if sort:
			indices = indices[np.argsort(arr[indices])]

	assert len(indices) == k

	return indices



	


	
```