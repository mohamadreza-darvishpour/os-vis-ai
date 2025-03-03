-- TogglePorts.vhd
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL; -- For integer arithmetic

entity TogglePorts is
    Port (
        clk : in  STD_LOGIC;   -- Clock input
        reset : in  STD_LOGIC; -- Reset input
        a : out STD_LOGIC;     -- Output port A
        b : out STD_LOGIC;     -- Output port B
        c : out STD_LOGIC      -- Output port C
    );
end TogglePorts;

architecture Behavioral of TogglePorts is
    signal counter : integer := 0;          -- Counter for clock cycles
    signal current_state : integer range 0 to 2 := 0; -- State to toggle outputs
    constant CLOCKS_PER_SECOND : integer := 50_000_000; -- Adjust for your clock frequency
begin
    process(clk, reset)
    begin
        if reset = '1' then
            current_state <= 0;
            counter <= 0;
        elsif rising_edge(clk) then
            if counter = CLOCKS_PER_SECOND - 1 then
                counter <= 0;
                current_state <= (current_state + 1) mod 3; -- Cycle through states 0, 1, 2
            else
                counter <= counter + 1;
            end if;
        end if;
    end process;

    -- Assign outputs based on the current state
    a <= '1' when current_state = 0 else '0';
    b <= '1' when current_state = 1 else '0';
    c <= '1' when current_state = 2 else '0';
end Behavioral;

-- Testbench: TogglePorts_tb.vhd
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity TogglePorts_tb is
end TogglePorts_tb;

architecture Behavioral of TogglePorts_tb is
    signal clk   : std_logic := '0';
    signal reset : std_logic := '1';
    signal a, b, c : std_logic;
begin
    -- Instantiate the design under test (DUT)
    DUT: entity work.TogglePorts
        port map (
            clk => clk,
            reset => reset,
            a => a,
            b => b,
            c => c
        );

    -- Clock generation (50 MHz clock, 20 ns period)
    clk <= not clk after 10 ns;

    -- Reset signal
    process
    begin
        reset <= '1';
        wait for 50 ns;
        reset <= '0';
        wait;
    end process;
end Behavioral;

