# Copyright 2026 Apheleia
#
# Description:
# Apheleia Clock and Reset Tutorial


import avl
import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
import copy

class A(avl.Object):

    def __init__(self, name : str, parent : avl.Component) -> None:
        super().__init__(name, parent)

        # TODO: update to print as hex
        self.a = avl.Int32(0)

        # TODO: update to print as int (unless 0 - print "N/A")
        self.b = avl.Logic(0, width=4)

class Env(avl.Env):

    def __init__(self, name : str, parent : avl.Component) -> None:
        super().__init__(name, parent)

        # Get handle to hdl from the factory
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)

        # Create class A
        self.A = A("A", self)

        # TODO : Create Trace class

        # TODO : Create Port

        # TODO : Connect port to trace

    async def task1(self):

        # TODO : print as info - should be 0x0 and N/A

        self.A.a.value = 255
        self.A.b.value = 15
        # TODO : print as info - should be 0xf and 15

    async def task2(self):

        # TODO : Transpose

        # TODO : print as info - should be 0xf and 15 horizontally

    async def task3(self):

        for _ in range(100):
            await RisingEdge(self.hdl.clk)

            self.hdl.a.value = self.A.a.value
            self.hdl.b.value = self.A.b.value

            # TODO : Send to Trace

            # Randomize
            self.A.randomize()

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

        # Start task2
        await self.task2()

        # Start task3
        await self.task3()

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
