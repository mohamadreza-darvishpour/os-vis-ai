use strict;
use warnings;
use Tk;
use Tk::Dialog;

# Board dimensions and settings
my $board_size = 10;
my $square_size = 50;
my %snakes = (16 => 6, 47 => 26, 49 => 11, 56 => 53, 62 => 19, 87 => 24, 93 => 73, 95 => 75, 98 => 78);
my %ladders = (3 => 38, 8 => 30, 28 => 84, 58 => 77, 75 => 86, 80 => 99);

# Player details
my @players = (
    { name => 'Player 1', color => 'blue', pos => 0, active => 0 },
    { name => 'Player 2', color => 'light green', pos => 0, active => 0 }
);
my $current_player = 0;

# Tk main window
my $mw = MainWindow->new;
$mw->title("Snake and Ladder");
$mw->geometry(($board_size * $square_size) . "x" . (($board_size * $square_size) + 100));

# Canvas for board
my $canvas = $mw->Canvas(
    -width  => $board_size * $square_size,
    -height => $board_size * $square_size,
    -background => 'white',
)->pack;

# Label for dice and turn
my $turn_label = $mw->Label(-text => "It's Player 1's turn to roll the dice")->pack(-side => 'bottom');
my $dice_label = $mw->Label(-text => "Dice: Not rolled yet")->pack(-side => 'bottom');

# Restart button
$mw->Button(
    -text    => 'Restart Game',
    -command => sub { restart_game(); }
)->pack(-side => 'bottom');

# Draw the board
for my $row (0 .. $board_size - 1) {
    for my $col (0 .. $board_size - 1) {
        my $step = ($board_size - $row - 1) * $board_size + (($row % 2 == 0) ? ($col + 1) : ($board_size - $col));
        my $x1 = $col * $square_size;
        my $y1 = $row * $square_size;
        my $x2 = $x1 + $square_size;
        my $y2 = $y1 + $square_size;

        # Draw cell and label it
        $canvas->createRectangle($x1, $y1, $x2, $y2, -outline => 'black', -fill => 'white');
        $canvas->createText($x1 + $square_size / 2, $y1 + $square_size / 2, -text => $step);

        # Add snake/ladder markers
        if (exists $snakes{$step}) {
            $canvas->createText($x1 + $square_size / 2, $y1 + $square_size / 3, -text => "&($snakes{$step})", -fill => 'red');
        }
        if (exists $ladders{$step}) {
            $canvas->createText($x1 + $square_size / 2, $y1 + 2 * $square_size / 3, -text => "H($ladders{$step})", -fill => 'green');
        }
    }
}

# Draw players
my %player_tokens;
for my $i (0 .. $#players) {
    $player_tokens{$i} = $canvas->createOval(
        -10, -10, -10, -10, -fill => $players[$i]->{color}, -outline => 'black'
    );
}

# Button for dice roll
$mw->Button(
    -text    => 'Roll Dice',
    -command => sub { roll_dice(); }
)->pack(-side => 'bottom');

# Helper functions
sub roll_dice {
    my $dice = int(rand(6)) + 1;
    $dice_label->configure(-text => "Dice: $dice");

    my $player = $players[$current_player];
    if ($player->{pos} == 0 && $dice != 6) {
        $turn_label->configure(-text => "$player->{name} needs a 6 to start.");
        switch_turn();
        return;
    }

    # Move the player
    $player->{pos} += $dice;
    if ($player->{pos} > 100) {
        $player->{pos} -= $dice; # Don't overshoot
        $turn_label->configure(-text => "$player->{name} cannot move, waiting for next turn.");
        switch_turn();
        return;
    }

    # Check for snakes or ladders
    if (exists $snakes{$player->{pos}}) {
        ask_question($player, "snake", $snakes{$player->{pos}});
    } elsif (exists $ladders{$player->{pos}}) {
        ask_question($player, "ladder", $ladders{$player->{pos}});
    } else {
        update_player_position($current_player);
        switch_turn() if $dice != 6;
    }

    # Check for win condition
    if ($player->{pos} == 100) {
        game_over("$player->{name} wins!");
    }
}

sub ask_question {
    my ($player, $type, $new_pos) = @_;
    my $popup = $mw->Dialog(
        -title   => "Question",
        -text    => "Are you ($player->{name}) at step $player->{pos}?",
        -buttons => ['Yes', 'No'],
    );
    my $response = $popup->Show;

    if (($response eq 'Yes' && $type eq 'ladder') || ($response eq 'No' && $type eq 'snake')) {
        $player->{pos} = $new_pos if $type eq 'ladder';
    } elsif (($response eq 'Yes' && $type eq 'snake') || ($response eq 'No' && $type eq 'ladder')) {
        $player->{pos} = $new_pos if $type eq 'snake';
    }
    update_player_position($current_player);
    switch_turn();
}

sub update_player_position {
    my ($player_idx) = @_;
    my $player = $players[$player_idx];
    my $pos = $player->{pos};
    my $row = int(($pos - 1) / $board_size);
    my $col = ($row % 2 == 0) ? (($pos - 1) % $board_size) : ($board_size - 1 - ($pos - 1) % $board_size);

    my $x = $col * $square_size + $square_size / 2;
    my $y = ($board_size - $row - 1) * $square_size + $square_size / 2;

    $canvas->coords($player_tokens{$player_idx}, $x - 10, $y - 10, $x + 10, $y + 10);
}

sub switch_turn {
    $current_player = 1 - $current_player;
    $turn_label->configure(-text => "It's $players[$current_player]->{name}'s turn to roll the dice");
}

sub restart_game {
    foreach my $player (@players) {
        $player->{pos} = 0;
    }
    for my $i (0 .. $#players) {
        update_player_position($i);
    }
    $dice_label->configure(-text => "Dice: Not rolled yet");
    $current_player = 0;
    $turn_label->configure(-text => "It's $players[$current_player]->{name}'s turn to roll the dice");
}

sub game_over {
    my ($message) = @_;
    my $popup = $mw->Dialog(
        -title   => "Game Over",
        -text    => $message,
        -buttons => ['OK'],
    );
    $popup->Show;
    restart_game();
}

MainLoop;
