from app import create_app
app=create_app()
app.jinja_env.add_extension('jinja2.ext.loopcontrols') 


if __name__=="__main__":
    app.run(use_reloader=False)
