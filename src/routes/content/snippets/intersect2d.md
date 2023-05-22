---
title: "Tricking numpy to see rows as values for a fake intersect2d"
description: "Normally numpy's useful intersect1d only works on 1d arrays. This snippet shows how to trick numpy into seeing rows as values for a fake intersect2d."
date: "2023-05-21"
published: true
tags: 
    - python
    - numpy
---

<br>

Numpy has a function called `intersect1d` which is quite helpful for finding intersections of 
lists of indices. So, for example, if you have two vectors of booleans you might want to find the intersection between them. This function doesn't work when you have lists of n-d indices. This snippet shows how to trick numpy into seeing rows as values for a fake intersect2d.

### Credit: User Joe Kington [[StackOverflow]](https://stackoverflow.com/questions/8317022/get-intersecting-rows-across-two-2d-numpy-arrays)

```py
def intersect2d(a: np.ndarray, b: np.ndarray):
	if not (a.shape == b.shape):
		raise TypeError("a and b must have the same shape.")

	_, ncols = a.shape
	dtype = {
		'names': ['f{}'.format(i) for i in range(ncols)],
		'formats': ncols * [a.dtype]
		}
	return np.intersect1d(a.view(dtype), b.view(dtype))


A = np.array([[1,4],[2,5],[3,6]])
B = np.array([[1,4],[3,6],[7,8]])

print(intersect2d(A, B))
# [(1, 4) (3, 6)]
```
