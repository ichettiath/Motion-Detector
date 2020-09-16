from MotionDetect import Enter_Exit_Times
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import DatetimeTickFormatter

Enter_Exit_Times["Enter_line"] = Enter_Exit_Times["Enter"].dt.strftime("%m/%d %H:%M:%S.%f")
Enter_Exit_Times["Exit_line"] = Enter_Exit_Times["Exit"].dt.strftime("%m/%d %H:%M:%S.%f")

timeData = ColumnDataSource(Enter_Exit_Times)

output_file("Motion_Graph.html")

x = Enter_Exit_Times["Enter"]

#creates the plotting graph
p = figure(height = 400, width = 1250, title = "Times of Motion")
p.yaxis.minor_tick_line_color = None
p.yaxis.visible = False
p.xaxis.axis_label = "Time after start"
p.xaxis.formatter=DatetimeTickFormatter(
        hours = ["%H:%M:%S"],
        days = ["%m/%d %H:%M:%S"],
        months = ["%m/%d %H:%M:%S"],
        seconds = ["%H:%M:%S"],
        milliseconds = ["%H:%M:%S.%f"]
    )

hover = HoverTool(tooltips = [("Enter", "@Enter_line"), ("Exit", "@Exit_line")])
p.add_tools(hover)

q = p.quad(left = "Enter", right = "Exit", bottom = 0, top = 1, color = "blue", source = timeData)

show(p)