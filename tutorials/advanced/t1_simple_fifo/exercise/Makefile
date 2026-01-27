#Copyright 2024 Apheleia
#
#Description:
# Apheleia Verification Library (AVL) Example

# Makefile

# HDL source files
VERILOG_SOURCES      += ./rtl/simple_fifo.sv
VERILOG_INCLUDE_DIRS +=
COMPILE_ARGS         +=

# COCOTB_TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
COCOTB_TOPLEVEL      := simple_fifo
PYTHONPATH           := ./cocotb

# MODULE is the basename of the Python test file(s)
MODULE         ?= simple_fifo_tb

EXTRA_ARGS     += --trace --trace-structs

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

clean::
	rm -rf cocotb/__pycache__/
	rm -rf *.xml *.json *.csv *.yaml *.vcd *.png sim.log
