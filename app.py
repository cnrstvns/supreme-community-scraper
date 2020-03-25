from flask import Flask, request, render_template, redirect, url_for
from dhooks import Webhook, Embed
import datetime
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('.scraper'))

@app.route("/scraper")
def scraper():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def form():
    if request.method == "POST":
        link = request.form.get('link')
        hook = request.form.get('webhook')
        group = request.form.get('group')
        icon = request.form.get('icon')
        print(f"Sending list {link} to {hook} for {group}")
        wh = Webhook(hook)

        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            cards = soup.find_all(class_="masonry__item")
            for card in cards:
                try:
                    img = card.find("img")['src']
                    imageUrl = f"https://supremecommunity.com/{img}"
                    name = card.find(class_="name item-details item-details-title")
                    price = card.find(class_="label-price")
                    ratio = card.find(class_="upvotesratio hidden")
                    embed = Embed(title=f"{name.text}", description="", color=0xff2b2b, timestamp="now")
                    try:
                        embed.set_image(url=imageUrl)
                    except:
                        print("no image")
                    try:
                        embed.add_field(name="Price", value=f"{price.text}", inline=False)
                    except:
                        embed.add_field(name="Price", value=f"No Prices Yet", inline=False)
                    try:
                        embed.add_field(name="Vote Ratio", value=f"{str(ratio.text)[:5]}% Positive", inline=False)
                    except:
                        print("no ratio")
                    embed.set_footer(f"connorstevens#0001 x {group}", icon_url=f"{icon}")
                    wh.send(embed=embed)
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
        return render_template("index.html")

if __name__ == '__main__':
    app.run(host="scraper.connorstevens.tech", port=5000, threaded=True)