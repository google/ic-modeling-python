# IC Modeling In Python

This library is set Python data models of common constructs used across various hardware description
languages like Spice, Verilog, VHDL, Verilog-AMS, and SystemVerilog.

This library isn't a tool in and of itself, but rather it is meant to serve as a foundation for
hardware language processing tools common in IC design.

## Potential use cases ##
* Create the Verilog code for a custom memory compiler.
* Read schematics and write out in SystemVerilog format.
* Generate a starting point of a design from spec documents.
* Write a script to read in a Verilog version of a design create a testbench for it.

## Non use cases ##

### Parsing ### 
This library will not include any language parsers as they are difficult to write and
often require a C/C++ tool chain to build, limiting portability.  There are several
open source parsers

### Simulation ###

The models here will eventually have constructs that map to procedural, behavioral 
hardware descriptions. For example, if/else blocks, case statements, always/initial blocks.

However, this library does not include a simulation engine, or a means to evaluate model behavior
to input stimulus.  It would, however, provide a good starting point for such a tool.