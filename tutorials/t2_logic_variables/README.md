# Logic Variables

Using the [variable documentation](https://avl-core.readthedocs.io/en/latest/variables/types.html) and [z3 documentation](https://avl-core.readthedocs.io/en/latest/constraints/z3.html) as reference:

    1. Create an 8 bit counter and assign to variable a
        a. Counter must reset to 0
        b. Counter must increment on rising edge of clock
        c. Counter must wrap at max

    2. Create a 32 bit random variable and assign to variable b
        a. Variable must reset to 0
        b. Variable must change to a random value on falling edge of clock

    3. Create a 16 bit 1-hot variable and assign to variable c
        a. Variable must reset to 0
        b. Variable must change to a 1-hot value on rising edge of clock
