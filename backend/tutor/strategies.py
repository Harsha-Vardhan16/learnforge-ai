from typing import Dict, Any, Optional

ADAPTIVE_STRATEGIES = {
    "technical": {
        "label": "Strategy 1: Technical & Algorithmic Mechanics",
        "description": "Rigorous definition, formal invariants, time/space complexity, and state flow."
    },
    "analogy": {
        "label": "Strategy 2: Intuitive Real-World Analogy",
        "description": "Relatable mental models, metaphors, and intuitive visual scenarios."
    },
    "worked_example": {
        "label": "Strategy 3: Step-by-Step Worked Trace",
        "description": "Concrete execution tracing through variable states step by step."
    },
    "interactive_micro": {
        "label": "Strategy 4: Worked Example + Micro-Check Question",
        "description": "Guided walkthrough followed immediately by a single diagnostic practice prompt."
    }
}

RECURSION_ADAPTATIONS = {
    "technical": {
        "title": "Formal Definition & The Call Stack",
        "content": (
            "**Formal Mechanism of Recursion**:\n"
            "A recursive function $f(n)$ decomposes a problem into one or more identical subproblems $f(n-1)$ "
            "until reaching an irreducible terminating condition known as the **base case**.\n\n"
            "Every function invocation pushes a new activation frame onto the process **Call Stack**, "
            "storing local variables, parameters, and return address. When the base case evaluates to `true`, "
            "the stack unwinds in Last-In-First-Out (LIFO) order, returning accumulated values back up the chain.\n\n"
            "**Critical Invariant**: Without a strictly guaranteed base case, or if the argument does not converge "
            "toward the base case, the stack allocation grows unbounded until memory is exhausted, throwing a `StackOverflowError`."
        )
    },
    "analogy": {
        "title": "Analogy: Russian Nesting Dolls (Matryoshka)",
        "content": (
            "💡 **Think of recursion like a set of Russian Nesting Dolls (Matryoshka)**:\n\n"
            "1. You hold a large wooden doll. You open it up, and inside is an almost identical doll, just one size smaller (this is your **recursive call**).\n"
            "2. You keep opening smaller and smaller dolls over and over again.\n"
            "3. Eventually, you reach the tiniest solid wooden doll in the very center. It cannot be opened anymore! That solid center doll is the **BASE CASE**.\n"
            "4. Only once you hit that solid doll can you start putting the lids back on each outer doll to finish (the stack unwinding).\n\n"
            "👉 *What would happen if there was no solid doll?* You would keep opening dolls forever until your table collapses under the weight. "
            "That's exactly what a Stack Overflow is!"
        )
    },
    "worked_example": {
        "title": "Worked Example: Tracing factorial(4) Step by Step",
        "content": (
            "Let's trace how the computer computes `factorial(4)` step by step:\n\n"
            "```python\n"
            "def factorial(n):\n"
            "    if n == 1:       # Base Case\n"
            "        return 1\n"
            "    return n * factorial(n - 1)  # Recursive Step\n"
            "```\n\n"
            "**Phase 1: Winding the Stack (Going Down)**\n"
            "- Call `factorial(4)`: Needs `4 * factorial(3)` → Wait!\n"
            "- Call `factorial(3)`: Needs `3 * factorial(2)` → Wait!\n"
            "- Call `factorial(2)`: Needs `2 * factorial(1)` → Wait!\n"
            "- Call `factorial(1)`: Reached Base Case! Returns `1` immediately!\n\n"
            "**Phase 2: Unwinding the Stack (Returning Up)**\n"
            "- `factorial(2)` receives 1: calculates `2 * 1 = 2`, returns 2.\n"
            "- `factorial(3)` receives 2: calculates `3 * 2 = 6`, returns 6.\n"
            "- `factorial(4)` receives 6: calculates `4 * 6 = 24`, returns 24."
        )
    },
    "interactive_micro": {
        "title": "Interactive Micro-Check: You Try factorial(3)",
        "content": (
            "Now that you saw `factorial(4) = 24`, test your mental trace on `factorial(3)`.\n\n"
            "When `factorial(3)` executes:\n"
            "1. It calls `factorial(2)` which calls `factorial(1)`.\n"
            "2. What is the value returned by the base case `factorial(1)`?"
        ),
        "mini_question": {
            "question": "In the function `factorial(n)`, when `n == 1` is evaluated, what value is returned to unstack?",
            "options": ["0", "1", "2", "None (Infinite loop)"],
            "correct_option": "1",
            "explanation": "At n == 1, the base condition triggers and returns 1 immediately, allowing the previous calls to multiply and resolve."
        }
    }
}

