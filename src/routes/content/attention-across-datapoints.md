---
layout: blog
title: "Attention across datapoints"
slug: "attention-across-datapoints"
author: "alex"
subtitle: "A new neural network architecture for tabular-ish data"
description: "A paper notes summary about Kossen et al. 2022."
date: "2022-07-31"
published: false
tags: 
    - ml
    - paper
youtube: https://www.youtube.com/watch?v=zejXBg-2Vpk&list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM&index=7
link: https://arxiv.org/abs/2106.02584
github: https://github.com/OATML/Non-Parametric-Transformers
category: Paper
---



<hr>
<span class="mb-0 pb-1"> Author abstract: </span>
<div class="dark:prose-invert prose max-w-3xl">
    <blockquote class=""> <span> We challenge a common assumption underlying most supervised deep learning:
    that a model makes a prediction depending only on its parameters and the features
    of a single input. To this end, we introduce a general-purpose deep learning
    architecture that takes as input the entire dataset instead of processing one datapoint
    at a time. Our approach uses self-attention to reason about relationships between
    datapoints explicitly, which can be seen as realizing non-parametric models using
    parametric attention mechanisms. However, unlike conventional non-parametric
    models, we let the model learn end-to-end from the data how to make use of other
    datapoints for prediction. Empirically, our models solve cross-datapoint lookup
    and complex reasoning tasks unsolvable by traditional deep learning models. We
    show highly competitive results on tabular data, early results on CIFAR-10, and
    give insight into how the model makes use of the interactions between points. </span> </blockquote>
</div>
<br>



# Introduction 

Supervised DL workflows often utilize some data: $\mathcal{D}_{train} = \{(x_1, y_1), ..., (x_n, y)\}$ to learn a function $f$ that maximizes $p(\mathbf{y}\ |\  \mathbf{x}; \theta)$.
    * these functions produce test-time predictions of the form $p(\mathbf{y}^*\ |\ \mathbf{x}^*; \theta)$ where there is no explicit link between $\mathcal{D}_{train}$ and $\theta$.  

<br>

This paper introduces an architecture called nonparametric transformers, or NPT, which the authors suggest have the following advantages:  

  * explict learning of interactions between datapoints using self-attention  
  * usage of non-parametric and parametric mechanisms.

  The hope is then to learn functions that can produce a test-time prediction of the form
  $p(\mathbf{y}^*\ |\ \mathbf{x}^*, \mathcal{D}_{train}; \theta)$, schematized in $(c)$ and $(d)$ below. 
  
<img class="object-center object-scale-down" src="/attention-across-datapoints/figure1.png">

## NPTs take entire datasets as input 

The general framework is this:

* We have, again, some $\mathcal{D}$, which we provide as the entire data matrix $\mathbf{X} \in \mathbb{R}^{n\ \mathrm{x}\ d}$. 
    * Columns of $\mathbf{x}$ are referred to as attributes $j$. For classic regression or classification, the paper refers to the target variable as $\mathbf{X}_{:,\ d}$, with other attributes $\{\mathbf{X}_{:,j}\ |\ j \neq d\}$ as input features.
    * The paper uses a similar framework as in masked language modeling. They introduce a masking matrix $\mathbf{M} \in \mathbb{R}^{n\ \mathrm{x}\ d}$ to specify masked elements of $\mathbf{X}$. 
    * The model is then trained to predict masked entries: $\mathbf{X}^{M} =\ \{\mathbf{X}_{i,j}\ |\ \mathbf{M}_{i,j}\}$.  
  
    
<br>

    
    The initial setting for the paper is that of single-target classification or regression, where the masking matrix $\mathbf{M}$ has 1 at every entry of the target column $\mathbf{X}_{:,\ d}$.

## Alternating self-attention over datapoint embeddings and datapoint attributes are the central operations in NPT

The interesting part of the method starts to really come out here. What we will do is compute an embedding for each column (feature) of $\mathbf{X}$. The reason for this is twofold:
    1. allow for the computation of a per-variable "mask" embedding
    2. allow for embedding of all features into an embedding space of the same dimension (so, if we set some embedding dimension $e$, we would encode all variables, both categorical and continuous, into $\mathbb{R}^e$)
        - to spell this out further, if we have a continuous variable $x_j$ then we would provide the model with a an $(n\ \mathrm{x}\ 2)$ matrix, with one column continuous-valued and the other an indicator variable for whether the data point is missing. To see this, note the `npt.Trainer` object in the `npt` codebase, specifically the `npt.Trainer.run_epoch` method, along with the `npt.model.NPTModel.in_embeddings` definition. 
        - if we had a categorical variable of cardinality 3, we would provide the model with a one-hot encoded vector of length 4 ("mask" and the three original categorical variables).

