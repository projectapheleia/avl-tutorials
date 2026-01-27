# Copyright 2025 Apheleia
#
# Description:
# Apheleia attributes example

import avl
import cocotb
from cocotb.triggers import Timer, RisingEdge

# TODO : Create simple_fifo_item (extend avl.SequenceItem)

# TODO : Create simple_fifo_sequence (extend avl.Sequence)

# TODO : Create simple_fifo_driver (extend avl.Driver)

# TODO : Create simple_fifo_monitor (extend avl.Monitor)

# TODO : Create simple_fifo_agent (extend avl.Agent)

class simple_fifo_env(avl.Env):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.info("Creating simple_fifo_env:...")

        # TODO : Register HDL module

        # TODO : Create the agent


    async def run_phase(self):
        self.raise_objection()

        # TODO : Create a clock

        # TODO : Create a reset

        # TODO : Create a Timeout

        # TODO : Check reset

        # Run for a while
        await Timer(2, unit="us")

        self.drop_objection()

@cocotb.test
async def test(dut):

    # TODO : Register the hdl with the factory and configure

    env = simple_fifo_env("env", None)
    await env.start()
