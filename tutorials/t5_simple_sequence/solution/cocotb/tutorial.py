# Copyright 2026 Apheleia
#
# Description:
# Apheleia Clock and Reset Tutorial


import avl
import cocotb
from cocotb.triggers import Timer

class Item(avl.SequenceItem):

    def __init__(self, name : str, parent : avl.Component) -> None:
        super().__init__(name, parent)

        self.a = avl.Uint32(0, fmt=hex)

class Sequence(avl.Sequence):
    def __init__(self, name, parent):
        super().__init__(name, parent)

    async def body(self):
        for i in range(100):

            await Timer(10, "ns")

            # TODO : Generate and send item
            item = Item(f"item[{i}]", self)
            await self.start_item(item)
            item.randomize()
            await self.finish_item(item)

class Driver(avl.Driver):

    def __init__(self, name, parent):
        super().__init__(name, parent)

    async def run_phase(self):
        while True:

            # TODO : fetch the item
            item = await self.seq_item_port.blocking_get()

            # TODO: log the item
            self.info(item)

            # TODO : Mark item as done
            item.set_event("done")

class Env(avl.Env):

    def __init__(self, name : str, parent : avl.Component) -> None:
        super().__init__(name, parent)

        # Get handle to hdl from the factory
        self.hdl = avl.Factory.get_variable(f"{self.get_full_name()}.hdl", None)

        # TODO : Create the driver
        self.driver = Driver("driver", self)

        # TODO : Create the sequencer
        self.sequencer = avl.Sequencer("sequencer", self)

        # TODO : Connect sequencer and driver
        self.sequencer.seq_item_export.connect(self.driver.seq_item_port)

    async def run_phase(self):
        self.raise_objection()

        # TODO : Create the sequence
        seq = Sequence("sequence", self.sequencer)

        # TODO : Start the sequence
        await seq.start()

        self.drop_objection()

@cocotb.test
async def test(dut):

    # Create env
    e = Env("env", None)

    # Start the test
    await e.start()
