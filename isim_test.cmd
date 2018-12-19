H:
cd H:\ProgramFiles\Xilinx\14.7\ISE_DS

call settings64.bat

C:

cd %1%

rm isim_output.txt

mips_tb_isim_beh.exe -tclbatch isim.tcl >> isim_output.txt
