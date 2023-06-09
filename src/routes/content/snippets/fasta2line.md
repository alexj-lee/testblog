---
title: "n-seq per line to 1-seq per line"
description: "Convert a non-1-sequence per line FASTA to 1-seq-per-line."
date: "2023-06-09"
published: true
tags: 
    - python
---

# Credit Pierre Lindenbaum at [Biostars](https://www.biostars.org/p/9262/)

Often it's useful (for example, to use in a Dataloader in torch) to have a FASTA file where each sequence is on a single line. This snippet does that.

```bash
awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < file.fa

```