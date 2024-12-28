use strict;
use warnings;
use Tk;

# Define constants for the game
my $BOARD_SIZE = 10;
my $SQUARE_SIZE = 50;
my $MAX_POSITION = 100;

# Snake and ladder mappings
my %snakes = (16 => 6, 47 => 26, 49 => 11, 56 => 53, 62 => 19, 87 => 24, 93 => 73, 95 => 75, 98 => 78);
my %ladders = (3 => 38, 8 => 30, 28 => 84, 58 => 77, 75 => 86, 80 => 99);

# Player class
package Player;
sub new {
    my ($class, $name, $color) = @_;
    my $self = {
        name  => $name,
        color => $color,
        pos   => 0,  # Position 0 means not on the board
        active => 0, # Player is not active until they roll a 6
    };
    bless $self, $class;
    return $self;
}

sub move {
    my ($self, $dice_roll) = @_;
    
    # If player is not yet active, check for dice roll of 6 to start
    if ($self->{pos} == 0 && $dice_roll == 6) {
        $self->{active} = 1;
        $self->{pos} = 1;  # Move to position 1
    } elsif ($self->{active}) {
        # Move the player by the dice roll if already active
        $self->{pos} += $dice_roll;
        $self->{pos} = $MAX_POSITION if $self->{pos} > $MAX_POSITION;  # Cap at 100
    }
}

sub reset {
    my ($self) = @_;
    $self->{pos} = 0;
    $self->{active} = 0;
}

package main;

# Create main window
my $mw = MainWindow->new;
$mw->title("Snake and Ladder Game");
$mw->geometry("600x600");

# Create player objects
my $player1 = Player->new("Player 1", 'blue');
my $player2 = Player->new("Player 2", 'dark green');
my @players = ($player1, $player2);
my $current_player = 0;  # Start with player 1

# Canvas for the game board
my $canvas = $mw->Canvas(
    -width  => $BOARD_SIZE * $SQUARE_SIZE,
    -height => $BOARD_SIZE * $SQUARE_SIZE,
    -background => 'white',
)->pack;

# Labels for the dice roll and turn
my $dice_label = $mw->Label(-text => "Dice: Not rolled yet", -fg => 'black')->pack(-side => 'bottom');
my $turn_label = $mw->Label(-text => "$players[$current_player]->{name}'s turn", -fg => $players[$current_player]->{color})->pack(-side => 'bottom');

# Restart button
$mw->Button(
    -text => 'Restart Game',
    -command => \&restart_game,
)->pack(-side => 'bottom');

# Manually define each step from 1 to 100 (bottom-left to top-right, left to right in rows)
my @steps = (
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    20, 19, 18, 17, 16, 15, 14, 13, 12, 11,
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    40, 39, 38, 37, 36, 35, 34, 33, 32, 31,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
    60, 59, 58, 57, 56, 55, 54, 53, 52, 51,
    61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
    80, 79, 78, 77, 76, 75, 74, 73, 72, 71,
    81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
    100, 99, 98, 97, 96, 95, 94, 93, 92, 91
);

# Draw the game board (10x10 grid)
my $step = 0;
for my $row (0 .. $BOARD_SIZE - 1) {
    for my $col (0 .. $BOARD_SIZE - 1) {
        # Number the steps from 1 to 100 left-to-right, bottom-to-top
        my $x1 = $col * $SQUARE_SIZE;
        my $y1 = ($BOARD_SIZE - 1 - $row) * $SQUARE_SIZE;  # Rows go up from bottom
        my $x2 = $x1 + $SQUARE_SIZE;
        my $y2 = $y1 + $SQUARE_SIZE;

        $canvas->createRectangle($x1, $y1, $x2, $y2, -outline => 'black', -fill => 'white');
        $canvas->createText($x1 + $SQUARE_SIZE / 2, $y1 + $SQUARE_SIZE / 2, -text => $steps[$step]);

        # Draw snakes and ladders
        if (exists $snakes{$steps[$step]}) {
            $canvas->createText($x1 + $SQUARE_SIZE / 2, $y1 + $SQUARE_SIZE / 3, -text => "&($snakes{$steps[$step]})", -fill => 'red');
        }
        if (exists $ladders{$steps[$step]}) {
            $canvas->createText($x1 + $SQUARE_SIZE / 2, $y1 + 2 * $SQUARE_SIZE / 3, -text => "H($ladders{$steps[$step]})", -fill => 'green');
        }

        $step++;
    }
}

