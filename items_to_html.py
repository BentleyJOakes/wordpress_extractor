import ast
import json
from datetime import datetime

class HTMLCreator:

    def __init__(self):
        pass

    def parse(self, filename):

        output_dir = "output/"
        date_format = "%B %d, %Y"

        print("Parsing: " + filename)
        with open(filename) as f:

            lines = json.load(f)
            lines = sorted(lines, key = lambda x : datetime.strptime(x['date'], date_format))
            lines = reversed(lines)
            lines = [l for l in lines]
            for i, j in enumerate(lines):
                # print(line)
                #print(j['date'])
                prev_entry = None
                next_entry = None

                if i > 0:
                    next_entry = lines[i-1]
                if i < len(lines) - 1:
                    prev_entry = lines[i+1]

                # print(j)
                # print(j['title'])
                tags = [t for t in j['tags'] if "Comments" not in t]


                def sani_title(t):
                    return t.replace("?", "")

                new_filename = output_dir + str(len(lines) - i) + "_" + sani_title(j["title"]) + ".html"
                print("Creating file: " + new_filename)
                with open(new_filename, 'w') as g:
                    g.write(f"<html><head><title>{j['title']}</title></head>")
                    g.write("<body>")
                    g.write("""
<style>
body {
  background-image: url('index.jpeg');
}
</style> """)
                    g.write(f"<h1 style='text-align:center;'>{j['title']}</h1><br>")
                    g.write(f"By <b>{j['author']}</b> on <b>{j['date']}</b><br>")

                    def write_prev_next():
                        if prev_entry:
                            prev_title = sani_title(prev_entry['title'])
                            prev_filename = str(len(lines) - i - 1) + "_" + prev_title + ".html"
                            g.write(f"Previous: <a href='{prev_filename}'>{prev_entry['title']}</a>    ")
                        if next_entry:
                            next_title = sani_title(next_entry['title'])
                            next_filename = str(len(lines) - i + 1) + "_" + next_title + ".html"
                            g.write(f"Next: <a href='{next_filename}'>{next_entry['title']}</a>")
                            g.write("<br>")
                    write_prev_next()
                    g.write(f"{j['content']}<br>")
                    g.write(f"Tags: {tags}<br>")
                    write_prev_next()
                    g.write("</body></html>")

if __name__ == "__main__":

    filename = "items.json"
    c = HTMLCreator()
    c.parse(filename)

