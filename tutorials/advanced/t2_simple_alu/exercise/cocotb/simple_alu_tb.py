# Copyright 2025 Apheleia
#
# Description:
# Apheleia attributes example

import avl
import avl.templates
import cocotb
from cocotb.triggers import Timer, RisingEdge
import random

class alu_item(avl.SequenceItem):

    # TODO : Create interesting values

    def __init__(self, name, parent_sequence):
        super().__init__(name, parent_sequence)

        # TODO : Add fields

        # TODO : Add constraints

        # TODO : Add some interesting values to a and b

class alu_driver(avl.templates.VanillaDriver):

    # TODO : Implement driver

    async def run_phase(self):
        pass

class alu_monitor(avl.templates.VanillaMonitor):

    # TODO : Implement monitor

    async def run_phase(self):
        pass

class alu_model(avl.templates.VanillaModel):

    # TODO : Implement model

    async def run_phase(self):
        pass

@cocotb.test
async def test(dut):
    # Create the environment
    avl.Factory.set_variable("*.hdl", dut)
    avl.Factory.set_variable("*.clk", dut.i_clk)
    avl.Factory.set_variable("*.rst", dut.i_rst_n)
    avl.Factory.set_variable("env.cfg.timeout_ns", 100000)
    avl.Factory.set_variable("*.n_items", 100)
    avl.Factory.set_override_by_type(avl.templates.VanillaDriver, alu_driver)
    avl.Factory.set_override_by_type(avl.templates.VanillaMonitor, alu_monitor)
    avl.Factory.set_override_by_type(avl.templates.VanillaModel, alu_model)
    avl.Factory.set_override_by_type(avl.SequenceItem, alu_item)

    e = avl.templates.VanillaEnv("env", None)

    # TODO : Add visualization

    await e.start()
