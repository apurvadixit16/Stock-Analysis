from bokeh.plotting import figure
import numpy as np
from bokeh.models import HoverTool,ColumnDataSource

def plot_candlestick(df):
    source_seg = ColumnDataSource({'x':df.index,'y':df['High'],'x_':df.index,'y_':df['Low'],
                                   'open': df['Open'], 'close': df['Close'],
                                  'high': df['High'], 'low': df['Low']})

    source_rect_r = ColumnDataSource({'left':df.index[df.Status == "Increase"],
                                  'top':df.Middle[df.Status == "Increase"],
                                  'right':df['Time'],
                                  'bottom':df.Height[df.Status == "Increase"],
                                  'open': df['Open'], 'close': df['Close'],
                                  'high': df['High'], 'low': df['Low']})

    source_rect_g = ColumnDataSource({'left':df.index[df.Status == "Decrease"],
                                  'top':df.Middle[df.Status == "Decrease"],
                                  'right':df['Time'],
                                  'bottom':df.Height[df.Status == "Decrease"],
                                  'open': df['Open'], 'close': df['Close'],
                                  'high': df['High'], 'low': df['Low']})

    hover = HoverTool(tooltips=[('HIGH', '@high'),
                                ('LOW', '@low'),
                                ('OPEN', '@open'),
                                ('CLOSE', '@close')])



    p = figure(x_axis_type='datetime',x_axis_label="Dates",  y_axis_label="Price",width=1000, height=300,
               sizing_mode="scale_width")  # sizing_mode:-adjst according to window size
    p.title.text = "Candlestick Chart"
    p.title.align = "center"
    p.title.text_font = "times"
    p.title.text_font_style = "bold"
    p.title.text_font_size = "25px"
    p.grid.grid_line_alpha = 0.3

    p.add_tools(hover)


    p.segment(x0='x',y0='y',x1='x_',y1='y_',source=source_seg, color="Black")

    p.rect(x='left',y='top',width='right',height='bottom',source=source_rect_r, fill_color="#CCFFFF", line_color="black")
    p.rect(x='left',y='top',width='right',height='bottom',source=source_rect_g, fill_color="#FF3333", line_color="black")
    # show(p)
    # output_file("p.html")
    return p

def plot_moving_avg(df):
    window_size =30
    stock_dates = np.array(df.index, dtype=np.datetime64)
    df['dates'] = stock_dates
    stock_close = df['Adj Close']
    window = np.ones(window_size) / float(window_size)
    stock_avg_o = np.convolve(stock_close, window, 'same')

    data = {'x':stock_dates, 'y':stock_avg_o}
    source = ColumnDataSource(data)
    hover = HoverTool(tooltips=[('Stock Avg', '@y')])
    p = figure(x_axis_type='datetime', x_axis_label="Dates",y_axis_label="Close price", width=1000, height=300,
               sizing_mode="scale_width")  # sizing_mode:-adjst according to window size
    p.title.text = "Moving Average Chart"
    p.title.align = "center"
    p.title.text_font = "times"
    p.title.text_font_style = "bold"
    p.title.text_font_size = "25px"
    p.grid.grid_line_alpha = 0.3
    p.line(x='x',y='y', color='red',source=source)
    p.add_tools(hover)

    return p