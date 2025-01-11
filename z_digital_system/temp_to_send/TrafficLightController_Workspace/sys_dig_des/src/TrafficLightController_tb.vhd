library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity TrafficLightController_tb is
end TrafficLightController_tb;

architecture Behavioral of TrafficLightController_tb is
    -- Component declaration for the main module
    component TrafficLightController
        Port (
            Y1 : out STD_LOGIC;
            Y2 : out STD_LOGIC;
            G1 : out STD_LOGIC;
            G2 : out STD_LOGIC;
            R1 : out STD_LOGIC;
            R2 : out STD_LOGIC;
            clk : in STD_LOGIC
        );
    end component;

    -- Signals to connect to the main module
    signal Y1 : STD_LOGIC;
    signal Y2 : STD_LOGIC;
    signal G1 : STD_LOGIC;
    signal G2 : STD_LOGIC;
    signal R1 : STD_LOGIC;
    signal R2 : STD_LOGIC;
    signal clk : STD_LOGIC := '0';

begin
    -- Instantiate the main module
    UUT: TrafficLightController
        Port map (
            Y1 => Y1,
            Y2 => Y2,
            G1 => G1,
            G2 => G2,
            R1 => R1,
            R2 => R2,
            clk => clk
        );

    -- Clock generation process
    Clock_Process: process
    begin
        while true loop
            clk <= '0';
            wait for 1 ns; -- 1ns clock period
            clk <= '1';
            wait for 1 ns;
        end loop;
    end process Clock_Process;

    -- Simulation time control
    Simulation_Process: process
    begin
        wait for 120 ns; -- Run simulation for 120ns (2 cycles)
        wait;
    end process Simulation_Process;
end Behavioral;
