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

entity Decryption is
  Port (clk : in std_logic;
        input  : in integer;
        output : out integer);
end Decryption;

architecture Behavioral of Decryption is

    constant varE : integer := 9;
    constant varD : integer := 137;
    constant varN : integer := 667;
    constant varR : integer := 616;
    
    signal x : integer;

begin
    process(clk, input)
    begin
        if(rising_edge(clk)) then
            x <= input**varE;
            output <= x mod varN;
        end if;
    end process;   

end Behavioral;
