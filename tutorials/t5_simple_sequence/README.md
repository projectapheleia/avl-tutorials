# Simple Sequence

Using the [sequence documentation](https://avl-core.readthedocs.io/en/latest/methodology/sequences/sequence.html) as reference:

    1. Update and instantiate the Sequencer and Driver
        a. No need to customize the avl.Sequencer
        b. Update body of driver to
            - wait for item
            - print the item
            - mark as done

    2. Connect the sequencer and driver

    2. Update the class Sequence
        a. Randomly generate 100 items
