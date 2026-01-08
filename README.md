# Supplementary Code & Tools for SIMT-SRS Research


## Overview 
This repository contains the source code, software tools, and data visualization scripts associated with the research paper:

> Title: [Analytical Modeling of Distance-Dependent Amplification of Residual Rotational Errors and a Distance-Adaptive Geometric Margin Strategy for Single-Isocenter Multi-Target SRS]
> Authors: [Jiaxin Deng, Guangyu Wang, et al.]

The content is organized into two main parts:
1.  Clinical Tool: A standalone calculator for Distance-Adaptive Geometric Margins (DAGM).
2.  Figure Reproduction: Python scripts to reproduce the key figures and analytical plots presented in the manuscript.

---

## Part 1: SIMT Error Calculator 
Located in the folder: `./Software_Tool/`

A GUI-based tool to assist clinical physicists in determining safety margins and assessing daily IGRT errors.
* Run: Double-click `SIMT_Calculator.exe` (Windows) or run `python SIMT_Calculator.py`.
* Features: Bilingual support (CN/EN), DAGM calculation ($k=2.45$), and instant TRE assessment.

---

## Part 2: Figure Generation Codes 
Located in the folder: `./Figure_Generation/`

These scripts allow readers to reproduce the simulation results and figures shown in the paper.

### Prerequisites
You can install all necessary dependencies using:
```bash
pip install -r requirements.txt