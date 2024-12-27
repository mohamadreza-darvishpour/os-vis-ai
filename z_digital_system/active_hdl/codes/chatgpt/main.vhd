name: TrafficLightController

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity TrafficLightController is
    Port (
        Y1 : out STD_LOGIC; -- First yellow light
        Y2 : out STD_LOGIC; -- Second yellow light
        G1 : out STD_LOGIC; -- First green light
        G2 : out STD_LOGIC; -- Second green light
        R1 : out STD_LOGIC; -- First red light
        R2 : out STD_LOGIC; -- Second red light
        clk : in STD_LOGIC  -- Clock input
    );
end TrafficLightController;

architecture Behavioral of TrafficLightController is
    signal counter : INTEGER := 0; -- Internal time counter
begin
    -- Process to manage the traffic light sequence
    TrafficLight_Process: process(clk)
    begin
        if rising_edge(clk) then
            -- Increment counter with each clock cycle
            counter <= (counter + 1) mod 60; -- 60ns cycle

            -- Set output based on counter value
            if counter >= 0 and counter < 2 then
                Y1 <= '1'; Y2 <= '1'; G1 <= '1'; G2 <= '0'; R1 <= '0'; R2 <= '1';
            elsif counter >= 2 and counter < 30 then
                Y1 <= '0'; Y2 <= '0'; G1 <= '0'; G2 <= '1'; R1 <= '1'; R2 <= '0';
            elsif counter >= 30 and counter < 32 then
                Y1 <= '1'; Y2 <= '1'; G1 <= '0'; G2 <= '1'; R1 <= '1'; R2 <= '0';
            elsif counter >= 32 and counter < 60 then
                Y1 <= '0'; Y2 <= '0'; G1 <= '1'; G2 <= '0'; R1 <= '0'; R2 <= '1';
            end if;
        end if;
    end process TrafficLight_Process;
end Behavioral;
