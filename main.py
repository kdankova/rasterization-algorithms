import streamlit as st
import plotly.express as px
import pandas as pd


def draw_cda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps

    points = [(round(x1 + i * x_increment), round(y1 + i * y_increment)) for i in range(steps + 1)]
    return points


def draw_bresenham(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    slope = dy / dx

    x, y = x1, y1
    points = [(x, y)]

    if slope <= 1:
        p = 2 * dy - dx
        for _ in range(dx):
            x += 1
            if p < 0:
                p += 2 * dy
            else:
                y += 1
                p += 2 * (dy - dx)
            points.append((x, y))
    else:
        p = 2 * dx - dy
        for _ in range(dy):
            y += 1
            if p < 0:
                p += 2 * dx
            else:
                x += 1
                p += 2 * (dx - dy)
            points.append((x, y))

    return points


def draw_circle_bresenham(xc, yc, r):
    x = 0
    y = r
    d = 3 - 2 * r

    points = []

    def plot_points(x, y):
        points.extend([(xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
                       (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)])

    plot_points(x, y)
    while y > x:
        x += 1

        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6

        plot_points(x, y)

    return points


def draw_dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps

    points = [(round(x1 + i * x_increment), round(y1 + i * y_increment)) for i in range(steps + 1)]
    return points


st.title("Raster Algorithms")

x1, y1 = st.number_input("Enter x1:", 0), st.number_input("Enter y1:", 0)
x2, y2 = st.number_input("Enter x2:", 10), st.number_input("Enter y2:", 10)

algorithm = st.selectbox("Select an algorithm:", ["DDA", "Bresenham (Line)", "Bresenham (Circle)", "CDA"])

fig = px.scatter(title='Scalable Coordinate Grid')

fig.update_layout(
    xaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=False),
    yaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=False)
)

if algorithm == "CDA":
    points = draw_cda(x1, y1, x2, y2)
elif algorithm == "Bresenham (Line)":
    points = draw_bresenham(x1, y1, x2, y2)
elif algorithm == "Bresenham (Circle)":
    radius = st.number_input("Enter the radius of the circle:", 5)
    points = draw_circle_bresenham(x1, y1, radius)
else:
    points = draw_dda(x1, y1, x2, y2)

df = pd.DataFrame(points, columns=['x', 'y'])

fig.add_scatter(x=df['x'], y=df['y'], mode='markers', marker=dict(size=8, color='plum'))

st.plotly_chart(fig)
