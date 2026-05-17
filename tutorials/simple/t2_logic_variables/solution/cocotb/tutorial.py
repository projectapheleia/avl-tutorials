# Copyright 2026 Apheleia
#
# Description:
# Apheleia Clock and Reset Tutorial


import avl
import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
import random
from z3 import *

class Env(avl.Env):
    def __init__(self, name : str, parent : avl.Component) -> None:
        super().__init__(name, parent)

        # Get handle to hdl from the factory
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)

    async def task1_a(self):

        # TODO: Declare 8 bit variable "a"
        self.a = avl.Logic(0, width=8)

        # Increment on rising edge of clock
        while True:
            # TODO : Wait on rising edge of clock and assign to hdl.a
            await RisingEdge(self.hdl.clk)
            self.hdl.a.value = self.a.value

            # TODO : Increment "a"
            self.a += 1

    async def task2_b(self):

        # TODO: Declare 32 bit variable "b"
        self.b = avl.Logic(0, width=32)

        # Increment on falling edge of clock
        while True:
            # TODO : Wait on falling edge of clock and assign to hdl.b
            await FallingEdge(self.hdl.clk)
            self.hdl.b.value = self.b.value

            # TODO : Randomize "b"
            self.b.randomize()

    async def task3_c(self):

        # TODO: Declare 16 bit variable "c"
        self.c = avl.Logic(0, width=16)

        # TODO : Add 1-hot constraint to "c"
        one_hot_values = [1 << i for i in range(16)]

        # Solution 1 : using random.choice
        #self.c.add_constraint("c_1_hot", lambda x: x == random.choice(one_hot_values), self.c)

        # Solution 2 : using z3.Or
        self.c.add_constraint("c_1_hot", lambda x: Or([x == val for val in one_hot_values]))

        # Increment on rising edge of clock
        while True:
            # TODO : Wait on rising edge of clock and assign to hdl.c
            await RisingEdge(self.hdl.clk)
            self.hdl.c.value = self.c.value

            # TODO : Randomize "c"
            self.c.randomize()

    async def run_phase(self):

        self.raise_objection()

        # Create clock
        cocotb.start_soon(self.clock(self.hdl.clk, 100))

        # Create asynchronous, active low reset for 10ns
        cocotb.start_soon(self.async_reset(self.hdl.rst_n, 10, active_high=False))

        # Wait for reset to complete
        while True:
            await RisingEdge(self.hdl.clk)
            if self.hdl.rst_n.value != 0:
                break

        # Start task1_a
        cocotb.start_soon(self.task1_a())

        # Start task2_b
        cocotb.start_soon(self.task2_b())

        # Start task3_c
        cocotb.start_soon(self.task3_c())

        # Wait 1 us
        await Timer(10, "us")

        self.drop_objection()

@cocotb.test
async def test(dut):

    # Set factory references to clock and reset
    avl.Factory.set_variable("*.hdl", dut)

    # Create env
    e = Env("env", None)

    # Start the test
    await e.start()
