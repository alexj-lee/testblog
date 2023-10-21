---
layout: blog
title: "What is representation learning in biology for?"
slug: "representationlearning"
author: "alex"
subtitle: "Unhelpful musings on ML in biology"
description: "What's the destination that computational biology is going towards?"
date: "2023-10-18"
published: true
tags: 
    - biology
category: blog
---

# What does representation learning in biology even mean?

In the last few years, there has been an explosion of interest in applications of machine learning in biology, particularly in (relatively) data-abundant subfields such as single-cell sequencing and protein/DNA sequencing data. Tools like transformers, graph neural networks, diffusion models, and other new and powerful techniques are entering the world of biology, and it's quite exciting! I myself in various fellowship and grant applications have written in a general way about the promise of computational biology when applied to unraveling the complexities of the rough and messy biological world. 

But I'll also admit that when it comes down to it, a lot of machine learning methods (my own included) seem to only perform marginally better than simpler statistical methods in many cases. And I think it's reasonable to say, and I also believe, that it's because in general in computational science (in academia) what we are really doing is overfitting to benchmarks or various contrived scenarios for paper publication and not for what is "useful" to biologists at the bench and to companies trying to develop new therapeutics and so on. 

When I think about what is "useful", however, I've realized I don't really know what useful means, and maybe the field doesn't either. When I read opinion pieces or grant applications I often see a reference to "data-driven science" or "hypothesis-free science" and in general I buy the idea specifically that if we had a ton of good data we could do *something* interesting. We could, for instance, gather a huge heaping pile of data and do what companies like [insitro](https://www.biorxiv.org/content/10.1101/2023.08.13.553051v1.full) and [Recursion](https://www.biorxiv.org/content/10.1101/2022.12.09.519400v1.full) are doing and create these "maps" of biology that we can use to understand interactions, structure, and ultimately create predictive perturbation models. I'm quite optimistic about these sorts of approaches in general. They are in some sense new (we have not had the ability to do this at large scale until now), but more importantly they have the potential to move us towards more general pictures of biological variation across the genome. Right now, I think something that makes it difficult to transfer inferences across subfields in biology is that every finding is conditioned on a huge number of specific details. Was this a study in immortalized cell lines, organoids, fibroblasts, iPSC, or did they use a combination of systems? What perturbations were used and how were they implemented? What phenotypic measurement technique was used? What were the working definitions of the various outcomes of the study? In general, I would hope that moving towards these large scale surveys has the potential to at least outline what is more general and what might be more specific, and to strucuture any future investigations on what makes up the differences. Certainly I think others would agree that the objective of projects where we generate a ton of data and analyze it is to find new hypotheses to test, and I think these approaches will do nothing if not generate new hypotheses. 

However when I talk to cynics and particularly people who have been in systems biology for longer, I can't really come up with an argument that really says these big data-driven approaches are going to be useful. I think the main argument is that we could use much simpler models (statistical or "good old fashioned machine learning") to do a lot of what we do, and insofar as the majority of what we do in computational biology is hypothesis generation, I think that's true. Certainly there are now many examples in the literature of how deep learning models only marginally outperform simple ones like linear regression for specific tasks. I realize that's not really fair to expect of the "representational learning" community, but I think it's a fair criticism of the field in general.

On the other side of this is also a criticism that I see folks like Konrad Kording bring up about neuroscience. We can only test so many hypotheses, and one way to see what we're doing in computational biology (and neuroscience) is generating a ton of hard-to-test ideas that haven't really helped us build towards specific theories of how these systems work. To say nothing of the huge amount of flawed methodologies and false-positive-generation-rituals we have in the field, I think it's fair to say that we have a lot of work to do to advance scientific understanding. 

I don't have any answers, and I mostly wrote this just to help myself understand what I find irritating about the state of the field and I suppose what I am really wondering is: what are we actually going to do with this data? This huge, huge amount of data? How **really** is it going to help us understand biology? 

