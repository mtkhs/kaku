
class LinePlugin():

    def __init__( self, bot, setting ):
        self.bot = bot
        self.setting = setting
        self.bot_construct()

    def __del__( self ):
        self.bot_destruct()

    def bot_construct( self ):
        pass

    def bot_destruct( self ):
        pass

    def reply_message( self, reply_token, message ):
        self.bot.reply_message( reply_token, message )

    # abstract methods

    def on_message( self, reply_token, message ):
        pass

    def on_raw( self, raw ):
        pass
