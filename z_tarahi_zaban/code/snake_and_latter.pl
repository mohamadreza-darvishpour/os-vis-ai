use strict;
use warnings;
use Tk;

# Tile class for each step on the board
package Tile;
sub new {
    my ($class, $position) = @_;
    my $self = {
        position  => $position,
        snake     => undef,
        ladder    => undef,
    };
    bless $self, $class;
    return $self;
}

# Set or get snake on this tile
sub set_snake {
    my ($self, $to) = @_;
    $self->{snake} = $to if defined $to;
    return $self->{snake};
}

# Set or get ladder on this tile
sub set_ladder {
    my ($self, $to) = @_;
    $self->{ladder} = $to if defined $to;
    return $self->{ladder};
}

# Player class for each player
package Player;
sub new {
    my ($class, $name, $color) = @_;
    my $self = {
        name   => $name,
        color  => $color,
        pos    => 0,  # Start at position 0
    };
    bless $self, $class;
    return $self;
}

# Move player by dice roll
sub move {
    my ($self, $dice, $board) = @_;
    my $new_pos = $self->{pos} + $dice;
    if ($new_pos > 100) {
        return;  # Can't move beyond 100
    }
    $self->{pos} = $new_pos;

    # Check for snakes or ladders
    my $tile = $board->get_tile($self->{pos});
    if (my $snake_to = $tile->set_snake) {
        $self->{pos} = $snake_to;  # Move to snake's tail
    }
    elsif (my $ladder_to = $tile->set_ladder) {
        $self->{pos} = $ladder_to;  # Move to ladder's top
    }
}

# Get player position
sub get_position {
    my $self = shift;
    return $self->{pos};
}

# Board class for the game board
package Board;
sub new {
    my ($class) = @_;
    my $self = {
        tiles   => [],  # List of tiles (1 to 100)
        players => [],
    };

    # Create 100 tiles
    for my $i (1 .. 100) {
        push @{ $self->{tiles} }, Tile->new($i);
    }

    bless $self, $class;
    return $self;
}

# Add player to the board
sub add_player {
    my ($self, $player) = @_;
    push @{ $self->{players} }, $player;
}

# Get tile by position
sub get_tile {
    my ($self, $position) = @_;
    return $self->{tiles}[$position - 1];  # 1-indexed position
}

# Set snakes and ladders
sub set_snakes_and_ladders {
    my ($self, $snakes, $ladders) = @_;
    for my $start (keys %$snakes) {
        my $tile = $self->get_tile($start);
        $tile->set_snake($snakes->{$start});
    }
    for my $start (keys %$ladders) {
        my $tile = $self->get_tile($start);
        $tile->set_ladder($ladders->{$start});
    }
}

# Game loop and UI
package main;

# Initialize the game
my $board = Board->new();
my $player1 = Player->new('Player 1', 'blue');
my $player2 = Player->new('Player 2', 'green');

$board->add_player($player1);
$board->add_player($player2);

# Example snakes and ladders
my %snakes = (16 => 6, 47 => 26, 49 => 11, 56 => 53, 62 => 19, 87 => 24, 93 => 73, 95 => 75, 98 => 78);
my %ladders = (3 => 38, 8 => 30, 28 => 84, 58 => 77, 75 => 86, 80 => 99);

$board->set_snakes_and_ladders(\%snakes, \%ladders);

# Initialize Tk window
my $mw = MainWindow->new;
$mw->title("Snakes and Ladders");

# Canvas for board
my $canvas = $mw->Canvas(-width => 500, -height => 500)->pack;

# Labels for player information
my $turn_label = $mw->Label(-text => "It's Player 1's turn to roll the dice")->pack;
my $dice_label = $mw->Label(-text => "Dice: Not rolled yet")->pack;

# Draw board with numbers and layout
my $square_size = 40;
for my $row (0 .. 9) {
    for my $col (0 .. 9) {
        my $x1 = $col * $square_size;
        my $y1 = $row * $square_size;
        my $x2 = $x1 + $square_size;
        my $y2 = $y1 + $square_size;
        my $tile_num = ($row * 10) + $col + 1;
        
        # Draw squares
        $canvas->createRectangle($x1, $y1, $x2, $y2, -outline => 'black');
        $canvas->createText($x1 + $square_size / 2, $y1 + $square_size / 2, -text => $tile_num);
    }
}

# Draw player tokens
my %player_tokens;
for my $i (0 .. 1) {
    my $player = $board->{players}[$i];
    my $color = $player->{color};
    $player_tokens{$i} = $canvas->createOval(10, 10, 10, 10, -fill => $color);
}

# Roll dice function
sub roll_dice {
    my $dice = int(rand(6)) + 1;
    $dice_label->configure(-text => "Dice: $dice");
    
    my $player = $board->{players}[0];  # Player 1's turn, could be changed
    $player->move($dice, $board);
    
    update_player_position($player);
    
    if ($player->get_position() == 100) {
        $turn_label->configure(-text => "Player 1 Wins!");
    }
    else {
        $turn_label->configure(-text => "It's Player 2's turn to roll the dice");
    }
}

# Update the player position on the board
sub update_player_position {
    my ($player) = @_;
    my $pos = $player->get_position();
    my $row = int(($pos - 1) / 10);
    my $col = ($pos - 1) % 10;
    my $x = $col * $square_size + $square_size / 2;
    my $y = $row * $square_size + $square_size / 2;
    
    # Update player token position
    $canvas->coords($player_tokens{0}, $x - 10, $y - 10, $x + 10, $y + 10);
}

# Roll dice button
$mw->Button(
    -text    => 'Roll Dice',
    -command => \&roll_dice
)->pack;

MainLoop;
