----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/02/2017 09:29:51 AM
-- Design Name: 
-- Module Name: main - Behavioral
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

entity main is
    Port (
        CLK_IN      : in std_logic;
        button      : in std_logic;
        correct_en  : out std_logic;
        correct_de  : out std_logic
    );
end main;

architecture Behavioral of main is

    constant HARD_INPUT : integer := 123;
    constant EXPECTED_OUTPUT : integer := 5275;
    
    signal encrypt  : integer;
    signal decrypt  : integer;
    signal slow     : std_logic;
    
    component CLK_DIV_FS is
        Port(   clk     : in std_logic;
                sclk    : out std_logic);
    end component;
    
    component Encryption is
        Port (clk : in std_logic;
              input  : in integer;
              output : out integer );
    end component;
    
    component Decryption is
        Port (clk : in std_logic;
              input : in integer;
              output : out integer);
    end component;
        
begin

--    CLK1 : CLK_DIV_FS
--    port map(clk => CLK_IN,
--             sclk => slow);
             
    ENCRYPTION1 : Encryption
    port map(clk => CLK_IN,
             input => HARD_INPUT,
             output => encrypt);

    DECRYPTION1 : Decryption
    port map(clk => CLK_IN,
             input => encrypt,
             output => decrypt);
    
    process(encrypt, decrypt, button)
    begin
        if (button = '1') then
            correct_en <= '0';
            correct_de <= '0';
        else
            if (encrypt = EXPECTED_OUTPUT) then
                correct_en <= '1';
            end if;
            if (decrypt = HARD_INPUT) then
                correct_de <= '1';
            end if;
        end if;
    end process;
    
end Behavioral;
