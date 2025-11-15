// Planning Process

3 ways to solve this challange

1. Using a Queue (Blocking queue)
    - thread-safe
    - blocking queue
    - built in syncronization
    - internal locks + condition variables handled by Python
    - minimal risk of deadlocks

    - No low-level concurrecny
    - wait and notify not available/needed

2. Using Threads (manual wait/notify)
    Pros
    - hits the “Wait/Notify mechanism” objective DIRECTLY
    - shows deep understanding of concurrency primitives
    - great talking point during presentation

    Cons
    - more boilerplate
    - potential for subtle bugs
    - must manage buffer manually

3. Hybrid (1+2)