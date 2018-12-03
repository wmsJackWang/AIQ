class desc():
    
    def __init__(self):
        # Initial setup
        self.observation = None
        self.reward_step = 0
        self.reward_total = 0
        self.done = None
        self.results = []
        self.info = None
        self.init = False
    

class header():
    
    def __init__(self, env_name, input_dim, output_dim, info, rl):
        self.env_name = env_name
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.info = info
        self.rl = rl

    