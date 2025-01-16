use strict;
use warnings;
use Tk;

# Define the game board with snakes and ladders
my %snakes = (
    16 => 6, 47 => 26, 49 => 11, 56 => 53, 62 => 19, 64 => 60, 87 => 24, 93 => 73, 95 => 75, 98 => 78
);
my %ladders = (
    1 => 38, 4 => 14, 9 => 31, 21 => 42, 28 => 84, 36 => 44, 51 => 67, 71 => 91, 80 => 100
);

# Player positions
my @players = (
    { name => "Player blue", color => "blue", position => 0 },
    { name => "Player green", color => "green", position => 0 }
);

# Current player and dice value
my $current_player = 0;
my $dice_value = 0;
my $started = 0; # Game starts only after a player rolls a 6

# GUI setup
my $mw = MainWindow->new;
$mw->title("Snakes and Ladders");

my $canvas = $mw->Canvas(-width => 500, -height => 500)->pack;

# Draw board
for my $i (0..9) {
    for my $j (0..9) {
        my $x = $i * 50;
        my $y = $j * 50;
        my $step = $j * 10 + $i +1;
        $canvas->createRectangle($x, $y, $x + 50, $y + 50, -fill => 'white');
        $canvas->createText($x + 25, $y + 25, -text => $step);

        # Draw snakes
        if (exists $snakes{$step}) {
            $canvas->createText($x + 40, $y + 40, -text => "SS($snakes{$step})", -fill => 'red');
        }

        # Draw ladders
        if (exists $ladders{$step}) {
            $canvas->createText($x + 40, $y + 40, -text => "LL($ladders{$step})", -fill => 'green');
        }
    }
}

# Dice display
my $dice_label = $mw->Label(-text => "Dice: 0", -font => "Arial 14")->pack;

# Turn display
my $turn_label = $mw->Label(-text => "Turn: Player 1", -font => "Arial 14")->pack;

# Dice button
my $dice_button = $mw->Button(
    -text => "Roll Dice",
    -command => \&roll_dice
)->pack;

# Roll dice function
sub roll_dice {
    $dice_value = int(rand(6)) + 1;
    $dice_label->configure(-text => "Dice: $dice_value");
    $mw->update;

    # If the game hasn't started, players must roll a 6 to start
    if (!$started) {
        if ($dice_value == 6) {
            $started = 1; # Game starts
        } else {
            switch_player();
            return;
        }
    }

    # Move the current player
    my $player = $players[$current_player];
    $player->{position} += $dice_value;

    # Check if the player has won
    if ($player->{position} >= 100) {
        $player->{position} = 100;
        show_winner($player->{name});
        return;
    }

    # Check for snakes or ladders
    my $new_position = $player->{position};
    if (exists $snakes{$new_position} || exists $ladders{$new_position}) {
        my $answer = ask_question($player->{name}, $new_position);
        if ($answer eq "yes") {
            if (exists $snakes{$new_position}) {
                # Snake does not bite
            } else {
                # Ladder helps
                $player->{position} = $ladders{$new_position};
            }
        } else {
            if (exists $snakes{$new_position}) {
                # Snake bites
                $player->{position} = $snakes{$new_position};
            } else {
                # Ladder does not help
            }
        }
    }

    # Update the board
    update_board();

    # Switch player if dice is not 6
    if ($dice_value != 6) {
        switch_player();
    }
}

# Switch player function
sub switch_player {
    $current_player = 1 - $current_player;
    $turn_label->configure(-text => "Turn: $players[$current_player]{name}");
}

# Ask question function
sub ask_question {
    my ($player_name, $step) = @_;
    my $answer = $mw->messageBox(
        -message => "Are you ($player_name) in step number $step?",
        -type => "yesno",
        -icon => "question"
    );
    return $answer;
}

# Show winner function
sub show_winner {
    my ($player_name) = @_;
    $mw->messageBox(-message => "$player_name wins!", -title => "Game Over");
    $mw->destroy;
}

# Update board function
sub update_board {
    $canvas->delete("player");
    for my $player (@players) {
        my $position = $player->{position};
        next if $position == 0;
        my $x = (($position - 1) % 10) * 50 + 25;
        my $y = int(($position - 1) / 10) * 50 + 25;
        $canvas->createOval($x - 10, $y - 10, $x + 10, $y + 10, -fill => $player->{color}, -tags => "player");
    }
}

MainLoop;