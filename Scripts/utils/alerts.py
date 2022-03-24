import os



DISCORD_LUNAUST = os.getenv("DISCORD_LUNAUST")
DISCORD_ANCUST = os.getenv("DISCORD_ANCUST")
DISCORD_LUNAXLUNA = os.getenv("DISCORD_LUNAXLUNA")
DISCORD_MARSUST = os.getenv("DISCORD_MARSUST")


class Discord:

    def __init__(self):
        self.webhooks = {
            'luna-ust': DISCORD_LUNAUST,
            'anc-ust': DISCORD_ANCUST,
            'lunax-luna': DISCORD_LUNAXLUNA,
            'mars-ust': DISCORD_MARSUST

        }
