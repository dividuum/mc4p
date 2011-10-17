
from plugins import MC3Plugin, msghdlr

class MutePlugin(MC3Plugin):
    """Lets the client mute players, hiding their chat messages.
    
    The client controls the plugin with chat commands:
        /mute NAME      Hide all messages from player NAME.
        /unmute NAME    Allow messages from player NAME.
        /muted          Show the list of currently muted players.
    """
    def init(self, args):
        self.muted_set = set() # Set of muted player names.

    def send_chat(self, chat_msg):
        """Send a chat message to the client."""
        self.to_client({'msgtype': 0x03, 'chat_msg': chat_msg})

    def mute(self, player_name):
        self.muted_set.add(player_name)
        self.send_chat('Muted %s' % player_name)

    def unmute(self, player_name):
        if player_name in self.muted_set:
            self.muted_set.remove(player_name)
            self.send_chat('Unmuted %s' % player_name)
        else:
            self.send_chat('%s is not muted' % player_name)

    def muted(self):
        self.send_chat('Currently muted: %s' % ', '.join(self.muted_set))

    @msghdlr(0x03)
    def handle_chat(self, msg, source):
        txt = msg['chat_msg']
        if source == 'client':
            # Handle mute commands
            if txt.startswith('/mute '):     self.mute(txt[len('/mute '):])
            elif txt.startswith('/unmute '): self.unmute(txt[len('/unmute '):])
            elif txt == '/muted':            self.muted()
            else: return True # Forward all other chat messages.

            return False # Drop mute plugin commands.
        else:
            # Drop messages containing the string <NAME>, where NAME is a muted player name.
            return not any(txt.startswith('<%s>' % name) for name in self.muted_set)

