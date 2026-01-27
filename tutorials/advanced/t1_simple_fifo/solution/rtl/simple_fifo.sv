// Copyright 2025 ProjectApheleia
//
// Description:
// Simple fixed width FIFO
// Supports bypass and read/write on full
//

module simple_fifo #(
    parameter WIDTH = 8,       // Width of each data entry
    parameter DEPTH = 8        // Depth of the FIFO (number of entries)
)(
    input  logic              i_clk,        // Clock
    input  logic              i_rst_n,      // Active-low reset
    input  logic              i_wr_en,      // Write enable
    input  logic              i_rd_en,      // Read enable
    input  logic [WIDTH-1:0]  i_wr_data,    // Write data
    output logic [WIDTH-1:0]  o_rd_data,    // Read data
    output logic              o_full,       // FIFO full flag
    output logic              o_empty       // FIFO empty flag
);

    localparam ADDR_WIDTH = $clog2(DEPTH);  // Address width for FIFO depth
    typedef logic [ADDR_WIDTH-1:0] ptr_t;   // Pointer type
    typedef logic [WIDTH-1:0]      data_t;  // Data type
    typedef logic [ADDR_WIDTH:0]   count_t; // Counter type

    // Memory and pointers
    data_t                 mem [0:DEPTH-1];          // FIFO storage
    ptr_t                  wr_ptr, rd_ptr, inc_ptr;  // Write and read pointers
    count_t                fifo_count, inc_count;    // Counter to track number of elements

    // Increment pointer / count
    always_comb inc_ptr   = ptr_t'(1);
    always_comb inc_count = count_t'(1);

    // Status flags
    assign o_full  = (fifo_count == count_t'(DEPTH));
    assign o_empty = (fifo_count == count_t'(0));

    // FIFO write operation
    logic wr_valid;
    always_comb wr_valid = i_wr_en && !o_full;
    always_ff @(posedge i_clk or negedge i_rst_n) begin
        if (!i_rst_n) begin
            wr_ptr <= 0;
        end else if (wr_valid) begin
            mem[wr_ptr] <= i_wr_data;
            wr_ptr      <= wr_ptr + inc_ptr;
        end
    end

    // FIFO read operation without bypass logic
    logic rd_valid;
    always_comb rd_valid = i_rd_en && !o_empty;
    always_ff @(posedge i_clk or negedge i_rst_n) begin
        if (!i_rst_n) begin
            rd_ptr <= 0;
        end else if (rd_valid) begin
            rd_ptr <= rd_ptr + inc_ptr;
        end
    end

    // Read data output
    always_comb begin
        o_rd_data = mem[rd_ptr]; // Normal read from FIFO
    end

    // FIFO counter
    always_ff @(posedge i_clk or negedge i_rst_n) begin
        if (!i_rst_n) begin
            fifo_count <= 0;
        end else begin
            case ({wr_valid, rd_valid})
                2'b01:   fifo_count <= fifo_count - inc_count; // Read without write
                2'b10:   fifo_count <= fifo_count + inc_count; // Write without read
                2'b11:   fifo_count <= fifo_count;             // Read and write simultaneously (no count change)
                default: fifo_count <= fifo_count;             // No read/write
            endcase
        end
    end

endmodule : simple_fifo