# Player tokens
my %player_tokens;
for my $i (0 .. $#players) {
    $player_tokens{$i} = $canvas->createOval(
        -10, -10, -10, -10, -fill => $players[$i]->{color}, -outline => 'black'
    );
}

# Dice roll button
$mw->Button(
    -text => 'Roll Dice',
    -command => \&roll_dice,
)->pack(-side => 'bottom');

# Roll the dice and process the move
sub roll_dice {
    my $dice_roll = int(rand(6)) + 1;
    $dice_label->configure(-text => "Dice: $dice_roll");

    my $player = $players[$current_player];

    # If player is active, move by the dice roll
    if ($player->{active} || $dice_roll == 6) {
        $player->move($dice_roll);
    }

    # Handle snakes and ladders
    if (exists $snakes{$player->{pos}}) {
        handle_snake_or_ladder($player, 'snake', $snakes{$player->{pos}});
    } elsif (exists $ladders{$player->{pos}}) {
        handle_snake_or_ladder($player, 'ladder', $ladders{$player->{pos}});
    }

    # Check if player won
    if ($player->{pos} == $MAX_POSITION) {
        game_over("$player->{name} wins!");
    } else {
        update_player_position($current_player);
        switch_turn();
    }
}

# Handle snake or ladder
sub handle_snake_or_ladder {
    my ($player, $type, $new_pos) = @_;
    
    my $popup = $mw->Dialog(
        -title => "Question",
        -text => "Are you $player->{name} in step $player->{pos}?",
        -buttons => ['Yes', 'No'],
    );
    
    my $response = $popup->Show;
    if ($response eq 'Yes') {
        if ($type eq 'ladder') {
            $player->{pos} = $new_pos;
        }
    } else {
        if ($type eq 'snake') {
            $player->{pos} = $new_pos;
        }
    }

    update_player_position($current_player);
    switch_turn();
}

# Update the position of the player's token on the board
sub update_player_position {
    my ($player_idx) = @_;
    my $player = $players[$player_idx];
    
    my $pos = $player->{pos};
    my $row = int(($pos - 1) / $BOARD_SIZE);
    my $col = ($pos - 1) % $BOARD_SIZE;
    
    my $x = $col * $SQUARE_SIZE + $SQUARE_SIZE / 2;
    my $y = ($BOARD_SIZE - $row - 1) * $SQUARE_SIZE + $SQUARE_SIZE / 2;
    
    $canvas->coords($player_tokens{$player_idx}, $x - 10, $y - 10, $x + 10, $y + 10);
}

# Switch the turn to the next player
sub switch_turn {
    $current_player = 1 - $current_player;
    $turn_label->configure(-text => "$players[$current_player]->{name}'s turn", -fg => $players[$current_player]->{color});
}

# Restart the game
sub restart_game {
    for my $player (@players) {
        $player->reset();
    }
    $dice_label->configure(-text => "Dice: Not rolled yet");
    $current_player = 0;
    $turn_label->configure(-text => "$players[$current_player]->{name}'s turn", -fg => $players[$current_player]->{color});
    update_player_position($current_player);
}

# Show the winner and restart the game
sub game_over {
    my ($message) = @_;
    my $popup = $mw->Dialog(
        -title => "Game Over",
        -text => $message,
        -buttons => ['OK'],
    );
    $popup->Show;
    restart_game();
}

MainLoop;
