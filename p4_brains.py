
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.resource = False

  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.)
    #message commands - 'order', 'collide', 'timer'
    #detail are key commands/objects for collision
    print details
    print type(details)
    
    if self.body.amount < 0.5:
        self.state = "fleeing"
        self.body.go_to(self.body.find_nearest("Nest"))
      
    #moving 'right click'
    if self.state is "moving":
        if message is "order":
            self.do_order(details)
        elif message is 'collide':
            pass
        elif message is "timer":
            pass
    #idle 'i'
    elif self.state is "idle":
        if message is "order":
            self.do_order(details)
        elif message is 'collide':
            pass
        elif message is "timer":
            pass
    #attack 'a'
    elif self.state is "attacking":
        if message is "order":
            self.do_order(details)
        elif message is 'collide':
            if details["what"] is "Mantis":
                mantis = details["who"]
                mantis.amount -= 0.05
        elif message is "timer":
            self.target = self.body.find_nearest("Mantis")
            self.body.follow(self.target)
            self.body.set_alarm(1)
    #build 'b'
    elif self.state is "building":
        if message is "order":
            self.do_order(details)
        elif message is 'collide':
            if details["what"] == "Nest":
                nest = details["who"]
                nest.amount += 0.01
        elif message is "timer":
            self.target = self.body.find_nearest("Nest")
            self.body.set_alarm(1)
            self.body.go_to(self.target)
    #harvest 'h'
    elif self.state is "harvesting": 
        if message is "order":
            self.do_order(details)
        elif message is 'collide':
            if self.resource:
                if details["what"] == "Nest":
                    self.resource = False
            else: #not carrying a resource
                if details["what"] == "Resource":
                    resource = details["who"]
                    resource.amount -= 0.25
                    self.resource = True
        elif message is "timer":
            if self.resource:
                self.target = self.body.find_nearest("Nest")
                self.body.set_alarm(1)
                self.body.go_to(self.target)
            else: #not carrying a resource
                self.target = self.body.find_nearest("Resource")
                self.body.go_to(self.target)
                self.body.set_alarm(1)
    #flee low health
    elif self.state is "fleeing":
        if message is "order":
            self.do_order(details)
        if message is "collide":
            if details["what"] == "Nest":
                self.body.amount = 1    
    
  def do_order(self, details): #chooses the correct command method
        if details == 'i':
            self.state = 'idle'
            self.body.stop()
        elif details == 'h':
            self.state = 'harvesting'
            self.body.set_alarm(0)
        elif details == 'a':
            self.state = 'attacking'
            self.body.set_alarm(0)
        elif details == 'b':
            self.state = 'building'
            self.body.set_alarm(0)
        elif isinstance(details, tuple):
            self.state = 'moving'
            self.body.go_to(details)
  def do_right_click(details):
      pass
  def do_i(details):
      pass
  def do_a(details):
      pass
  def do_b(details):
      pass
  def do_h(details):
      pass

world_specification = {
  #'worldgen_seed': 13, # comment-out to randomize
  'nests': 2,
  'obstacles': 25,
  'resources': 5,
  'slugs': 5,
  'mantises': 5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
