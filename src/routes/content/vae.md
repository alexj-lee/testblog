---
layout: blog
title: "Diffusion models"
slug: "vae"
author: "alex"
description: "Some paper notes on diffusion models"
subtitle: "something"
date: "2023-06-14"
published: false
tags: 
    - ml
    - paper
category: Note
---

# [Understanding Diffusion Models: A Unified Perspective](https://arxiv.org/abs/2208.11970)

## Background: VAEs, Hierarchical VAEs and the ELBO

A key concept in VAEs is the concept of the ELBO. Mathematically we want to represent our concepts and data with the joint distribution $p(\mathbf{x}, \mathbf{z})$. There are two routes to the marginal:

1. Explicit marginalization of $\mathbf{z}$: 
$$
\tag{eq-1} p(\mathbf{x}) = \int p(\mathbf{x}, \mathbf{z}) \mathrm{d}\mathbf{z}
$$ 
2. Chain rule of probability: $p(\mathbf{x}) = \frac{p(\mathbf{x}, \mathbf{z})}{p(\mathbf{z}\mid\mathbf{x})}$

Computing the likelihood $p(\mathbf{x})$ is hard, so we turn to the ELBO, or evidence lower bound as a proxy for the objective. Formally this is:


$$
\mathbb{E}_{q_\phi(\mathbf{z}\mid\mathbf{x})} \left[ \mathrm{log} \frac{p(\mathbf{x}, \mathbf{z})}{q_\phi(\mathbf{z}\mid\mathbf{x})} \right]
$$ 

which can be rearranged to:

$$
\mathrm{log}\ p(\mathbf{x}) \geq \mathbb{E}_{q_\phi(\mathbf{z}\mid\mathbf{x})} \left[ \mathrm{log} \frac{p(\mathbf{x}, \mathbf{z})}{q_\phi(\mathbf{z}\mid\mathbf{x})} \right]
$$

Here parameters of some model to approximate a variational distribution are $\phi$. Let's spell out what we are doing here a bit more:

Keep in mind for this (for me), the reason we can go from the integral to the expectation is because the definition of expectation is: $\mathbb{E} = \int \mathbf{x}f_\mathbf{x}\ \mathrm{d}\mathbf{x}$, and since we have set in this case that $q_\phi (\mathbf{z} \mid \mathbf{x})$ is the PDF of $\mathbf{z}$, then we have satisfied this condition; see also [LOTUS](https://en.wikipedia.org/wiki/Law_of_the_unconscious_statistician).

However this is more of a definition than an explanation. To better understand why this is actually a good thing to be modeling, let's dig in further: 

<div class="overflow-scroll">

$$
\begin{align*}
& \mathrm{log}\ p(\mathbf{x}) &{} = &{}\ \mathrm{log} \int p(\mathbf{x}) \int q_\phi(\mathbf{z} \mid \mathbf{x}) \mathrm{d}\mathbf{z} \\
& &{} = &{} \int q_\phi (\mathbf{z} \mid \mathbf{x})\ \mathrm{log}\ p(\mathbf{x}) \mathrm{d} \mathbf{z} \quad \text { (Bring evidence in integral) } \\ 
& &{} = &{}\  \mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\mathrm{log}\ p(\mathbf{x}) \right] \quad \text{ Definition of expectation} \\
\end{align*}
$$

$$
\begin{align*}
& \mathrm{log}\ p(\mathbf{x}) &{} = &{}\ \mathrm{log} \int p(\mathbf{x}) \int q_\phi(\mathbf{z} \mid \mathbf{x}) \mathrm{d}\mathbf{z} && &{} \text{Multiply by}\ 1 \\ 
& &{} = &{} \int q_\phi (\mathbf{z} \mid \mathbf{x})\ \mathrm{log}\ p(\mathbf{x}) \mathrm{d} \mathbf{z} && &{} \text { Bring evidence in integral} \\ 
& &{} = &{}\  \mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\mathrm{log}\ p(\mathbf{x}) \right] && &{} \text { Definition of expectation} 
\end{align*}
$$


</div>