BINARY_SEARCH_ADAPTATIONS = {
    "technical": {
        "title": "Binary Search: Invariants and Logarithmic Convergence",
        "content": (
            "Binary Search maintains a search interval $[low, high]$ over a monotonically sorted array $A$. "
            "At each iteration, it computes $mid = \lfloor low + (high - low)/2 \rfloor$ and compares $A[mid]$ with target $T$. "
            "Because the array is sorted, comparing $T$ with $A[mid]$ eliminates exactly $\lceil (high - low)/2 \rceil$ candidates. "
            "The recurrence relation $T(n) = T(n/2) + O(1)$ yields asymptotic runtime complexity of $\mathcal{O}(\log n)$."
        )
    },
    "analogy": {
        "title": "Analogy: Searching a 1000-page Dictionary",
        "content": (
            "💡 **Imagine looking for the word 'Mango' in a huge 1000-page dictionary**:\n\n"
            "- Would you start at page 1 and flip one page at a time? No! That would take up to 1000 page flips (Linear Search).\n"
            "- Instead, you open the book right in the middle (page 500). Suppose you see words starting with 'M'. You compare: does 'Mango' come before or after?\n"
            "- In one second, you throw away 500 pages! You repeat on the remaining half.\n"
            "Within only **10 flips**, you can locate any word among 1,000 pages! That is Binary Search."
        )
    },
    "worked_example": {
        "title": "Worked Example: Finding 7 in [1, 3, 5, 7, 9, 11, 13]",
        "content": (
            "Given sorted array `[1, 3, 5, 7, 9, 11, 13]` and target `7`:\n\n"
            "- **Step 1**: `low = 0 (val 1)`, `high = 6 (val 13)`. `mid = (0+6)//2 = 3`. Element `arr[3]` is `7`.\n"
            "- Target `7 == 7`! Found on index `3` in exactly **1 step**.\n\n"
            "If searching for `11`:\n"
            "- Step 1: `arr[3] = 7 < 11` → discard left half! Set `low = 4`.\n"
            "- Step 2: `low = 4`, `high = 6`, `mid = 5`. `arr[5] = 11 == 11`! Found in 2 steps."
        )
    },
    "interactive_micro": {
        "title": "Micro-Check: Prerequisite for Binary Search",
        "content": "Consider applying Binary Search to find a student ID.",
        "mini_question": {
            "question": "What is the mandatory prerequisite condition for an array before Binary Search can be applied?",
            "options": ["The array elements must be sorted", "The array must contain only positive integers", "The array size must be a power of 2", "The array must have no duplicate elements"],
            "correct_option": "The array elements must be sorted",
            "explanation": "Binary Search relies on the sorting invariant to safely eliminate half of the remaining elements at each step."
        }
    }
}

def get_strategy_for_attempt(attempt_number: int) -> str:
    """
    Selects strategy based on student struggle depth:
    Attempt 1: technical
    Attempt 2: analogy
    Attempt 3: worked_example
    Attempt 4+: interactive_micro
    """
    if attempt_number <= 1:
        return "technical"
    elif attempt_number == 2:
        return "analogy"
    elif attempt_number == 3:
        return "worked_example"
    else:
        return "interactive_micro"

def get_adaptive_explanation(topic: str, strategy: str) -> Dict[str, Any]:
    """Retrieves curated adaptive content for topic and strategy."""
    topic_normalized = topic.strip().title()
    
    if "Recursion" in topic_normalized:
        content_dict = RECURSION_ADAPTATIONS.get(strategy, RECURSION_ADAPTATIONS["analogy"])
    elif "Binary Search" in topic_normalized:
        content_dict = BINARY_SEARCH_ADAPTATIONS.get(strategy, BINARY_SEARCH_ADAPTATIONS["analogy"])
    else:
        # Default adaptive structure
        content_dict = {
            "title": f"Adaptive Learning: {topic} ({strategy.replace('_', ' ').title()})",
            "content": f"Exploring {topic} using {strategy.replace('_', ' ')}. Break the concept down into its fundamental mechanics and trace an example.",
            "mini_question": None
        }

    info = ADAPTIVE_STRATEGIES.get(strategy, ADAPTIVE_STRATEGIES["analogy"])
    return {
        "strategy": strategy,
        "strategy_label": info["label"],
        "title": content_dict.get("title", f"{topic} Breakdown"),
        "content": content_dict.get("content", ""),
        "mini_question": content_dict.get("mini_question")
    }
