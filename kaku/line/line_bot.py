import requests
import json
import importlib
import os

class LineBot():

    def __init__( self, setting ):
        print( "-- __init__()" )
        channel_secret = setting[ 'line' ][ 'channel_secret' ]
        access_token = setting[ 'line' ][ 'access_token' ]
        plugins_dir = setting[ 'bot' ][ 'plugins_dir' ]
        plugins_setting = setting[ 'plugins' ]

        self.CHANNEL_SECRET = channel_secret
        self.ACCESS_TOKEN = access_token
        self.API_PREFIX = 'https://api.line.me/v2/bot'
        self.HEADER = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.ACCESS_TOKEN
        }
        self.plugins_setting = plugins_setting
        self.plugins_dir = plugins_dir
        self.plugin_modules = []
        self.plugin_classes = []
        self.plugin_instances = []

    def load_plugins( self ):
        for ps in self.plugins_setting:
            mod = importlib.import_module( self.plugins_dir + '.' + ps[ 'module' ] )
            klass_name = ps[ 'name' ]
            klass = getattr( mod, klass_name )
            self.plugin_classes.append( klass )
            self.plugin_instances.append( klass( self, ps ) )

    def load_plugins_filename_based( self ):
        plugins_dir = os.listdir( self.plugins_dir )
        for filename in plugins_dir:
            if filename.endswith('.py'):
                if filename == "__init__.py":
                    continue
                klass_name = os.path.splitext( filename )[ 0 ]
                klass_name = klass_name[ 0 ].upper() + klass_name[ 1: ]
                modulePath =  self.plugins_dir + '/' + filename
                cpath = os.path.splitext( modulePath )[ 0 ].replace( os.path.sep, '.' )
                try:
                    mod = importlib.import_module( cpath )
                    self.plugin_modules.append( mod )
                    klass = getattr( mod, klass_name )
                    self.plugin_classes.append( klass )
                    self.plugin_instances.append( klass( self, klass_name ) )
                except ModuleNotFoundError:
                    print( 'Module not found' )
                except AttributeError:
                    print( 'Method not found' )

    def unload_plugins( self ):
        for ins in self.plugin_instances:
            del( ins )
        self.plugin_instances = []

        for cls in self.plugin_classes:
            del( cls )
        self.plugin_classes = []

        for mod in self.plugin_modules:
            del( mod )
        self.plugin_modules = []

    def reload_plugins( self ):
        self.unload_plugins()
        self.load_plugins()

    def reply_message( self, reply_token, messages ):
        print( "-- reply_message()" )
        payload = {
            "replyToken": reply_token,
            "messages": messages,
        }
        requests.post( self.API_PREFIX + '/message/reply', headers = self.HEADER, data = json.dumps( payload ) )

    def on_message( self, event ):
        print( "-- on_message()" )

        reply_token = event[ 'replyToken' ]
        message = event[ 'message' ][ 'text' ]

        for plugin in self.plugin_instances:
            plugin.on_message( reply_token, message )

    def on_sticker( self, event ):
        pass

    def on_image( self, event ):
        pass

    def on_video( self, event ):
        pass

    def on_audio( self, event ):
        pass

    def on_action( self, event ):
        pass

    def process_event( self, event ):
        print( "-- process_event()" )
        if event[ 'type' ] == 'message':
#            self.process_message( event )
            self.on_message( event )
        elif event[ 'type' ] == 'sticker':
#            self.process_sticker( event )
            self.on_sticker( event )
        elif event[ 'type' ] == 'image':
            self.on_image( event )
        elif event[ 'type' ] == 'video':
            self.on_video( event )
        elif event[ 'type' ] == 'audio':
            self.on_audio( event )
        elif event[ 'type' ] == 'action':
            self.on_action( event )
        else:
            print( "unknown event type:" + event[ 'type' ] )

    def on_callback( self, request ):
        print( "-- on_callback()" )
        for event in request.json[ 'events' ]:
            self.process_event( event )

    def start( self ):
        self.load_plugins()

