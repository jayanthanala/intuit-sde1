1. High-Level Summary (30 seconds)

- Producer–Consumer with a bounded buffer

Synchronization using Condition (wait/notify)

deque for O(1) queue operations

Poison pill (None) for clean shutdown

Container classes are single-threaded → no locks needed

Full pytest suite with stress tests

2. Key Concepts & Why You Chose Them
Condition Variable

Enables waiting for a condition, not just locking

wait() releases lock → thread sleeps

notify_all() wakes blocked threads

Perfect for "wait while full / wait while empty"

Lock vs Semaphore vs Condition (short):

Lock → only mutual exclusion (can’t coordinate threads)

Semaphore → counting mechanism, but complex (needs 2 + a lock)

Condition → simplest & cleanest coordination
→ Perfect match for producer–consumer

Deque

O(1) push/pop

Full control over synchronization

queue.Queue hides locking → not allowed for this assignment

Poison Pill

Avoids stop flags & race conditions

Clean deterministic shutdown

Can scale to multi-consumer by sending N pills

3. Synchronization Flow (Short)
In put()

Acquire lock

While buffer full → wait()

Append item

notify_all()

Release lock

In get()

Acquire lock

While buffer empty → wait()

Pop item

notify_all()

Release lock

4. Why No Locks in Containers

SourceContainer → only used by Producer

DestinationContainer → only used by Consumer

Not shared → no synchronization needed

→ Only the shared buffer needs locking

5. Testing Strategy (Short)

Basic flow: items move 1 → N in order

Edge cases: buffer size 1, empty source

Poison pill verification

Stress test: random delays simulate real concurrency

Ensures no race conditions, no starvation

6. Common Interview Follow-Ups (and perfect answers)
Q: What if multiple producers/consumers?

Works fine. Just need one poison pill per consumer for shutdown.

Q: How to convert to async?

Use asyncio.Queue, replace threads with coroutines, replace wait/notify with await.

Q: notify vs notify_all?

notify wakes 1, notify_all wakes everyone. notify_all prevents waking the wrong type of thread.

Q: Where can deadlocks happen?

If wait conditions aren’t inside the while loop or if lock isn't released before waiting.

Q: Why is wait() inside a loop?

To protect against spurious wakeups or state changes while waking.

Q: What if notify happens before wait?

That’s okay — state already changed; the thread won’t wait when it checks the condition.

Q: Why not stop flags?

Flags cause stale reads and need locks → poison pill is cleaner and race-free.

7. Two Improvements (Must have ready)
Improvement #1 — Multi-producer/multi-consumer support

Add fairness

Add multiple poison pills

Improvement #2 — Observability

Add queue depth metrics

Add throughput and wait-time tracking

(Both show system-design maturity.)