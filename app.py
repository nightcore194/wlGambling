import json, requests
from flask import Flask, request, render_template
from models import *

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///linkBuyersDB.db"
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def mainPage():
    return render_template("index.html")

@app.route('/link/create', methods=["GET","POST"])
def addLink(): # inserting link, that affiliated with buyers
    if request.method == 'POST':
        linkoffer = LinkOffer(
            link=request.form['link'],
            naviBar=True if request.form['naviBar'] == 'on' else False,
            offer=request.form['offer']
        )
        db.session.add(linkoffer)
        db.session.commit()
    return render_template("addLink.html")

@app.route('/link/get')
def getLink():# getting all existing links
    links = db.session.execute(db.select(LinkOffer).order_by(LinkOffer.link)).scalars()
    return links

@app.route('/getReferrer')
def getReferrer():  # sending request to App store API and getting response
    isMatched, offerUrl, naviBar = ''
    # getting request arguments
    ip = request.args.get("ip", type=str)
    # sending request to App store API
    # TODO
    # handle response of App store API
    # TODO
    # formatting data
    # TODO
    # formatting body of response
    bodyResopnse = {"isMatched": isMatched,
            "Url": offerUrl,
            "naviBar": naviBar}
    return json.dumps(bodyResopnse)

@app.route('/actionPostback')
def actionPostback():
    # getting request arguments
    action = request.args.get("action", type=str)
    link_id = request.args.get("link_id", type=int)
    # making a note in db
    linkstat = LinkStatistic(action=action, linkOffer=db.session.execute(db.select(LinkOffer).where(LinkOffer.id==link_id)))
    db.session.add(linkstat)
    db.session.commit()
    return 'success!'

@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    # getting a data from db
    stat_by_action = {"click": db.session.execute(db.select(db.count(LinkStatistic)).where(LinkStatistic.action == "click")),
                      "install": db.session.execute(db.select(db.count(LinkStatistic)).where(LinkStatistic.action == "install")),
                      "reg": db.session.execute(db.select(db.count(LinkStatistic)).where(LinkStatistic.action == "reg")),
                      "dep": db.session.execute(db.select(db.count(LinkStatistic)).where(LinkStatistic.action == "dep"))}
    # make a filter
    if request.method == "POST":
        stat_by_action = {
            "click": db.session.execute(db.select(db.count(LinkStatistic)).where(LinkStatistic.action == "click" and LinkStatistic.linkOffer == request.form['link_id'])),
            "install": db.session.execute(db.select(db.count(LinkStatistic)).where(LinkStatistic.action == "install" and LinkStatistic.linkOffer == request.form['link_id'])),
            "reg": db.session.execute(db.select(db.count(LinkStatistic)).where(LinkStatistic.action == "reg" and LinkStatistic.linkOffer == request.form['link_id'])),
            "dep": db.session.execute(db.select(db.count(LinkStatistic)).where(LinkStatistic.action == "dep" and LinkStatistic.linkOffer == request.form['link_id']))}
    return render_template("statLink.html", stat=stat_by_action)

if __name__ == '__main__':
    app.run()
