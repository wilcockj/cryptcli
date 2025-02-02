import typer
from typing import List, Optional
from rich.console import Console
from rich.table import Table
import requests, json, time
import plotext as pltx
import inquirer
app = typer.Typer()
console = Console()

def getResp(crypto: str):
    url = f"https://api.coincap.io/v2/assets/{crypto}"
    console.print(f"Querying {url}...")
    resp = requests.get(url)
    return resp

@app.command()
def info(crypto: str):
    """
    provides basic info for a specific crypto
    """
    print()
    resp = getResp(crypto)
    # console.print(resp)
    if (resp.status_code != 200):
        console.print(f"[bold red blink]Error: reponse code {resp.status_code}...[/ bold red blink]")
        return
    text = resp.text
    data = json.loads(text)['data']
    # console.print(data)

    table = Table(
        title = f"-== {crypto} ({data['symbol']}) ==-",
        title_justify = "left",
        title_style = "bold orange3",
    )
    table.add_column("Rank")
    table.add_column("Price")
    table.add_column("Supply")
    table.add_column("Down or Up (24hr)")
    table.add_row(
        str(data['rank']),
        f"${data['priceUsd']}",
        str(data['supply']),
        f"[red]{data['changePercent24Hr']}[/ red]" if data['changePercent24Hr'][0] == "-" else f"[green]{data['changePercent24Hr']}[/ green]",
    )
    console.print(table)
    print()

@app.command()
def price(crypto: str):
    """
    displays the price of a specific crypto
    """
    print()
    resp = getResp(crypto)
    # console.print(resp)
    if (resp.status_code != 200):
        console.print(f"[bold red blink]Error: reponse code {resp.status_code}...[/ bold red blink]")
        return
    text = resp.text
    data = json.loads(text)['data']
    console.print(f"[bold dim]The price of [green italic]{crypto}[/ green italic] is [yellow italic]${data['priceUsd']}[/ yellow italic].[/ bold dim]")
    print()

@app.command()
def list(num: Optional[int] = 10):
    """
    lists out the top crypto prices
    """
    resp = requests.get("https://api.coincap.io/v2/assets")
    if (resp.status_code != 200):
        console.print(f"[bold red blink]Error: reponse code {resp.status_code}...[/ bold red blink]")
        return
    text = resp.text
    data = json.loads(text)['data']

    for idx, crypto in enumerate(data):
        if (idx >= num):
            break
        console.print(f"({idx + 1}) {crypto['id']} : ${crypto['priceUsd']}")
        time.sleep(0.01)

@app.command()
def hist(cryptos: List[str]):
    """
    displays pricing graph for a certain interval
    """
    if (len(cryptos) > 2):
        console.print("[red bold]At this time, you can only graph two cryptos at a time...[/ red bold]")
        return
    questions = [
      inquirer.List('data',
                    message="Range",
                    choices=['1D', '1W', '1M', '6M', '1Y'],
                ),
    ]
    interval = inquirer.prompt(questions)

    convertedRange =  "d1"
    match interval['data']:
        case "1Y":
            convertedRange = "d1"
        case "1D":
            convertedRange = "m1"
        case "1M":
            convertedRange = "h1"
        case "1W":
            convertedRange = "m15"
        case "6M":
            convertedRange = "h6"

    for idx, crypto in enumerate(cryptos):
        resp = requests.get(f"https://api.coincap.io/v2/assets/{crypto}/history?interval={convertedRange}")
        if (resp.status_code != 200):
            console.print(f"[bold red blink]Error: reponse code {resp.status_code}...[/ bold red blink]")
            return
        text = resp.text
        data = json.loads(text)['data']

        prices = []
        for instance in data:
            prices.append(float(instance['priceUsd']))
        price_up = (prices[-1] - prices[0]) > 0 
        pltx.plot(prices, label=f"price of {crypto}", yside = "left" if idx == 0 else "right", color = "green" if price_up else "red+")
    
    pltx.canvas_color(236)
    pltx.axes_color(236)
    pltx.ticks_color("white")
    pltx.ticks_style("bold")
    pltx.xlabel(f"Time ({interval['data']})")
    pltx.xfrequency(0)
    pltx.ylabel("Price (USD)")
    pltTitle = f"{interval['data']} price range of"
    for idx, crypto in enumerate(cryptos):
        if len(cryptos) == 1:
            pltTitle += f" {crypto}"
        elif idx < len(cryptos) - 1:
            pltTitle += f" {crypto},"
        else:
            pltTitle += f" and {crypto}."
    pltx.title(pltTitle)
    pltx.show()

if __name__ == "__main__":
    app()
