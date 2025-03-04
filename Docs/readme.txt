# Possibilistic & Absurd Reasoning Inference System

This repository contains two inference systems developed during my **first year of Master's studies**:
1. **Possibilistic Inference System**: Uses **weighted knowledge bases** and possibilistic reasoning to evaluate certainty levels.
2. **Absurd Reasoning System**: Implements **proof by contradiction** (refutation-based inference) using a SAT solver.

## 📌 Overview
These systems process a knowledge base in **Conjunctive Normal Form (CNF)** and determine whether a given fact can be inferred.

### **Possibilistic Inference System**
- Uses **weighted knowledge bases** where each rule has a confidence level.
- Performs **inference using possibilistic logic**.
- Applies **binary search over confidence levels** to find the minimum certainty threshold.
- Supports **negation handling** for more precise reasoning.

### **Absurd Reasoning System**
- Implements **proof by contradiction**.
- Uses **UBCSAT** as a SAT solver.
- Adds the **negation of the target fact** to the knowledge base.
- If the solver detects an inconsistency, the fact is inferred as **logically true**.

## 📂 Repository Structure
```
/Inference-Systems
│── /possibilistic_reasoning  # Code for possibilistic inference
│── /absurd_reasoning         # Code for proof by contradiction
│── /UI                       # A simple UI in Tkinter (python)
│── /Data-Absurd              # Example knowledge bases (CNF format)
│── /Data-Proba-Inf           # Example knowledge bases for inference
│── /docs                     # Additional Documentation
│── README.md                 # Project overview
```

## ⚙️ Installation & Usage
### Prerequisites
Ensure you have **Python 3.x** and a SAT solver (**UBCSAT**) installed.

### Running the Possibilistic Inference System
```sh
python main.py RCR_BASE.txt target_variable
```

### Running the Absurd Reasoning System
```sh
python absurd_reasoning.py classic_BC/BC-Zoo2.cnf "2 0"
```

## 📜 License
This repository is for academic and research purposes. Feel free to explore and modify the code for learning.

---
📌 *For more details, check the documentation in the `/docs` folder.*
