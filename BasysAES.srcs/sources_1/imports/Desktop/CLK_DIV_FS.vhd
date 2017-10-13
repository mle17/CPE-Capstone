----------------------------------------------------------------------------------
-- Company: Ratner Engineering
-- Engineer: bryan mealy
-- 
-- Create Date:    15:27:40 12/27/2010 
-- Design Name: 
-- Module Name:    clk_div.vhd
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: This divides the input clock frequency into a slower
--              frequency. The frequency is set by the the MAX_COUNT
--              constant in the declarative region of the architecture. 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
--------------------------------------------------------------------------------

-----------------------------------------------------------------------
-----------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
-----------------------------------------------------------------------
-- Module to divide the clock 
-----------------------------------------------------------------------
entity CLK_DIV_FS is
    Port (  clk : in std_logic;
           sclk : out std_logic);
end CLK_DIV_FS;


architecture my_clk_div1 of CLK_DIV_FS is
   -- new clock = original clock * 1 / (max_count + 1)
   constant max_count : integer := (49999999);  
   signal tmp_clk : std_logic := '0'; 
begin
   my_div: process (clk,tmp_clk)              
      variable div_cnt : integer := 0;   
   begin
      if (rising_edge(clk)) then   
         if (div_cnt = MAX_COUNT) then 
            tmp_clk <= not tmp_clk; 
            div_cnt := 0; 
         else
            div_cnt := div_cnt + 1; 
         end if; 
      end if; 
      sclk <= tmp_clk; 
   end process my_div; 
end my_clk_div1;
