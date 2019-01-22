import toml
from kaku.line import LineBot
from flask import Flask, request

LINE_SETTINGS = toml.load( open( 'line_settings.toml' ) )

app = Flask( __name__ )
lb = LineBot( LINE_SETTINGS )
lb.start()

@app.route( "/callback", methods = [ 'POST' ] )
def callback():
    lb.on_callback( request )
    return "Success"

if __name__ == "__main__":
    port = 5000 # TODO: LINE_SETTINGS
    app.run( debug = True, host = '0.0.0.0', port = port )

