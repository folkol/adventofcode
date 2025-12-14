from PIL import Image, ImageDraw

with open('input.dat') as f:
    points = [
        tuple(map(int, line.split(',')))
        for line in f
    ]

xs, ys = zip(*points)
min_x, min_y = min(xs), min(ys)

points = [(x - min_x,  y - min_y) for x, y in points]

w = max(x for x, _ in points) + 1
h = max(y for _, y in points) + 1

points = [(50 + x / 100, 50 + y / 100) for x, y in points]

img = Image.new("RGB", (100 + w // 100, 100 + h // 100), "white")
draw = ImageDraw.Draw(img)
draw.line(points, fill="black", width=2)

img.save("path.png")
