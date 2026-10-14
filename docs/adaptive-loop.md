# The Adaptive Tutor Loop & Student Model

LearnForge AI's core differentiator is that it does not stop at answering document questions. It tracks how well the student understands each concept, diagnoses specific mental blocks, and changes its teaching strategy dynamically.

---

## 1. The Central 7-Stage Learning Loop

```
  [1. UNDERSTAND]  ---> Student asks question; Tutor responds with source citations.
         |
         v
    [2. TEST]      ---> System generates diagnostic check calibrated to student's level.
         |
         v
 [3. DETECT GAP]   ---> Student errors trigger misconception diagnosis (e.g. missing base cases).
         |
         v
   [4. ADAPT]      ---> Tutor switches strategy: delivers real-world analogy & step trace.
         |
         v
  [5. REASSESS]    ---> Student solves targeted micro-check to verify understanding.
         |
         v
[6. UPDATE MODEL]  ---> Mastery formula updates: 42% -> 67% (+25%).
         |
         v
 [7. RECOMMEND]    ---> System suggests what to study next based on prerequisite graph.
```

---

## 2. Explainable Student Mastery Formula

Rather than relying on opaque heuristics or black-box neural estimators, LearnForge AI uses a documented, explainable algorithm:

$$\text{mastery} = 0.50 \times \text{recent\_accuracy} + 0.30 \times \text{difficulty\_factor} + 0.20 \times \text{consistency}$$

### Factor Definitions:
1. **Recent Accuracy (50%)**:
   - The ratio of correct answers over total attempts ($\frac{\text{correct}}{\text{attempts}}$).
2. **Difficulty-Adjusted Factor (30%)**:
   - Scaled reward reflecting the highest tier attempted and validated:
     - `EASY`: $0.60$
     - `MEDIUM`: $0.85$
     - `HARD`: $1.00$
3. **Consistency Score (20%)**:
   - Retention indicator: $0.80$ if consecutive correct answers or steady performance, $0.30$ upon cognitive regression.

The result is clamped between $0.00$ and $1.00$ and expressed as a percentage ($42\%$).

---

## 3. Four Adaptive Teaching Strategies

When a student repeatedly struggles with a concept, repeating the same formal definition does not help. LearnForge AI switches between 4 distinct pedagogical strategies:

| Attempt | Strategy | Methodology | Recursion Example |
|---|---|---|---|
| **1** | **Technical & Algorithmic Mechanics** | Formal invariant, asymptotic complexity, call-stack allocation | "A recursive function calls smaller instances until base case unwinds activation records." |
| **2** | **Intuitive Analogy** | Relatable real-world mental model | "Russian Nesting Dolls (Matryoshka): Opening dolls until hitting the tiny solid doll inside." |
| **3** | **Step-by-Step Worked Trace** | Number-by-number execution tracing | "Trace factorial(4): 4 * fact(3) -> 3 * fact(2) -> 2 * fact(1) -> 1, then returns up: 2, 6, 24." |
| **4** | **Interactive Micro-Check** | Trace combined with immediate one-step question | "Given factorial(n), when n==1 evaluates, what value is returned to unstack?" |

---

## 4. Weak Concept Detection & Thresholds

- **Needs Practice / Weak Concept**: $\text{mastery} < 0.60$ (e.g. Recursion at $42\%$, Trees at $51\%$).
- **Competent Concept**: $0.60 \le \text{mastery} < 0.75$ (e.g. Sorting at $72\%$).
- **Strong Concept**: $\text{mastery} \ge 0.75$ (e.g. Binary Search at $85\%$, Arrays at $90\%$).

---

## 5. Explainable Recommendation Logic

The recommendation engine queries the curriculum dependency DAG:
- `Arrays` $\to$ `Binary Search`, `Sorting`, `Recursion`
- `Recursion` $\to$ `Trees`
- `Trees`, `Recursion` $\to$ `Graphs`

If a student attempts or approaches `Trees` while their prerequisite `Recursion` mastery is below $60\%$, the engine produces an explicit explanation:
> *"You should practice Recursion before advancing in Trees because your recursion mastery is currently 42%. Recursion is an essential prerequisite for tree traversal algorithms (DFS, Inorder, Preorder)."*
