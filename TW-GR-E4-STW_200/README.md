# TW_GR_E4_STW
##### Description:
Many saw the [fourth installment of Toaster Wars: Going Rogue](http://shell2017.picoctf.com:31884) as a return to grace after the relative mediocrity of the third. I'm just glad it was made at all. And hey, they added some nifty new [online scoreboard](http://shell2017.picoctf.com:31884/scoreboard) features, too!

#### Hints:
Ooh, what a nifty scoreboard! If we get a bunch of people playing at once, we can have a race through the dungeon!

#### Solution:

Unlike the previous games, the current floor of the player is stored in the database
for the scoreboard.

When a player reaches the stairs, we find the following line of code:
```javascript
db.scoreboard[socket.id].floor++;
```

The flag is on the fifth floor, but the stairs on the fourth floor are unreachable.
Because of the way the floors are stored in the database, we can trigger a race condition
by sending two requests to move to the stairs on the second floor at the same time.
This will trigger the floor increment twice, allowing us to skip a floor.
We can do this by defining the following function in the javascript console:

```javascript
function move() {
    api("action", {
        type: "move",
        direction: facingDirection
    });
    api("action", {
        type: "move",
        direction: facingDirection
    });
}
```

Then, when facing the stairs on the third floor, call the function.
```javascript
> move()
```

We immediately skip to the fifth floor, where we find the flag:
`im_still_upset_you_dont_get_to_keep_the_cute_scarves_in_the_postgame_13a8da6472334d3077f4abd265ea72af`
