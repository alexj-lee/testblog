---
layout: presentation
title: "The Dayhoff Atlas: scaling sequence diversity for improved protein generation"
slug: "ml4pe-dayhoff"
author: "alex"
subtitle: "Invited talk at ML for Protein Engineering (ML4PE)"
description: "My invited talk at the ML4PE seminar series on the Dayhoff Atlas and synthetic data augmentation for protein language models"
date: "2025-10-07"
published: false
tags:
    - ml
    - protein
    - paper
category: Presentation
youtube: "https://www.youtube.com/watch?v=ke8IJIOtV_Y"
link: "https://doi.org/10.1101/2025.07.21.665991"
github: "https://github.com/microsoft/Dayhoff"
huggingface: "https://huggingface.co/datasets/microsoft/Dayhoff"
---

I was invited to give a talk at the [ML for Protein Engineering (ML4PE)](https://www.ml4proteinengineering.com/) seminar series on our work on the Dayhoff Atlas. This was a really fun talk to give -- it's a great community and I got some good questions from the audience.

The talk covers the main ideas behind the [Dayhoff Atlas](https://doi.org/10.1101/2025.07.21.665991), which started as my internship project at Microsoft Research New England in the BioML group (with [Ava Amini](https://www.microsoft.com/en-us/research/people/avapm/) and [Kevin Yang](https://www.microsoft.com/en-us/research/people/kevinyang/)). The core question was: can we use synthetic protein data to improve protein language models, and does that improvement translate to real wet-lab results?

The answer turned out to be yes. We created BackboneRef, a large-scale synthetic protein dataset (240,811 de novo designed backbones, 73M sequences) using a pipeline of RFDiffusion, ProteinMPNN, OmegaFold, and Foldseek. Training protein language models with this synthetic data augmentation led to an 87.5% increase in expression success rate and 50% increase in novelty of de novo designed proteins compared to baseline.

The paper is currently in revision at Cell Systems.

You can watch the full recording here: [YouTube](https://www.youtube.com/watch?v=ke8IJIOtV_Y).
