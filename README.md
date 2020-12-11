# Bingo Simulator

## Bingo Game Description
* `n` people in a room.
* Each person will have a board of `(size, size)`
* Each person will fill his/her board with the number in `[0, n)`.
* At the end of the game, the host will draw numbers `i` from `[0, n)` without replacement.
And each time an `i` is drawn, people with `i` on his/her board can cross it out number.
* The game will end when at least one person's board connect.
* We want to know how many iterations will the host need to draw the number in average.
And how many boards will connect when the game ends.

## Simuation Result

(The number of experiments: `10000`)

|`n`|`size`|The average number of iterations|The number of boards connect|
|---|---|---|---|
|30|3|5.75|1.31|
|30|4|8.27|1.29|
|35|3|6.26|1.28|
|35|4|9.12|1.26|
|40|3|6.67|1.25|
|40|4|9.85|1.23|

## How to Run
`python simulator.py <num exps> <n> <size>`

Ex. `python simulator.py 10000 30 3` for the first row of the experiment.