* Each data "batch" contains some number of datapoints that will be encoded as above, as well as a masking matrix that denotes a given "target" column or a different type of masked-learning procedure. 
    * the way the data is provided, for example, in the breast cancer dataset (569 observations, with 31 variables each [not counting the ID]):
      * a series of $(569\ \mathrm{x}\ d)$ matrices, with $d = 3$ if categorical (original cardinality is 2), or $d = 2$ if continuous. 
    * the code then embeds these into a latent dimension of dimension $e$.

### A small review of self-attention

* For a nice review of self-attention, see Lillian Weng's blog post about it: [Attention? Attention!](https://lilianweng.github.io/posts/2018-06-24-attention/) I think if I read and absorbed all of Lillian's blog posts maybe I would get out of grad school faster.
* To recap some of the terminology used in the paper here, multi-headed dot product attention is defined as:  

<br>

<div class="flex flex-col items-center justify-center">

$\mathrm{MHSelfAtt}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{concat}_h(\mathbf{O}_1, ..., \mathbf{O}_k)\mathbf{W}^O$, with:

$\mathbf{O}_j = \mathrm{Attention}(\mathbf{Q}\mathbf{W}_{j}^{Q}, \mathbf{K}\mathbf{W}_{j}^{K}, \mathbf{V}\mathbf{W}_{j}^V)$
</div>

<br>


* this paper also combines MHA with LayerNorm and skip connections, for:

<br>

<div class="flex flex-col items-center justify-center">

$\mathrm{Res}(H) = \mathbf{H}\mathbf{W}^\mathrm{res} + \mathrm{MHSelfAtt}(\mathrm{LN}(H))$

</div>

<br>

* where the residual branch incorporates a weight matrix $\mathbf{W}^\mathrm{res} \in \mathbb{R}^{h\ \mathrm{x}\ h}$. 

* the authors also use a second residual branch, parameterized by a row-wise feed forward network, finally producing:

<br>

<div class="flex items-center justify-center">

$\mathrm{MHSA}(\mathbf{H}) = \mathrm{Res}(\mathbf{H}) + \mathrm{rFF}(\mathrm{LN}(\mathrm{Res}(\mathbf{H}))) \in \mathbb{R}^{n\ \mathrm{x}\ h}$

</div>

### Modifications of attention to allow for attention between datapoints, and attention between attributes (features)

* the innovative advance in this paper is to come up with a way to modify MHSA to allow for explicit comparison across pairs of variables (ABA) and pairs of datapoints (ABD). 
* this part was a bit hard to follow at first, so please bear with me:

### Attention between Datapoints (ABD)

* The input to ABD is a reshaped layer output $\mathbf{H}^{(l)} \in \mathbb{R}^{n \mathrm{x}\ h}, h = d * e$
* MHSA is applied between datapoint representations, yielding:

<br>

<div class="flex justify-center items-center">

$\mathrm{ABD}(\mathbf{H}^{(l)}) = \mathrm{MHSA}(\mathbf{H}^{(l)}) = \mathbf{H}^{(l+1)} \in \mathbb{R}^{n\ \mathrm{x}\ h}$

</div>

<br>

* For example, in the first layer, we input $\mathbf{H}^{(0)} \in \mathbf{R}^{n\ \mathrm{x}\ d\ \mathrm{x}\ e}$, the linearly input embedding data. Then after ABD, the output is shaped back into $\mathbb{R}^{n\ \mathrm{x}\ d\ \mathrm{x}\ e}$ from $\mathbb{R}^{n\ \mathrm{x}\ h}$.
  * The rFF operation is an MLP that is applied separately to all datapoints ("row-wise")
* The sort of prototypical case that the authors pose would be ideal would be if through these operations, you could learn an optimal way to embed a given $\mathbf{Q}_i$ and $\mathbf{K}_i$ close together (or far away). There might be additional benefits to stacking these layers and using them to learn more complex interactions between pairs of datapoints. 

### Attention between Attributes (ABA)

* ABD is designed to facilitate comparisons between datapoints, given some features. ABA is designed to allow the model to refine a given datapoint's representation by attending to its own state. 
* Each row (datapoint) is indexed by $\mathbf{H}^{(l)}_i, i\ \in\{1, ..., n\}$, giving:

<br>

<div class="flex items-center justify-center">

$\mathrm{ABA}(\mathbf{H}_{i}^{(l)}) = \mathrm{MHSA}(\mathbf{H}_{i}^{(l)}) = \mathbf{H}^{(l+1)} \in \mathbb{R}^{1\ \mathrm{x}\ d\ \mathrm{x}\ e}$.

</div>

<br>


