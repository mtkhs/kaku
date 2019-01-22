from kaku.line import LinePlugin

class Parrot( LinePlugin ):

    def bot_construct( self ):
        print( "-- Parrot.bot_construct" )
        pass

    def on_message( self, reply_token, message ):
        print( "-- Parrot.on_message" )
        messages = [
            {
                'type': 'text',
                'text': message
            }
        ]
        self.reply_message( reply_token, messages )

