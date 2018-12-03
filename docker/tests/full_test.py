### Ideal functionality
import yaml
import time
import sys
sys.path.insert(0, "/home/chris/Desktop/github/AIQ")

### Import AIQ package
from AIQ.AIQ import AIQ
# from AIQ import agent_class

def main():
    #Import username and password
    credentials = yaml.safe_load(open("credentials.yml"))

    username = credentials['username']
    password = credentials['password']

    # Single Call
    interface = AIQ(username, password)
    
    # Check login data
    '''
    if not interface.connect():
        print("Invalid login Credentials")
        exit()
    '''

    # Load test suite
    interface.add('CartPole_new')
    interface.add('MSPackman')
    # interface.add('RPM')

    # What if it is not in set?
    interface.add('none_test')

    # Set our agent
    # Overloads agent class
    #TODO add this
    # interface.agent = agent_class()

    interface.evaluate()
    
    print(interface.results)

    #TODO edit machine side to make work
    interface.submit()
    exit()

if __name__ == '__main__':
    main()