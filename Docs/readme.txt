# Possibilistic Inference System

This repository contains a **possibilistic inference system** developed during my **first year of Master's studies**. The system is designed to perform **reasoning with weighted knowledge bases** using **CNF (Conjunctive Normal Form) transformations** and a **SAT solver** for inference.

## 📌 Overview
The goal of this project is to evaluate the **certainty level** of an inferred fact based on a weighted knowledge base. The system processes a list of logical rules, sorts them by confidence levels, and applies **possibilistic reasoning** to determine the strongest inference.

## 🔍 Key Features
- **Processes weighted knowledge bases** from a text file.
- **Transforms logical formulas into CNF format**.
- **Uses a SAT solver** to check logical consistency.
- **Implements possibilistic inference** to determine the certainty of a conclusion.
- **Handles negation** and performs binary search on strata (confidence levels).


## ⚙️ Installation & Usage
### Prerequisites
Ensure you have **Python 3.x** installed along with the required dependencies.

### Running the Inference System
To execute the system on a knowledge base file:
```sh
python main.py RCR_BASE.txt target_variable
```

## 📜 License
This repository is for academic and research purposes. Feel free to explore and modify the code for learning.

---
📌 *For more details, check the documentation in the `/docs` folder.*
