
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.resource = False

  def handle_event(self, message, details):

    if self.state is 'idle':

        if message == 'timer':
            if random.random() < 0.8:
                # go to a random point, wake up sometime in the next 10 seconds
                world = self.body.world
                x, y = random.random()*world.width, random.random()*world.height
                self.body.go_to((x,y))
                self.body.set_alarm(random.random()*10)
            else:
                self.state = "thievery"
                self.body.set_alarm(1)

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
            if self.target:
                self.body.follow(self.target)
            else:
                self.body.stop()
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
        self.body.radius += 0.1
        self.body.speed += 0.1
        
    elif self.state == "thievery":
        if self.resource:
            if message == "collide":
                if details["what"] == "Resource":
                    details["who"].amount += .15
                    self.resource = False
                if details["what"] == "Slug":
                     # a slug bumped into us; get curious
                     self.state = 'curious'
                     self.body.set_alarm(1) # think about this for a sec
                     self.body.stop()
                     self.target = details['who']
            elif message == "timer":
                resource = self.body.find_nearest("Resource")
                if resource:
                    self.body.go_to(resource)
                else:
                    self.body.stop()
                self.body.set_alarm(1)
        else:
            if message =="collide":
                if details["what"] == "Nest":
                    details["who"].amount -= .15
                    self.resource = True
                if details["what"] == "Slug":
                     # a slug bumped into us; get curious
                     self.state = 'curious'
                     self.body.set_alarm(1) # think about this for a sec
                     self.body.stop()
                     self.target = details['who']
            elif message == "timer":
                nest = self.body.find_nearest("Nest")
                if nest:
                    self.body.go_to(nest)
                else:
                    self.body.stop()
                self.body.set_alarm(1)
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
    
    if self.body.amount < 0.5:
        self.state = "fleeing"
        nest = self.body.find_nearest("Nest")
        if nest:
            self.body.go_to(nest)
        else:
            self.body.stop()
      
    #moving 'right click'
    if self.state is "moving":
        if message is "order":
            self.do_order(details)
    #idle 'i'
    elif self.state is "idle":
        if message is "order":
            self.do_order(details)
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
            if self.target:
                self.body.follow(self.target)
            else:
                self.body.stop()
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
            if self.target:
                self.body.go_to(self.target)
            else:
                self.body.stop()
            self.body.set_alarm(1)
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
                if self.target:
                    self.body.go_to(self.target)
                else:
                    self.body.stop()
                self.body.set_alarm(1)
            else: #not carrying a resource
                self.target = self.body.find_nearest("Resource")
                if self.target:
                    self.body.go_to(self.target)
                else:
                    self.body.stop()
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
