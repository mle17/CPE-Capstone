----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/04/2017 02:40:56 PM
-- Design Name: 
-- Module Name: Encryption - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.NUMERIC_STD.ALL;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.math_real.all;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity Encryption is
  Port (clk : in std_logic;
        input  : in integer;
        output : out integer);
end Encryption;

architecture Behavioral of Encryption is

    constant varD : integer := 3;
    constant varN : integer := 15;  -- 5 * 3
    constant varR : integer := 8;
    
    signal x : integer;

begin

    process(clk, input, x)
    begin
        if(rising_edge(clk)) then
            x <= input * input * input; -- raise to 3
            output <= x mod 15;
        end if;
    end process;   

end Behavioral;
