`default_nettype none

module test_core
#(
	
)
(
	input rst_i,
	input clk_i
);

always @(posedge clk_i or posedge rst_i) begin
	if (rst_i) begin
		
	end
	else begin
		
	end
end
endmodule