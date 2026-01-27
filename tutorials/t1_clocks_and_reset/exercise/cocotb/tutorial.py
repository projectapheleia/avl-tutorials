# Copyright 2026 Apheleia
#
# Description:
# Apheleia Clock and Reset Tutorial


import avl
import cocotb
from cocotb.triggers import Timer

class Env(avl.Env):
    def __init__(self, name : str, parent : avl.Component) -> None:
        super().__init__(name, parent)

        # Get handle to clock and reset from the factory
        self.clk = avl.Factory.get_variable(f"{self.get_full_name()}.clk", None)
        self.rst_n = avl.Factory.get_variable(f"{self.get_full_name()}.rst_n", None)

    async def run_phase(self):

        self.raise_objection()

        # TODO : Create clock

        # TODO : Create asynchronous, active low reset for 10ns

        # Wait 1 us
        await Timer(1, "us")

        self.drop_objection()

@cocotb.test
async def test(dut):

    # Set factory references to clock and reset
    avl.Factory.set_variable("*.clk", dut.clk)
    avl.Factory.set_variable("*.rst_n", dut.rst_n)

    # Create env
    e = Env("env", None)

    # Start the test
    await e.start()
