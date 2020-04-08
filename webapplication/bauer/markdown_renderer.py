import markdown
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter

class MarkdownIngestor():
    def __init__(self, path: str):
        self.path = path
        self.markdown_contents = self.read_contents()
        self.formatted_contents = self.format_contents()
    def read_contents(self):
        try:
            with open(self.path, "r") as f: return f.read()
                
        except Exception as error:
            print("[-] Could not read the contents of {}\nError: {}".format(
                self.path, error
            ))
            return None
            
    def format_contents(self):

        md_template = markdown.markdown(
            self.markdown_contents, extensions=["fenced_code", "codehilite"]
        )

        # Generate css for syntax highlighting
        formatter = HtmlFormatter(style="friendly", full=True, cssclass="codehilite")
        md_css = "<style>{}</style>".format(formatter.get_style_defs())

        return "{}{}".format(md_css, md_template)
