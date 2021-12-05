#!/usr/bin/php -f
<?php
$grid = array();
while($line = fgets(STDIN)){
    [$a, $b, $c, $d] = array_map('intval', preg_split( '/,|(->)/', $line));
    if ($a == $c || $b == $d) {
        [$i, $j, $di, $dj] = [$a, $b, $c - $a <=> 0, $d - $b <=> 0];
        $grid[strval($i) . ',' . strval($j)]++;
        while($i != $c || $j != $d) {
            $i += $di;
            $j += $dj;
            $grid[sprintf("%d,%d", $i, $j)]++;
        };
    }
}
echo array_reduce($grid, function($acc, $cell_count) {
    return $acc + ($cell_count > 1);
});
?>
