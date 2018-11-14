# ten-castles

## Example

Suppose that the server address is localhost and the port used 50001. Then for
the server side,

```bash
python3 ./server.py 50001 
```

And for the client side,

```bash
python3 ./client.py localhost:50001

# The following lines are the input
add uniform 10 10 10 10 10 10 10 10 10 10
run uniform
delete uniform
check uniform
duels
exit

```

where 'uniform' is the identifier of the strategy. It is encouraged to add a
prefix, such as 'evensgn_' before the identifier to avoid conflicts. 
