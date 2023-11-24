from flask import render_template


class MainController:

    def root(self):
        return render_template("base.html")





