# Copyright 2025 Apheleia
#
# Description:
# Apheleia attributes example

import avl
import cocotb
from cocotb.triggers import Timer, RisingEdge
import random

class simple_fifo_item(avl.SequenceItem):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.value = avl.Logic(0, width=8, fmt=hex)

class simple_fifo_sequence(avl.Sequence):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.n_items = avl.Factory.get_variable(f"{self.get_full_name()}.n_items", 4)  # Default to 4 items

    async def body(self):
        sqr = self.get_sequencer()

        sqr.raise_objection()
        for _ in range(self.n_items):
            item = simple_fifo_item("item", self)
            await self.start_item(item)
            item.value.randomize()
            await self.finish_item(item)
        sqr.drop_objection()

class simple_fifo_driver(avl.Driver):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)
        self.wr_rate = avl.Factory.get_variable(f"{self.get_full_name()}.wr_rate", 100)
        self.rd_rate = avl.Factory.get_variable(f"{self.get_full_name()}.rd_rate", 100)

    async def reset(self):
        self.hdl.i_wr_en.value = 0
        self.hdl.i_wr_data.value = 0
        self.hdl.i_rd_en.value = 0

    async def pop(self):
        while True:
            self.hdl.i_rd_en.value = 0
            while random.randint(0, 100) > self.rd_rate:
                await RisingEdge(self.hdl.i_clk)
            self.hdl.i_rd_en.value = 1
            await RisingEdge(self.hdl.i_clk)

    async def push(self, item):
        while random.randint(0, 100) > self.wr_rate:
            await RisingEdge(self.hdl.i_clk)

        self.hdl.i_wr_en.value = 1
        self.hdl.i_wr_data.value = item.value.value
        while True:
            if bool(self.hdl.o_full.value):
                await RisingEdge(self.hdl.i_clk)
            else:
                break
        item.set_event("done")
        await RisingEdge(self.hdl.i_clk)
        self.hdl.i_wr_en.value = 0
        self.hdl.i_wr_data.value = 0

    async def run_phase(self):
        await self.reset()

        # Start pops in brackground
        cocotb.start_soon(self.pop())

        while True:
            item = await self.seq_item_port.blocking_get()
            while True:
                await RisingEdge(self.hdl.i_clk)
                if not bool(self.hdl.i_rst_n.value):
                    await self.reset()
                else:
                    break
            cocotb.start_soon(self.push(item))

class simple_fifo_monitor(avl.Monitor):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)

        # Build checks into monitor as so simple
        self.fifo = avl.Fifo(8)

    async def run_phase(self):
        while True:
            await RisingEdge(self.hdl.i_clk)

            if not bool(self.hdl.i_rst_n.value):
                self.fifo.clear()
                continue

            assert self.hdl.o_full.value == (len(self.fifo) == 8), "FIFO full signal mismatch"
            assert self.hdl.o_empty.value == (len(self.fifo) == 0), "FIFO empty signal mismatch"

            if bool(self.hdl.i_rd_en.value) and not bool(self.hdl.o_empty.value):
                assert self.fifo.pop(0) == self.hdl.o_rd_data.value

            if bool(self.hdl.i_wr_en.value) and not bool(self.hdl.o_full.value):
                self.fifo.append(self.hdl.i_wr_data.value)

class simple_fifo_agent(avl.Agent):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)

        # Create a driver
        self.driver = simple_fifo_driver("driver", self)

        # Create a monitor
        self.monitor = simple_fifo_monitor("monitor", self)

        # Create a sequencer
        self.sequencer = avl.Sequencer("sequencer", self) # No need to override

        # Create a sequence
        self.sequence = simple_fifo_sequence("sequence", self)

        # Connect the driver to the sequencer
        self.sequencer.seq_item_export.connect(self.driver.seq_item_port)

        # Assign sequencer to the sequencer
        self.sequence.set_sequencer(self.sequencer)

    async def run_phase(self):
        await self.sequence.start()

class simple_fifo_env(avl.Env):
    def __init__(self, name, parent):
        super().__init__(name, parent)

        # Register the HDL module
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)

        # Create an agents
        self.agent = simple_fifo_agent("agent", self)

    async def run_phase(self):
        self.raise_objection()

        # Create a clock
        cocotb.start_soon(self.clock(self.hdl.i_clk, freq_mHz=100))

        # Create a reset
        cocotb.start_soon(self.async_reset(self.hdl.i_rst_n, duration=100, units="ns", active_high=False))

        # Create a Timeout
        cocotb.start_soon(self.timeout(duration=1, units="ms"))

        # Check reset
        while True:
            await RisingEdge(self.hdl.i_clk)
            if self.hdl.i_rst_n.value == 1:
                break
        assert self.hdl.o_full.value == 0, "FIFO should be empty after reset"
        assert self.hdl.o_empty.value == 1, "FIFO should be empty after reset"

        # Run for a while
        await Timer(2, unit="us")

        self.drop_objection()

@cocotb.test
async def test(dut):
    # Register the hdl with the factory for easy access
    avl.Factory.set_variable("*.hdl", dut)
    avl.Factory.set_variable("*.n_items", 100)
    avl.Factory.set_variable("*.wr_rate", 50)
    avl.Factory.set_variable("*.rd_rate", 5)

    env = simple_fifo_env("env", None)
    await env.start()
