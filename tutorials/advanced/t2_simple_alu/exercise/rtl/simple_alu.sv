// Copyright 2025 ProjectApheleia
//
// Description:
// Simple ALU
//

module simple_alu (
    input  logic        i_clk,
    input  logic        i_rst_n,
    input  logic [2:0]  i_opcode,
    input  logic [31:0] i_a,
    input  logic [31:0] i_b,
    output logic [31:0] o_c,
    output logic        o_carry
);

    logic [32:0] result_ext;

    always_comb begin
        result_ext = 33'b0;
        o_carry = 1'b0;
        o_c     = 32'b0;

        case (i_opcode)
            3'b000: begin // NOP
                o_c = 32'b0;
                o_carry = 1'b0;
            end
            3'b001: begin // ADD
                result_ext = {1'b0, i_a} + {1'b0, i_b};
                o_c = result_ext[31:0];
                o_carry = result_ext[32];
            end
            3'b010: begin // SUB
                result_ext = {1'b0, i_a} - {1'b0, i_b};
                o_c = result_ext[31:0];
                o_carry = result_ext[32];  // borrow flag if needed
            end
           3'b011: begin // AND
                o_c = i_a & i_b;
                o_carry = 0;
            end
            3'b100: begin // OR
                o_c = i_a | i_b;
                o_carry = 0;
            end
            3'b101: begin // XOR
                o_c = i_a ^ i_b;
                o_carry = 0;
            end
            3'b110: begin // COMP (a = b)
                o_c = (i_a == i_b) ? 32'd1 : 32'd0;
                o_carry = 0;
            end
            default: begin
                $fatal("Unknown opcode: %b", i_opcode);
            end
        endcase
    end

endmodule
