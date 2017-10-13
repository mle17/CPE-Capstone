----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/12/2017 07:56:43 PM
-- Design Name: 
-- Module Name: Exponent - Behavioral
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
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity Exponent is
  Port (power : in integer;
      base  : in integer;
      result : out integer);
end Exponent;

architecture Behavioral of Exponent is

    variable i : integer := 0;
    variable num : integer := 1;
    variable pow : integer := power;

begin

    process(base, pow)
        while i < pow loop
            num := num * base;
            i := i + 1;
        end loop;
    end process;
end Behavioral;
