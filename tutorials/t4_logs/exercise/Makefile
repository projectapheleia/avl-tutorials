#Copyright 2026 Apheleia
#
#Description:
# Apheleia Verification Library (AVL) Tutorial

# Makefile

# HDL source files
VERILOG_SOURCES      += $(PWD)/rtl/hdl.sv
VERILOG_INCLUDE_DIRS +=
COMPILE_ARGS         +=

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL             := hdl
PYTHONPATH           := $(PWD)/cocotb

# MODULE is the basename of the Python test file(s)
MODULE               ?= tutorial

# Questa / ModelSim workaround
VSIM_ARGS            += -lib work

# Enable VCD trace from Verilator
ifeq ($(SIM), verilator)
EXTRA_ARGS           += --trace --trace-structs
endif

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

clean::
	rm -rf cocotb/__pycache__/
	rm -rf *.txt *.xml *.json *.csv *.yaml *.vcd *.png *.vhex *.vbin *.vmem *.ihex *.ti-txt *.srec sim.log html transcript modelsim.ini ucli.key
