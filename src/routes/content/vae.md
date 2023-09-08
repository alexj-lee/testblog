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

<div class="overflow-scroll text-sm">

$$
\begin{align*}
& \mathrm{log}\ p(\mathbf{x}) &{} = &{}\ \mathrm{log} \int p(\mathbf{x}) \int q_\phi(\mathbf{z} \mid \mathbf{x}) \mathrm{d}\mathbf{z} && &{} \text{Multiply by}\ 1 \\ 
& &{} = &{} \int q_\phi (\mathbf{z} \mid \mathbf{x})\ \mathrm{log}\ p(\mathbf{x}) \mathrm{d} \mathbf{z} && &{} \text { Bring evidence in integral} \\ 
& &{} = &{}\  \mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\mathrm{log}\ p(\mathbf{x}) \right] && &{} \text { Definition of expectation} \\
& &{} = &{}\ \mathbb{E}_{q\phi (\mathbf{z} \mid \mathbf{x})} \left[\mathrm{log} \frac{p(\mathbf{x}, \mathbf{z})}{p(\mathbf{z} \mid \mathbf{x})} \right] && &{} \text { Chain rule of probability} \\
& &{} = &{}\ \mathbb{E}_{q\phi (\mathbf{z} \mid \mathbf{x})} \left[\mathrm{log} \frac{p(\mathbf{x}, \mathbf{z}) p_\phi (\mathbf{z} \mid \mathbf{x})}{p(\mathbf{z} \mid \mathbf{x}) q_\phi (\mathbf{z} \mid \mathbf{x})} \right] && &{} \text{} \\
& &{} = &{}\ \mathbb{E}_{q\phi (\mathbf{z} \mid \mathbf{x})} \left[\log \frac{p(\mathbf{x}, \mathbf{z})}{q_\phi (\mathbf{z} \mid \mathbf{x})} \right] +  && &{} \text{Split expectation using log rules} \\
& &{} &{} \quad \mathbb{E}_{q\phi (\mathbf{z} \mid \mathbf{x})} \left[\log \frac{q_\phi(\mathbf{z} \mid \mathbf{x})}{p (\mathbf{z} \mid \mathbf{x})} \right] \\
& &{} = &{}\ \mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\log \frac{p(\mathbf{x}, \mathbf{z})}{q_\phi (\mathbf{z} \mid \mathbf{x})} \right] + && &{} \text{Definition of KL divergence} \\
& &{} &{}\ \quad\mathcal{D}_{KL}(q_\phi (\mathbf{z} \mid \mathbf{x})\ \Vert\ p(\mathbf{z} \mid \mathbf{x})) \\
& &{} \geq &{}\ \mathbb{E}_{q\phi (\mathbf{z} \mid \mathbf{x})} \left[\log \frac{p(\mathbf{x}, \mathbf{z})}{q_\phi (\mathbf{z} \mid \mathbf{x})} \right] && &{} \text{KL is always greater than 0}
\end{align*}
$$

</div>

This is better than our previous formulation for several reasons:

- The evidence, $\mathrm{log}\ p(\mathbf{x})$, is always equal to the ELBO $\mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\log \frac{p(\mathbf{x}, \mathbf{z})}{q_\phi (\mathbf{z} \mid \mathbf{x})} \right]$ plus the KL divergence between the approximate posterior $q_\phi (\mathbf{z} \mid \mathbf{x})$ and the true posterior $p(\mathbf{z}) \mid \mathbf{x}$. In the first derivation, Jensen's inequality removed this term.
- The sort of theoretical strength of the of this framework is that we can easily see how we want to match the true posterior $p(\mathbf{z} \mid \mathbf{x})$ with our approximate, $q_\phi(\mathbf{z} \mid \mathbf{x})$ by matching their KL divergence.
- However, in practice we cannot access the true distribution--but by noticing that the evidence is constant with respect to $\phi$ (because we marginalize out all latents from the joint and so it does not really depend on the model itself, or the $\phi$'s), we can see that any maximization of the ELBO is a minimization of the KL divergence.

## Variational autoencoders

In the default formulation, VAEs maximize the ELBO according to the approach and ideas above. This is *variational* because we approximate for the best $q_\phi$ amongst a family of potential distributions parameterized by $\phi$. To see this, let's split the ELBO term into components to understand them:

<div class="text-sm overflow-scroll">

$$
\begin{aligned}
& \mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\log \frac{p(\mathbf{x}, \mathbf{z})}{q_\phi (\mathbf{z} \mid \mathbf{x})} \right] &{} = &{}\ \mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\log \frac{p_\theta(\mathbf{x} \mid \mathbf{z}) p(\mathbf{z})}{q_\phi (\mathbf{z} \mid \mathbf{x})} \right] && &{} \text{Chain rule} \\
& &{} = &{}\ \mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\log p_\theta (\mathbf{x} \mid \mathbf{z}) \right] + && &{} \\
& &{} &{} \quad \mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\log \frac{p(\mathbf{z})}{q_\phi (\mathbf{z} \mid \mathbf{x})} \right] && &{} \text{Split expectation} \\
& &{} = &{}\ \mathbb{E}_{q_\phi (\mathbf{z} \mid \mathbf{x})} \left[\log p_\theta (\mathbf{x} \mid \mathbf{z}) \right] - && &{} \\
& &{} &{} \quad \mathcal{D}_{KL}(q_\phi (\mathbf{z} \mid \mathbf{x})\ \Vert\ p(\mathbf{z})) && &{} \text{Definition of KL} 
\end{aligned}
$$

</div>

Where we can see the first term is basically a reconstruction (something implemented as MSE, maybe), and the second term is a prior matching term, which encourages the encoder to learn a distribution rather than collapsing into a delta function (on 0, or perhaps on the mean of the distribution).

Usually we chose a multivariate Gaussian for the prior, and a multivariate Gaussian with diagonal covariance for the latents.

<br>
