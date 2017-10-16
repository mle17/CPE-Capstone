----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/16/2017 10:10:08 AM
-- Design Name: 
-- Module Name: PowerMod - Behavioral
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

entity PowerMod is
  Port (base   : in integer;
        exp    : in integer;
        modder : in integer;
        result : out integer);
end PowerMod;

architecture Behavioral of PowerMod is

begin

    process(base, exp, modder)
    
    variable A : integer;
    variable m : integer;
    variable t : integer;
    variable k : integer;
    variable r : integer;

    begin
        A := 1;
        m := exp;
        t := base;
        while m > 0 loop
            k := m/2;
            r := m - 2*k;
            if r = 1 then
                A := (A*t) mod modder;
            end if;
            t := (t*t) mod modder;
            m := k;
        end loop;
        result <= A;
    end process;   

end Behavioral;
