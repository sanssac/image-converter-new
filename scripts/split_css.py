import os

workspace = "c:\\image converter new"
css_path = os.path.join(workspace, "assets", "css", "style.css")

with open(css_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

def write_css(filename, start, end):
    with open(os.path.join(workspace, "assets", "css", filename), "w", encoding="utf-8") as f:
        f.write("".join(lines[start-1:end]))

# Break it down
write_css("base.css", 1, 34)
write_css("layout.css", 35, 72)
with open(os.path.join(workspace, "assets", "css", "layout.css"), "a", encoding="utf-8") as f:
    f.write("".join(lines[193:204]))

# Components
write_css("components.css", 73, 193)
with open(os.path.join(workspace, "assets", "css", "components.css"), "a", encoding="utf-8") as f:
    f.write("".join(lines[205:412]))
    f.write("".join(lines[606:638]))
    f.write("".join(lines[646:738]))
    f.write("".join(lines[760:773]))

# Utilities (Animations, Media Queries, Light Theme)
write_css("utilities.css", 412, 605)
with open(os.path.join(workspace, "assets", "css", "utilities.css"), "a", encoding="utf-8") as f:
    f.write("".join(lines[639:646]))
    f.write("".join(lines[739:759]))

print("CSS split successfully.")
