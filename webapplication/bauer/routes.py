from flask import Flask, render_template, url_for, flash, redirect, request, session, send_file, send_from_directory
from bauer import app
# this is an example of how the models can be put on the front end
from bauer.forms import RPNExpressionIngestor
from bauer.models import PortfolioItem
from bauer.markdown_renderer import MarkdownIngestor
from backend import main
import os

@app.route("/", methods=['GET', 'POST'])
def calculator():
    """
    A very basic interface to work with backend code. 
    This was the hardest part of the Flask component.
    Here we know we can access the function from backend.main
    The rest is just front end components.
    Results are currently printed to the console, please take this ouput and try to put it somewhere other than the console.
    """
    calculator_ = RPNExpressionIngestor(request.form)
    if(calculator_.validate_on_submit()):
        expr_ = calculator_.expression_.data
        main.rpn_calculator(expr_)
        if(not main.stack_.is_empty()):
          # output generated here
          try: print("\t{0:.15f}".format(main.stack_.peek()))
          except IndexError: print("\tstack is empty")
        main.stack_.clear_contents()
        return redirect(url_for('calculator'))
    return render_template('calculator.html', form=RPNExpressionIngestor(request.form), title="Bauer")

@app.route("/about")
def about():
    content = MarkdownIngestor("bauer/ABOUT_README.md").formatted_contents
    return render_template('about.html', AboutPageContent=content)

