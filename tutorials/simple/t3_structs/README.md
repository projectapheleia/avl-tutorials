# Structs

Using the [structs documentation](https://avl-core.readthedocs.io/en/latest/variables/structs.html) and [z3 documentation](https://avl-core.readthedocs.io/en/latest/constraints/z3.html) as reference:

    0. Create an AVL representation of the structs in the rtl directory
        a. Variables must reset to 0

    1. Create a struct_t and assign to variable a
        a. Randomly change each variable on rising edge of clock (100 cycles)

    2. Re-using variable a
        a. Randomly change each variable on rising edge of clock (100 cycles)
        b. Constrain so state_enum == S0 -> multi_bit == 0
