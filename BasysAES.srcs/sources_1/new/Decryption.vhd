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
        input  : in integer ;
        output : out integer);
end Decryption;

architecture Behavioral of Decryption is

    constant varD : integer := 449;
    constant varN : integer := 9797;  -- 5 * 3
    constant varR : integer := 9600;
    signal x : integer;
    
    component PowerMod is
    Port (base   : in integer;
          exp    : in integer;
          modder : in integer;
          result : out integer);
    end component;
    
begin

    PowerMod1 : PowerMod
    port map(base => input,
             exp => varD,
             modder => varN,
             result => x);

    process(clk, input, x)
    
    begin
        output <= x;
--        if(rising_edge(clk)) then
--            x <= input * input * input; -- raise to 3
--            output <= x mod 15;
--        end if;
    end process;   

end Behavioral;
