# Verilog Testbench 自动生成器

**代码介绍见[此](https://zhuanlan.zhihu.com/p/413868736)**

## 代码使用

直接使用命令：

```
python VerilogTestbenchGen.py <input file name> <output file name>
```

即可运行，其中`input file name`为待生成`Testbench`的模块的路径；`output file name`为生成结果的路径。

除此以外，进入源码`VerilogTestbenchGen.py`，还可以选择性地修改以下参数：

- **TESTBENCH_MODULE_NAME**：`Testbench`模块前缀名，默认为`test_`;
- **INST_MODULE_NAME**：`Testbench`中例化模块的前缀名，默认为`inst_`;

如接口名称过长(最终接口可能无法对齐)，还可适当增大以下值：

- **LINE_LENTH_1**：默认为`20`;
- **LINE_LENTH_2**：默认为`15`;
- **LINE_LENTH_3**：默认为`30`;

**注意，使用本代码对输入模块有一定要求:**

- `(`后不能出现字符；
- 模块结束的`);`需要单独成行；
- 不支持带参数的模块；

一个恰当的格式如下：

```v
module module_name(
    input  ...,
    output ...,
    input [15:0] ...,
    output [3:0] reg ...,
    ...
);
```

将模块以合适的格式放至正确的文件中后，运行代码，结果会出现在你指定路径的文件中.

## 测试样例及结果

运行仓库自带测试样例：

**待例化模块：**

```v
module AXI_Top(
    input           clk,
    input           rstn,
    //I-Cache
    input           i_rd_req,
    input  [2:0]    i_rd_type,
    input  [31:0]   i_rd_addr,
    output          i_rd_rdy,
    output          i_ret_valid,
    output          i_ret_last,
    output  [31:0]  i_ret_data,
    input           i_wr_req,
    input  [2:0]    i_wr_type,
    input  [31:0]   i_wr_addr,
    input  [3:0]    i_wr_wstrb,
    input  [127:0]  i_wr_data,
    output          i_wr_rdy,
    //D-Cache
    input           d_rd_req,
    input  [2:0]    d_rd_type,
    input  [31:0]   d_rd_addr,
    output          d_rd_rdy,
    output          d_ret_valid,
    output          d_ret_last,
    output  [31:0]  d_ret_data,
    input           d_wr_req,
    input  [2:0]    d_wr_type,
    input  [31:0]   d_wr_addr,
    input  [3:0]    d_wr_wstrb,
    input  [127:0]  d_wr_data,
    output          d_wr_rdy,
    //UART signal
    output          TxD,
    input           RxD,
    output          interrupt,
    //VGA signal
    output [11:0]   vrgb,
    output          hs,
    output          vs
);
```

**运行结果：**

```v
`timescale 1ns / 1ps 
/*------------------------------------------------
Testbench file made by VerilogTestbenchGen.py
------------------------------------------------*/


module test_AXI_Top();

reg                 clk;
reg                 rstn;
reg                 i_rd_req;
reg  [2:0]          i_rd_type;
reg  [31:0]         i_rd_addr;
wire                i_rd_rdy;
wire                i_ret_valid;
wire                i_ret_last;
wire [31:0]         i_ret_data;
reg                 i_wr_req;
reg  [2:0]          i_wr_type;
reg  [31:0]         i_wr_addr;
reg  [3:0]          i_wr_wstrb;
reg  [127:0]        i_wr_data;
wire                i_wr_rdy;
reg                 d_rd_req;
reg  [2:0]          d_rd_type;
reg  [31:0]         d_rd_addr;
wire                d_rd_rdy;
wire                d_ret_valid;
wire                d_ret_last;
wire [31:0]         d_ret_data;
reg                 d_wr_req;
reg  [2:0]          d_wr_type;
reg  [31:0]         d_wr_addr;
reg  [3:0]          d_wr_wstrb;
reg  [127:0]        d_wr_data;
wire                d_wr_rdy;
wire                TxD;
reg                 RxD;
wire                interrupt;
wire [11:0]         vrgb;
wire                hs;
wire                vs;


initial
begin
	clk           ='d0;
	rstn          ='d0;
	i_rd_req      ='d0;
	i_rd_type     ='d0;
	i_rd_addr     ='d0;
	i_wr_req      ='d0;
	i_wr_type     ='d0;
	i_wr_addr     ='d0;
	i_wr_wstrb    ='d0;
	i_wr_data     ='d0;
	d_rd_req      ='d0;
	d_rd_type     ='d0;
	d_rd_addr     ='d0;
	d_wr_req      ='d0;
	d_wr_type     ='d0;
	d_wr_addr     ='d0;
	d_wr_wstrb    ='d0;
	d_wr_data     ='d0;
	RxD           ='d0;
end


AXI_Top inst_AXI_Top
(
	.clk(clk),                   // input
	.rstn(rstn),                 // input
	.i_rd_req(i_rd_req),         // input
	.i_rd_type(i_rd_type),       // input [2:0]
	.i_rd_addr(i_rd_addr),       // input [31:0]
	.i_rd_rdy(i_rd_rdy),         // output
	.i_ret_valid(i_ret_valid),   // output
	.i_ret_last(i_ret_last),     // output
	.i_ret_data(i_ret_data),     // output [31:0]
	.i_wr_req(i_wr_req),         // input
	.i_wr_type(i_wr_type),       // input [2:0]
	.i_wr_addr(i_wr_addr),       // input [31:0]
	.i_wr_wstrb(i_wr_wstrb),     // input [3:0]
	.i_wr_data(i_wr_data),       // input [127:0]
	.i_wr_rdy(i_wr_rdy),         // output
	.d_rd_req(d_rd_req),         // input
	.d_rd_type(d_rd_type),       // input [2:0]
	.d_rd_addr(d_rd_addr),       // input [31:0]
	.d_rd_rdy(d_rd_rdy),         // output
	.d_ret_valid(d_ret_valid),   // output
	.d_ret_last(d_ret_last),     // output
	.d_ret_data(d_ret_data),     // output [31:0]
	.d_wr_req(d_wr_req),         // input
	.d_wr_type(d_wr_type),       // input [2:0]
	.d_wr_addr(d_wr_addr),       // input [31:0]
	.d_wr_wstrb(d_wr_wstrb),     // input [3:0]
	.d_wr_data(d_wr_data),       // input [127:0]
	.d_wr_rdy(d_wr_rdy),         // output
	.TxD(TxD),                   // output
	.RxD(RxD),                   // input
	.interrupt(interrupt),       // output
	.vrgb(vrgb),                 // output [11:0]
	.hs(hs),                     // output
	.vs(vs)                      // output
);

endmodule
```