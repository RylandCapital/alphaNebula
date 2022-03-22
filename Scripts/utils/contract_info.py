class ContractInfo:
    def __init__(self):
        self.clusters = {
            "testnet": {
                "clusters": {"MAU": "terra1rhuwcluvgnql4f0xlhzmxlrgk22q65ym646sk2",},
                "chain_id": "bombay-12",
                "chain_url": "https://bombay-fcd.terra.dev/",
            }
        }
        self.dexes = {
            "astro": {
                # docs: https://docs.astroport.fi/astroport/
                "router": {
                    "mainnet": "terra16t7dpwwgx9n3lq6l6te3753lsjqwhxwpday9zx",
                    "testnet": "terra13wf295fj9u209nknz2cgqmmna7ry3d3j5kv7t4",
                },
                "luna-ust": {"mainnet": "terra1m6ywlgn6wrjuagcmmezzz2a029gtldhey5k552"},
            },
            "terraswap": {
                # docs: https://docs.terraswap.io/
                "router": {
                    "mainnet": "terra19qx5xe6q9ll4w0890ux7lv2p4mf3csd4qvt3ex",
                    "testnet": "terra14z80rwpd0alzj4xdtgqdmcqt9wd9xj5ffd60wp",
                },
                "luna-ust": {"mainnet": "terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6"},
            },
            "loop": {
                # docs: https://docs.loop.markets/loop-finance/
                "router": {},
                "luna-ust": {"mainnet": "terra1sgu6yca6yjk0a34l86u6ju4apjcd6refwuhgzv"},
            },
        }
