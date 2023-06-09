---
title: "`matplotlib` reference"
description: "A reference sheet for matplotlib."
date: "2023-06-02"
published: true
tags: 
    - python
---

<br>

## Changing ticks and tick labels

### With axis object, change tick spacing
```py
from matplotlib import ticker
tick_spacing = 1
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

# or

ax.set_xticks(ax.getxticks()[::2]) 
# set xticks can also just be given a list or np array of tick locations
ax.set_xticklabels(ax.get_xticklabels()[::2])
# can also receive args like (..., fontsize=6, rotation=45), etc


# also
ax.set_xticklabels(ax.get_xticklabels()[::2])
```
# https://www.geeksforgeeks.org/change-the-x-or-y-ticks-of-a-matplotlib-figure/#

```fig, axs = plt.subplots(1)
axs.imshow(corrs)

axs.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
# axs.xaxis.set_major_locator(ticker.MultipleLocator(5))

yaxislabels = [item.get_text() for item in axs.get_yticklabels()]
#axs.set_yticklabels(list(range(1,6)))
a = np.array(axs.get_yticks().tolist())
a[1:] += 1 

axs.set_yticklabels(a.astype(int))

# a = np.array(axs.get_xticks().tolist())
# a[1:] += 1 

# axs.set_xticklabels(a.astype(int))

axs.xaxis.set_ticks([0] + (np.arange(0, len(corrs.T), 5)[1:]-1).tolist() + [43])
a = np.array(axs.get_xticks().tolist())
a[:] += 1 

axs.set_xticklabels(a.astype(int))
```

## Turn grid off
```py
ax.grid(False) # or None
```

## Change colorbar width
```py
# credit https://stackoverflow.com/questions/33443334/how-to-decrease-colorbar-width-in-matplotlib
fig.colorbar(c, aspect=5)

# or
cbar_ax = fig.add_axes([0.09, 0.06, 0.84, 0.02])
fig.colorbar(scatter, cax=cbar_ax, orientation="horizontal")
```

## Histogram clipping

```py
sns.distplot(data, hist=False, kde_kws={'clip': (0, 1)})
# or
sns.kdeplot(data, clip=(0.0, 1.0))

# not 100% sure if this actually recalculates the function or just clips the visualization limits
```



