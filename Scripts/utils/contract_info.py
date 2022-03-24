class ContractInfo:

    def __init__(self):
        self.clusters = {
                'testnet': {
                    'clusters':{
                        'MAU':'terra1rhuwcluvgnql4f0xlhzmxlrgk22q65ym646sk2',
                    },
                    'chain_id':'bombay-12',
                    'chain_url':'https://bombay-fcd.terra.dev/'
                }
            }
        self.dexes = {
            'astro': {
                # docs: https://docs.astroport.fi/astroport/
                'router': {
                    'mainnet': 'terra16t7dpwwgx9n3lq6l6te3753lsjqwhxwpday9zx',
                    'testnet': 'terra13wf295fj9u209nknz2cgqmmna7ry3d3j5kv7t4'
                },
                'luna-ust': {
                    'mainnet': 'terra1m6ywlgn6wrjuagcmmezzz2a029gtldhey5k552'
                },
                'anc-ust': {
                    'mainnet':'terra1qr2k6yjjd5p2kaewqvg93ag74k6gyjr7re37fs'
                },
                'lunax-luna': {
                    'mainnet':'terra1qswfc7hmmsnwf7f2nyyx843sug60urnqgz75zu'
                },
                'mars-ust': {
                    'mainnet':'terra19wauh79y42u5vt62c5adt2g5h4exgh26t3rpds'
                }  
                
            },
            'terraswap': {
                # docs: https://docs.terraswap.io/
                'router': {
                    'mainnet': 'terra19qx5xe6q9ll4w0890ux7lv2p4mf3csd4qvt3ex',
                    'testnet': 'terra14z80rwpd0alzj4xdtgqdmcqt9wd9xj5ffd60wp'
                },
                'luna-ust': {
                    'mainnet': 'terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6'
                },
                'anc-ust': {
                    'mainnet':'terra1gm5p3ner9x9xpwugn9sp6gvhd0lwrtkyrecdn3'
                },
                'lunax-luna': {
                    'mainnet':'terra1zrzy688j8g6446jzd88vzjzqtywh6xavww92hy'
                },
                'mars-ust': {
                    'mainnet':'terra15sut89ms4lts4dd5yrcuwcpctlep3hdgeu729f'
                }    
            },
            'loop': {
                # docs: https://docs.loop.markets/loop-finance/
                'router': {
                },
                'luna-ust': {
                    'mainnet': 'terra1sgu6yca6yjk0a34l86u6ju4apjcd6refwuhgzv'
                },
                'anc-ust': {
                    'mainnet':'terra1f6d3pggq7h2y7jrgwxp3xh08yhvj8znalql87h'
                },
                'lunax-luna': {
                    'mainnet':'terra1ga8dcmurj8a3hd4vvdtqykjq9etnw5sjglw4rg'
                }
            }
        }


