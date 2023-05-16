---
layout: blog
title: "df across datapoints"
slug: "check"
author: "alex"
description: "A paper notes sum al. 2022. elephant"
subtitle: "something"
date: "2022-01-01"
published: true
tags: 
    - ml
    - paper
youtube: https://www.youtube.com/watch?v=zejXBg-2Vpk&list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM&index=7
link: https://arxiv.org/abs/2106.02584
github: https://github.com/OATML/Non-Parametric-Transformers
category: Note
---

# What are Docker and Singularity/Apptainer?

Note: this is a guide I made for a student I was TA'ing for, and I thought it might be useful to others. I tried to make it relatively comprehensive, but it is not meant to be a complete guide and the language is meant to not be really, really technical.

The main idea of these softwares, which are referred to as *containerization* softwares, is to encapsulate a programming environment in a single file.

What this means is that we are doing something generally analogous to a virtual environment in `Python`--but what Docker and Singularity (or Apptainer) allow users to do is encapsulate an entire computing environment. 

This includes the OS (so, Ubuntu or CentOS or even something like a custom OS) and *all* of the software. We can install a custom version of `Python`, or even several versions, and then all of a specific group of libraries. 
We can also install more complex libraries, like CUDA and GPU compute-related libraries, as well. 
What's even better about this is that we get all of this in one file that we can then pass around or send to someone else.
By sending someone a Docker or Singularity image--which are the individual files that encapsulate the computing environments, we can then let them
run an entire workflow that we've created, down to all of the specific libraries and versions that we used.

This is obviously highly useful for reproducible computing, but
can also help make your life easier by allowing you to perform the same computation on the same environment across different places.

## What is the difference between Docker and Singularity/Apptainer?

The original containerization software was Docker. It was used to facilitate workflows 
in more computer-science focused and particularly enterprise workflows, for example to allow a user
to create a cluster of similar compute environments (for example, to have all the same environment to produce some 
product recommendation or something else). Scientific computing users thought this might be useful,
but realized that there is a significant drawback of Docker--it requires root access to a given machine,
and particularly in the high performance computing clusters that we typically operate
on in academia, might allow a specific group of users to cause undesirable changes to a clusters' underlying environment. 

Singularity (originally developed by LBNL), which later became Apptainer (although a lot of people still use 
Singularity, and it is generally interoperable with Apptainer), are the standard for academic use. 

In particular, you cannot use Docker images on Wynton--but you can use Singularity. One issue is that
you cannot create Singularity images on Wynton (with some notable exceptions). 

# How do I use a Docker or Singularity image?

## How to use Docker 

### Pulling a Docker image from DockerHub

Let's assume for now we already have a Docker or Singularity (I'm just going to refer to them as Singularity images, but know that here we can use
Apptainer here as the term interchangably.) I will also assume you have already installed Docker, which can be done
fairly easily on an Ubuntu machine or on OS X--see the [installation guide](https://docs.docker.com/get-docker/).

Say, for example, we want to use a Docker image equipped with the CUDA libraries and PyTorch.

This is sort of a simple case that might be easy, maybe we want to use a specific CUDA version or something similar. 

Fortunately, many Docker images have already been created, and are uploaded to a central repository called the DockerHub ([https://hub.docker.com](https://hub.docker.com))
In fact, PyTorch itself distributes a group of relatively minimal Docker images with PyTorch installed on DockerHub: [https://hub.docker.com/r/pytorch/pytorch](https://hub.docker.com/r/pytorch/pytorch)

What we can do, then, is type in at the command line [see [here](https://hub.docker.com/r/pytorch/pytorch/tags) to see the specific versions of the images provided]:







NOTE: often Docker is set up to allow specific users to access it by invoking the `docker` command.
For other situations you may need to prepend `sudo` to the `docker` call--this is one of the reasons that 
HPC clusters prefer to use Singularity. For this document I will just save space by not prepending the `sudo` but note that you may need it in practice. 

When we do this, we get an output that looks like: 



