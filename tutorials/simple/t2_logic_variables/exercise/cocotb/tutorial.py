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

        # Increment on rising edge of clock
        while True:
            # TODO : Wait on rising edge of clock and assign to hdl.a

            # TODO : Increment "a"

    async def task2_b(self):

        # TODO: Declare 32 bit variable "b"

        # Increment on falling edge of clock
        while True:
            # TODO : Wait on falling edge of clock and assign to hdl.b

            # TODO : Randomize "b"

    async def task3_c(self):

        # TODO: Declare 16 bit variable "c"

        # TODO : Add 1-hot constraint to "c"

        # Increment on rising edge of clock
        while True:
            # TODO : Wait on rising edge of clock and assign to hdl.c

            # TODO : Randomize "c"

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
