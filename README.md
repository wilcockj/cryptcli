# cryptcli

## Description
The cryptcli is a python package that gives you access to cryptocurrency prices right in your terminal!
- API Used: [coincap](https://coincap.io/)
- Libraries Used: [typer](https://github.com/tiangolo/typer), [rich](https://github.com/Textualize/rich), [plotext](https://github.com/piccolomo/plotext), [inquirer](https://github.com/magmax/python-inquirer) 

## Installation
```zsh
$ pip install cryptcli
```

## Usuage
For a list of commands, type:
```zsh
$ crypt --help
```
To see specifics of each command, type:
```zsh
$ crypt [COMMAND] --help
```

## Commands
```zsh
$ crypt [COMMANDS] [ARGS]
  [COMMANDS] = info, list, hist, price
```

### hist
For example, type:
```zsh
$ crypt hist litecoin
```
This command will prompt you to select the interval, use the up and down arrow keys hitting enter to make a selection.
After selecting a 1Y interval, you should see something like this:
<img src="./pictures/litecoin-1y.png">
You can also compare two cryptocurrencies prices at the same time by typing:
```zsh
$ crypt hist [CRYPTO1] [CRYPTO2]
```

### price
For example, type:
```zsh
$ crypt price dogecoin
```
This command will display the current price of the supplied cryptocurrency argument.
For the example above, you should see this output:
<img src="./pictures/price-doge.png">

### list
For example, type:
```zsh
$ crypt list
$ crypt list --num 10
```
This command will return a list of cryptos and their corresponding prices. The length of the list depends on the integer argument supplied.
The command above should yeild something like this:
<img src="./pictures/list-10.png">

### info
For example, type:
```zsh
$ crypt info solana
```
This command returns a basic table of current values about a specific supplied cryptocurrency.
The example command above should show something similar to this:
<img src="./pictures/info-solana.png">
