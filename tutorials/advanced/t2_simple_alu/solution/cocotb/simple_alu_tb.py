# Copyright 2025 Apheleia
#
# Description:
# Apheleia attributes example

import avl
import avl.templates
import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
import random

class alu_item(avl.SequenceItem):

    interesting_values = [0x000000000, 0x00000001, 0xFFFFFFFE, 0xFFFFFFFF, 0x55555555, 0xaaaaaaaa]
    for i in range(32):
        interesting_values.append(1 << i)
        interesting_values.append(~(1 << i))
    interesting_values = list(set(interesting_values))  # Remove duplicates


    def __init__(self, name, parent_sequence):
        super().__init__(name, parent_sequence)
        self.set_field_attributes("name", compare=False)

        self.opcode = avl.Enum("NOP", {"NOP" : 0, "ADD" : 1, "SUB" : 2, "AND" : 3, "OR" : 4, "XOR" : 5, "COMP" : 6, "ILLEGAL" : 7})
        self.a      = avl.Uint32(0, fmt=hex)
        self.b      = avl.Uint32(0, fmt=hex)
        self.c      = avl.Uint32(0, fmt=hex)
        self.carry  = avl.Bool(False)

        # Add constraints
        self.add_constraint("c_no_illegal", lambda x : x != self.opcode.ILLEGAL, self.opcode)

        # Add some interesting values to a and b
        interesting_values = [self.a.get_min(), self.a.get_min()+1, self.a.get_max()-1, self.a.get_max()]
        interesting_values.extend([1 << i for i in range(32)])
        interesting_values.extend([~(1 << i) for i in range(32)])
        weights = [1] * len(interesting_values)
        self.add_constraint("c_a", lambda x,y : x == random.choices(interesting_values + [y],
                                                                    weights=weights + [100])[0],
                                                                    self.a, random.randint(self.a.get_min(), self.a.get_max()))
        self.add_constraint("c_b", lambda x,y : x == random.choices(interesting_values + [y],
                                                                    weights=weights + [100])[0], self.b,
                                                                    random.randint(self.b.get_min(), self.b.get_max()))


class alu_driver(avl.templates.VanillaDriver):
    async def clear(self):
        self.hdl.i_a.value = 0
        self.hdl.i_b.value = 0
        self.hdl.i_opcode.value = 0

    async def reset(self):
        await self.clear()
        while True:
            await FallingEdge(self.rst)
            await self.clear()

    async def run_phase(self):
        cocotb.start_soon(self.reset())

        while True:
            item = await self.seq_item_port.blocking_get()
            while True:
                await RisingEdge(self.clk)
                if bool(self.rst.value):
                    break

            self.hdl.i_opcode.value = int(item.opcode)
            self.hdl.i_a.value = int(item.a)
            self.hdl.i_b.value = int(item.b)
            item.set_event("done")

    async def report_phase(self):
        self.raise_objection()
        for _ in range(10):
            await RisingEdge(self.clk)
            await self.clear()
        self.drop_objection()

class alu_monitor(avl.templates.VanillaMonitor):

    async def run_phase(self):
        while True:
            await RisingEdge(self.clk)

            if self.rst.value == 0:
                continue

            item = alu_item("monitor_item", None)
            item.opcode.value = int(self.hdl.i_opcode.value)
            item.a.value      = int(self.hdl.i_a.value)
            item.b.value      = int(self.hdl.i_b.value)
            item.c.value      = int(self.hdl.o_c.value)
            item.carry.value  = bool(self.hdl.o_carry.value == 1)

            # Write to the item export
            self.item_export.write(item)

class alu_model(avl.templates.VanillaModel):

    def __init__(self, name, parent_env):
        super().__init__(name, parent_env)

        # Coverage
        self.item = alu_item("coverage_item", None)

        self.cg        = avl.Covergroup("alu_cg", self)

        # Cover all opcodes
        self.cp_opcode = self.cg.add_coverpoint("opcode", lambda: self.item.opcode)
        for k,v in self.item.opcode.values.items():
            self.cp_opcode.add_bin(k, v, illegal=(k=="ILLEGAL"))

        # Cover all interesting values for a and b
        self.cp_a = self.cg.add_coverpoint("a", lambda: self.item.a)
        self.cp_b = self.cg.add_coverpoint("b", lambda: self.item.b)
        for v in alu_item.interesting_values:
            self.cp_a.add_bin(f'{v}', v)
            self.cp_b.add_bin(f'{v}', v)

        # Cover the carry result
        self.cp_carry = self.cg.add_coverpoint("carry", lambda: self.item.carry)
        for t in (True, False):
            self.cp_carry.add_bin(f'{t}', t)

        # Cross coverage carry X opcode
        self.cc = self.cg.add_covercross("carry_X_opcode", self.cp_carry, self.cp_opcode)
        # Remove opcodes which can't generate a carry
        rbins = []
        for k,v in self.cc._bins_.items():
            if k.startswith("True") and not (k.endswith("ADD") or k.endswith("SUB")):
                rbins.append(k)
        for k in rbins:
            self.cc.remove_bin(k)

    async def report_phase(self):
        print(self.cg.report(full=False))

    async def run_phase(self):
        self.info("Running ALU model...")
        while True:
            orig = await self.item_port.blocking_get()
            item = alu_item("model_item", None)
            item.opcode.value  = orig.opcode.value
            item.a.value = orig.a.value
            item.b.value = orig.b.value

            if item.opcode == item.opcode.NOP:
                c = avl.Logic(0, fmt=hex, auto_random=False, width=33)
            elif item.opcode == item.opcode.ADD:
                c = avl.Logic((item.a.value + item.b.value), fmt=hex, auto_random=False, width=33)
            elif item.opcode == item.opcode.SUB:
                c = avl.Logic((item.a.value - item.b.value), fmt=hex, auto_random=False, width=33)
            elif item.opcode == item.opcode.AND:
                c = avl.Logic((item.a.value & item.b.value), fmt=hex, auto_random=False, width=33)
            elif item.opcode == item.opcode.OR:
                c = avl.Logic((item.a.value | item.b.value), fmt=hex, auto_random=False, width=33)
            elif item.opcode == item.opcode.XOR:
                c = avl.Logic((item.a.value ^ item.b.value), fmt=hex, auto_random=False, width=33)
            elif item.opcode == item.opcode.COMP:
                c = avl.Logic((item.a.value == item.b.value), fmt=hex, auto_random=False, width=33)
            else:
                raise ValueError("Illegal opcode")

            item.c     = avl.Uint32(c)
            item.carry = avl.Bool((c >> 32))
            self.cg.sample()
            self.item_export.write(item)

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
    print(avl.Visualization.tree(e))
    avl.Visualization.diagram(e)

    await e.start()
