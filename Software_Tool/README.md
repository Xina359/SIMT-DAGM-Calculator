# SIMT Geometric Error Calculator
## Introduction
This software is the official companion tool for the research paper:
> [Analytical Modeling of Distance-Dependent Amplification of Residual Rotational Errors and a Distance-Adaptive Geometric Margin Strategy for Single-Isocenter Multi-Target SRS] > *Authors: [Jiaxin Deng, Guangyu Wang, et al.]*

This tool is designed to assist clinical physicists in:
1.  Planning Phase: Calculating the Distance-Adaptive Geometric Margin (DAGM) based on the Rayleigh distribution ($P_{95}$).
2.  Delivery Phase: Assessing the instantaneous Target Registration Error (TRE) during daily IGRT.


## Features 
* Bilingual Support: One-click switching between English and Chinese.
* Scientific Rigor: Implements the exact analytical models and statistical factors ($k=2.45$) derived in the paper.
* User-Friendly: Graphical User Interface (GUI) based on Python/Tkinter.

## How to Run 

### Option A: Using the Executable 
If you have downloaded the `.exe` file (Windows):
1.  Simply double-click `SIMT_Calculator.exe`.
2.  No Python installation is required.

### Option B: Running from Source Code 
If you prefer to run the Python script directly.

Prerequisites :
* Python 3.6 or higher
* Library: `numpy`, `tkinter` (usually built-in)

Installation:
```bash
pip install numpy