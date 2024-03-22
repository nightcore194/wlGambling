import json, requests
from flask import Flask, request, render_template
from models import *
from settings import DB_DESTINITION

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_DESTINITION}"
db.init_app(app)
migrate.init_app(app)

@app.route('/') # main page
def mainPage():
    return render_template("index.html")

@app.route('/link/create', methods=["GET","POST"])
def addLink(): # inserting link, that affiliated with buyers
    if request.method == 'POST':
        db.session.add(LinkOffer(
            link=request.form['link'],
            naviBar=True if request.form['naviBar'] == 'on' else False,
            offer=request.form['offer']
        ))
        db.session.commit()
    return render_template("addLink.html")

@app.route('/link/get')
def getLink():# getting all existing links
    links = db.session.query(LinkOffer)
    return render_template("getLink.html", links=links)

@app.route('/getReferrer')
def getReferrer():  # sending request to App store API and getting response
    isMatched, offerUrl, naviBar = ''
    # getting request arguments
    ip = request.args.get("ip", type=str)
    # sending request to App store API
    # TODO https://developer.apple.com/documentation/appstoreconnectapi/power_and_performance_metrics_and_logs
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
    LinkOffer.query.filter_by(link='1').count()
    # getting a data from db
    stat_by_action = {"click": db.session.query(LinkStatistic).filter_by(action="click").count(),
                      "install": db.session.query(LinkStatistic).query.filter_by(action="install").count(),
                      "reg": db.session.query(LinkStatistic).query.filter_by(action="reg").count(),
                      "dep": db.session.query(LinkStatistic).query.filter_by(action="dep").count()}
    # make a filter
    if request.method == "POST":
        stat_by_action = {
            "click": db.session.query(LinkStatistic).query.filter_by(action="dep", linkoffer=request.form['link_id']).count(),
            "install": db.session.query(LinkStatistic).query.filter_by(action="install", linkoffer=request.form['link_id']).count(),
                      "reg": db.session.query(LinkStatistic).query.filter_by(action="reg", linkoffer=request.form['link_id']).count(),
                      "dep": db.session.query(LinkStatistic).query.filter_by(action="dep", linkoffer=request.form['link_id']).count()}
    return render_template("getLink.html", stats=stat_by_action)

if __name__ == '__main__':
    app.run()
