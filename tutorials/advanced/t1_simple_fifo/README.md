# Simple FIFO

* Phase 0

    1. Drive clock and reset signal
    2. Add a 1ms Timeout
    3. Confirm FIFO is empty after reset

* Phase 1

    1. Create UVM style environment
    2. Create random sequence
    3. Create monitor and checks

* Phase 2

    1. Add rate limiters to driver
    2. Increase number of items
