from flask import Flask,render_template,request
from pandas_datareader import data
from dateutil import parser
from bokeh.embed import components
from bokeh.resources import CDN
from plot import plot_candlestick,plot_moving_avg

app = Flask(__name__)


plot_names = ['Candlestick','One-Month Average']
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data', methods=['POST'])
def data_extraction():
    if request.method == 'POST':
        global df
        global current_plot_name
        cname = request.form['company_symbol']
        d_start = parser.parse(request.form["start_date"])
        d_end = parser.parse(request.form["end_date"])
        df = data.DataReader(name=cname, data_source="yahoo", start=d_start,
                             end=d_end)  # start,end parameter must have datetime datatype
        current_plot_name = request.args.get("plot_name")

        def inc_dec(c, o):  # c=close,o=open
            if c > o:
                value = "Increase"
            elif c < o:
                value = "Decrease"
            else:
                value = "Equal"
            return value

        df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]  # list is assigned to dataframe
        df["Middle"] = (df.Open + df.Close) / 2
        df["Height"] = abs(df.Close - df.Open)
        df["Time"] = 12 * 60 * 60 * 1000

        if current_plot_name == None:
            current_plot_name = "Candlestick"

        plot = create_figure(current_plot_name,df)

        # Embed plot into HTML via Flask Render
        script, div = components(plot)
        cdn_js = CDN.js_files[0]
        cdn_css = CDN.css_files[0]
    return render_template("plot.html", plot_names=plot_names,current_plot_name=current_plot_name,script=script,div=div,
                           cdn_js=cdn_js,cdn_css=cdn_css)


@app.route('/plot')
def plot():
    current_plot_name = request.args.get("plot_name")
    if current_plot_name == None:
        current_plot_name = "Candlestick"

    plot = create_figure(current_plot_name,df)

    script, div = components(plot)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    
    return render_template("plot.html",plot_names=plot_names,current_plot_name=current_plot_name,script=script,div=div,
                           cdn_js=cdn_js,cdn_css=cdn_css)


def create_figure(current_plot_name,df):
    if current_plot_name == 'Candlestick':
        p=plot_candlestick(df)
        return p
    elif current_plot_name == 'One-Month Average':
        p=plot_moving_avg(df)
        return p

def new():
    data_extraction()

if __name__== "__main__":
    app.run(debug=True)