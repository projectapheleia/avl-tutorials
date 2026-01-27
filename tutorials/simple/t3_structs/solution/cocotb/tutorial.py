# Copyright 2026 Apheleia
#
# Description:
# Apheleia Clock and Reset Tutorial


import avl
import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from z3 import *

# TODO : Create the struct_t
class struct_t(avl.Struct):
    multi_bit : avl.Uint32 = avl.Uint32(0)
    state_enum : avl.Enum = avl.Enum("S0", {"S0" : 0, "S1" : 1, "S2" : 2})

class Env(avl.Env):
    def __init__(self, name : str, parent : avl.Component) -> None:
        super().__init__(name, parent)

        # Get handle to hdl from the factory
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)

        # TODO: Declare struct "a"
        self.a = struct_t()

    async def task1(self):

        # Randomize on rising edge of clock
        for _ in range(100):

            # TODO : Wait on rising edge of clock and assign to hdl.a
            await RisingEdge(self.hdl.clk)
            self.hdl.a.value = self.a.value

            # TODO : Randomize
            self.a.multi_bit.randomize()
            self.a.state_enum.randomize()

    async def task2(self):

        # TODO : Add constraint a.state_enum == S0 -> a.multi_bit == 0
        self.add_constraint("c", lambda x,y : Implies(x == self.a.state_enum.S0, y == 0), self.a.state_enum, self.a.multi_bit)

        # Randomize on rising edge of clock
        for _ in range(100):

            # TODO : Wait on rising edge of clock and assign to hdl.a
            await RisingEdge(self.hdl.clk)
            self.hdl.a.value = self.a.value

            # TODO : Randomize
            self.randomize()

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

        # Start task1
        await self.task1()

        # Wait 1 us
        await Timer(1, "us")

        # Start task2
        await self.task2()

        # Wait 1 us
        await Timer(1, "us")

        self.drop_objection()

@cocotb.test
async def test(dut):

    # Set factory references to clock and reset
    avl.Factory.set_variable("*.hdl", dut)

    # Create env
    e = Env("env", None)

    # Start the test
    await e.start()
