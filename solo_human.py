import pygame, sys, random ,os,math,time
from pygame.locals import *


num_inputs = 22     #number of inputs for humans 
nodes_per_layer = 20
num_layers = 3
universe_string = "Universe # (20x3), mutant clone LONE WOLF"
'''
nodes_per_layer = 20    #old brain
num_layers = 2
'''
num_outputs = 8
maxx = 500
maxy = 500
human_max = 1

zombie_list = []
safe_zone_list = []
human_list = []
human_corpse_list = []
food_list = []
zombie_corpse_list = []


class food:
    # used to keep humans alive.  Spawn randomly and stay until consumed
    def __init__(self):
        self.x = random.randint(0,maxx)
        self.y = random.randint(0,maxy)
    
class safe_zone:
    # Destructable buildings offer temporary safety for humans
    def __init__(self):
        self.x = random.randint(0,maxx - 50)
        self.y = random.randint(0,maxy - 50)
        self.life = 100.0 
        self.alive = True       
        
    
class human:
    def __init__(self,b):                                               #b:= brain to use
        self.food_level = 100
        self.food_sources = []
        self.safe_areas = []
        self.x = random.randint(0,maxx)
        self.y = random.randint(0,maxy)
        self.found = False
        self.searchx = random.randint(0,maxx)
        self.searchy = random.randint(0,maxy)
        self.heading = 0                                                #direction traveling
        self.alive = True
        self.life = 100
        self.infected = False                                           #currently infected
        self.zfound = False                                             #see other zombie variables
        self.zgoalx = 0                                                 #observed zombies (x,y)
        self.zgoaly = 0
        self.goalx = random.randrange(0,maxx)                           # where to search for food
        self.goaly = random.randrange(0,maxy)
        self.accuracy = 0.3                                             #attacking variables
        self.paranoia = 0.9                                             #starting very paranoid
        self.damage = 25                                                #damnage done per shot
        self.attack_delay = 0                                           #time between shots
        self.hgoalx = random.randrange(0,maxx)                          #see other human variables
        self.hgoaly = random.randrange(0,maxy)
        self.hfound = False                                     
        self.suicide = False
        self.bool_list = [False for i in range(num_inputs)]            #list of bools for sight 
        self.saw_zombie = 0
        self.hiding = False
        self.last_choice = -1
        self.consomption_rate = 0.005                                   #rate hunger progresses
        self.return_score = 0
        self.Brain = b
                                                                        #Below, return score for
        self.attack_counter = 0
        self.alive_timer = 0
        self.food_gathered = 0
        self.total_choice = 0     #how many choices did they make per simulation (based on "last_choice" which will initially change from -1)
        self.survived_timer = 0
        
        
    def end_score(self):
        
        bonus = 0   #bonus for mutli intelligent behavior test
        if self.attack_counter > 0 and self.food_gathered > 0:  
            bonus += 500     #bonus for getting food and attacking zombies
        #if self.infected == False and self.food_gathered > 0:
        #    bonus += 500      #bonus for few infections and getting food
        if self.attack_counter > 0 and self.food_gathered > 0 and self.infected == False:
            bonus += 1000    #attacked Z & got food & few infections
        if self.attack_counter > 0 and self.food_gathered > 0 and self.infected == False and self.food_level > 0:
            bonus += 2000    #attacked Z & got food & few infections & died full
        """
        if attack_counter > 0 and food_gathered == 0:   #penalize for not doing both

            bonus -= 100
        if attack_counter == 0 and food_gathered > 0:
            bonus -= 100
        if attack_counter <= 0 and food_gathered == 0:
            bonus -= 200
        """
        
        print "total_chocies =",self.total_choice
        print "attack_counter =", self.attack_counter/10
        print "end_food_lvl =",self.food_level
        print "infected =",self.infected
        print "suicide =",self.suicide
        print "bonus =",bonus
        print "food_gathered =",self.food_gathered
        print "alive_timer =",self.alive_timer/10
        print "SCORE =",self.attack_counter/10 + self.food_level - 10*self.infected + bonus + \
        5*self.food_gathered + self.alive_timer/10
        print
        
        
        return self.attack_counter/10 + self.food_level - 10*self.infected + bonus + \
        5*self.food_gathered + self.alive_timer/10
        

class Zed:
    def __init__(self):                                             #simple agent, random walk->follow target->attack
        self.food_level = 100
        self.life = 100
        self.x = random.randint(0,maxx)
        self.y = random.randint(0,maxy)
        self.heading = 0
        self.active = True                                          #zombie active or destored
        self.found = False
        self.searchx = random.randint(0,maxx)
        self.searchy = random.randint(0,maxy)
        
class brains:
    def __init__(self, inputs = 1, nodes_per_layer = 1, num_layers = 1, num_outputs = 1):
        self.inputs = inputs
        self.nodes_per_layer = nodes_per_layer
        self.num_layers = num_layers
        self.num_outputs = num_outputs
        

        layer_weight = []
        network = []                                                #list of all network objects
        
        for i in range(0,inputs):                                   #connecting input to first hidden layer
            input_weight = []
            
            for j in range(0,nodes_per_layer):
                node_weight = random.random() * 2.0 - 1             # -1 <= randint <= 1
                input_weight.append(node_weight)
                
            layer_weight.append(input_weight)
            
        network.append(layer_weight)
        
        
        for i in range(0,num_layers):                               #connecting inner layers together
            layer_weight = []                                       #reset layer weight to add to network
            for i in range(0,nodes_per_layer):                      #connecting input to first hidden layer
                input_weight = []
            
                for j in range(0,nodes_per_layer):
                    node_weight = random.random() * 2.0 - 1
                    input_weight.append(node_weight)
                    
                layer_weight.append(input_weight)
            
            network.append(layer_weight)
                
        layer_weight = []                                           #reset layer weight to add to network
        for i in range(0,nodes_per_layer):                          #connecting last layer to output
            input_weight = []
        
            for j in range(0,num_outputs):
                node_weight = random.random() * 2.0 - 1
                input_weight.append(node_weight)
                
            layer_weight.append(input_weight)
        
        network.append(layer_weight)                                #list of network weights (list of lists)
        
        self.network = network
        
    

    def make_child(self,mother):                                    #mother used only for mutation
        
        self.inputs = mother.inputs
        self.nodes_per_layer = mother.nodes_per_layer
        self.num_layers = mother.num_layers
        self.num_outputs = mother.num_outputs
                                                    
        total_weights = mother.inputs * mother.nodes_per_layer + mother.nodes_per_layer * mother.nodes_per_layer * (mother.num_layers - 1) + mother.nodes_per_layer * mother.num_outputs

        self.network = []                                           #holds child network (brain)
        mother_weights = total_weights
        pulled_weights = 0
        count = 0
        #randchance = .05                                           #random chance of mutation

                                                                    #mutate self
        for i in range(0,len(mother.network)):
            layer_weights = []
            for j in range(0,len(mother.network[i])):
                node_weights = []
                for k in range(0,len(mother.network[i][j])):
                    pulled_weights += 1
                    node_weights.append(mother.network[i][j][k] + (random.random()*2-1)/10)    
                layer_weights.append(node_weights)
            self.network.append(layer_weights)
            
            #self.network contains child brain (with half mom/dad)
        
        

    def load(self,filename):
        f = open(filename,"r")
        self.network = eval(f.read())
        f.close()
        
    def save(self,filename):
        f = open(filename, "w")
        f.write(repr(self.network))
        f.close()


    def choice(self,input_list,nodes_per_layer,num_layers,num_outputs):
        
        values = [0 for i in range(0,nodes_per_layer)]                  #sets list values to zero for every node
        
        for i in range(0,nodes_per_layer):
            
            for j in range(0,num_inputs):
                
                if input_list[j]:
                    values[i] += self.network[0][j][i]
                else:
                    values[i] -= self.network[0][j][i]             
        for a in range(1,num_layers):                                   #weighting nodes to nodes
            next_values = [0 for t in range (0,nodes_per_layer)]
            for i in range(0,nodes_per_layer):
                node_weight = (1/(1+math.e** (-values[i])))             #sigmoid funct
                for j in range(0,nodes_per_layer):
                    
                    next_values[j] += node_weight * self.network[a][i][j]     #update weight and next_value
                    
                        
            values = next_values
        output_values = [0 for t in range (0,num_outputs)]              #weighting last layer to output
        for i in range(0,nodes_per_layer):
            node_weight = (1/(1+math.e** (-values[i])))                 #sigmoid funct
            for j in range(0,num_outputs):
                   
                                                                        #sigmoid := 1 / (1+e^-t) | t = values[j]
                    
                output_values[j] += node_weight * self.network[num_layers][i][j]
                  
        biggest = 0
        for i in range(0,num_outputs):
            if output_values[i] > output_values[biggest]:
                biggest = i
        
        return biggest                                                  #returns index of biggest output (to be performed)


def search(searchx,searchy):
    '''
    location to look for food (if no previous food found or previous locations not desirable)
    '''
    searchx = random.randint(0,maxx)
    searchy = random.randint(0,maxy)                                   
    return searchx,searchy

def walk(h):
    '''
    walking function: returns direction moving (including not moving)
    '''
    newx = h.x
    newy = h.y
    if h.x < h.searchx:
        newx += 1
        if h.y < h.searchy:         # heading SE
            newy += 1
            h.heading = 3
        elif h.y > h.searchy:       #heading NE
            newy -= 1
            h.heading = 1
        else:
            h.heading = 2           #heading E
    elif h.x > h.searchx:           #heading W
        newx -= 1 
        if h.y < h.searchy:         #heading SW
            newy += 1
            h.heading = 5
        elif h.y > h.searchy:       #heading NW
            newy -= 1
            h.heading = 7
        else:
            h.heading = 6           #heading W
        
    else:
        if h.y > h.searchy:
            newy -= 1
            h.heading = 0
        elif h.y < h.searchy:
            newy += 1
            h.heading = 4
        else:
            pass                    #standing on searchx searchy

    return newx,newy
    

def hsight(h,food_list,oldfound,oldgoalx,oldgoaly):
    '''
    Human sight: considers locations of previously found food sources
    '''
    found,goalx,goaly = False,oldgoalx,oldgoaly
    for i in food_list:
        deltax = (i.x - h.x)
        deltay = (i.y - h.y)
        
        
        if deltax**2 + deltay**2 <= 50**2:                       #human within circle rad of food
            if h.heading == 0:
                if abs(deltax) <= abs(deltay):  
                    if h.y > i.y:                                #food is in sight & upper 45deg
                        found = True
                
                        
            if h.heading == 1:
                if deltax > 0:
                    if deltay < 0:                              #moving NE and found 
                        found = True
                        
            if h.heading == 2:
                if deltax > 0:
                    if abs(deltax) > abs(deltay):
                        found = True
                        
            if h.heading == 3:
                if deltax > 0:
                    if deltay > 0:
                        found = True
                        
            if h.heading == 4:
                if deltay > 0:
                    if abs(deltax) < abs(deltay):
                        found = True
                        
            if h.heading == 5:
                if deltay > 0:
                    if deltax < 0:
                        found = True
            
            if h.heading == 6:
                if deltax < 0:
                    if abs(deltax) > abs(deltay):
                        found = True
                        
            if h.heading == 7:
                if deltax < 0:
                    if deltay < 0:
                        found = True

            if found == True:
                goalx = i.x
                goaly = i.y
                return found,goalx,goaly 
    
               
    return False,oldgoalx,oldgoaly         

def zsight(h,food_list):
    '''
    zombie sight: does not consider previous locations of humans found
    '''
    for i in food_list:
        deltax = (i.x - h.x)
        deltay = (i.y - h.y)
        
        if i.hiding == True:
            zsight_rad = 20
        else:
            zsight_rad = 50
        
        if deltax**2 + deltay**2 <= zsight_rad**2:              #human within circle rad of food
            if h.heading == 0:
                if abs(deltax) <= abs(deltay):  
                    if h.y > i.y:                               #food is in sight & upper 45deg
                        h.found = True
                        
            if h.heading == 1:
                if deltax > 0:
                    if deltay < 0:                              #moving NE and found 
                        h.found = True
                        
            if h.heading == 2:
                if deltax > 0:
                    if abs(deltax) > abs(deltay):
                        h.found = True
                        
            if h.heading == 3:
                if deltax > 0:
                    if deltay > 0:
                        h.found = True
                        
            if h.heading == 4:
                if deltay > 0:
                    if abs(deltax) < abs(deltay):
                        h.found = True
                        
            if h.heading == 5:
                if deltay > 0:

                    if deltax < 0:
                        h.found = True
            
            if h.heading == 6:
                if deltax < 0:
                    if abs(deltax) > abs(deltay):
                        h.found = True
                        
            if h.heading == 7:
                if deltax < 0:
                    if deltay < 0:
                        h.found = True

            if h.found == True:
                h.goalx = i.x
                h.goaly = i.y
                break

def attack(h,zx,zy): 
    '''
    Returns true if attack was possible 
    '''
    
    for z in zombie_list:
        if z.x == zx and z.y == zy:
            if h.attack_delay <= 0:
                if random.random() < h.accuracy:
                    z.life -= h.damage      
                    h.attack_delay = 5
            return True
    
    for s in human_list:
        if s.x == zx and s.y == zy:
            if h.attack_delay <= 0:
                if random.random() < h.accuracy:
                    s.life -= h.damage      
                    h.attack_delay = 5
            return True
    return False
        
    

def simulate(Brain,drawing):
    '''
    Init all pygame and other varibales then enter main loop
    '''

    global maxx,maxy
    
    global zombie_list,safe_zone_list,human_list,human_corpse_list,food_list,zombie_corpse_list


    if drawing == True:
        pygame.init()

        
        window = pygame.display.set_mode((maxx,maxy+40))

        blue = pygame.Color(0,0,255)
        dark_blue = pygame.Color(0,0,127)
        green = pygame.Color(0,255,0)
        black = pygame.Color(0,0,0)
        white = pygame.Color(255,255,255)
        red = pygame.Color(255,0,0)
        dark_green = pygame.Color(0,127,0)
        yellow = pygame.Color(255,255,0)
        cyan = pygame.Color(0,255,255)
        aqua = pygame.Color(0,127,255)
        brown = pygame.Color(128,42,42)

        fnt = pygame.font.Font(pygame.font.match_font("arial"), 12)
        txt = [fnt.render("Moving to Food", False, white),
               fnt.render("Attack Zombie", False, white),
               fnt.render("Attack Human", False, white),
               fnt.render("Infected", False, white),
               fnt.render("Wandering", False, white),
               fnt.render("new target", False, white),
               fnt.render("Fleeing", False, white),
               fnt.render("Hiding", False, white)]
        clock = pygame.time.Clock()
    
   
    food_timer = 0
    food_list = []

     
    human_list = [human(Brain[i])for i in range(human_max)]
    human_corpse_list = []

    zombie_list = []
    for i in range(0,10):
        zombie_list.append(Zed())
    zombie_corpse_list = []

    safe_zone_list = []
    safe_zone_max = 10
    safe_zone_list = [safe_zone() for i in range(safe_zone_max)]

    corpse_turning = []
    corpse_timer = 0

    b = brains(num_inputs,nodes_per_layer,num_layers,num_outputs)            #create brain object to store network state
    #b.load("cap_network_state.txt")

    clock_time = 0                                                          #clock timer for trials
    #infection_counter = 0                                                  #number of humans infected during game
    #attack_counter = 0                                                     #number of zombies attacked - number of humans on human attack
    #end_food_level = 0
    #food_gathered = 0                                                      #number of food collected
    #bonus = 0                                                              #bonus for multi-intelligent behavior
    return_tuple = []                                                       #Returned tuple of (brain,score)


    while 1:
        '''
        MAIN LOOP
        '''
        if drawing == True:
            window.fill(black)                                              #fills between screens
            for event in pygame.event.get():                                #quits if pressed
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()      
              
        
        if len(zombie_list) <= 0 and len(human_list) > 0:                   #End simulation test (humans alive & zomb dead)        
            for h in human_list:
                if h.alive == True:
                    h.survived_timer += 1

                    if h.survived_timer >= 10000:
                        print "SURVIVED THE ZOMBIES!!!"
                        return_tuple.append((h.Brain,h.end_score()))
                        pygame.quit()

                        return return_tuple


        food_timer += 1
        if food_timer > 180 - maxx/10 :                                     #spawn food
            food_timer = 0
            food_list.append(food())

        if drawing == True:                                                 
            '''
            If drawing is on: draw buildings, zombies(active/deactive), humans(alive/dead), food
            '''
            pygame.draw.circle(window, blue, (10, 510),5,0)
            pygame.draw.circle(window, white, (10, 510),6,1)
            window.blit(txt[0], (20, 502))

            pygame.draw.circle(window, blue, (135, 510),5,0)
            pygame.draw.circle(window, green, (135, 510),6,1)
            window.blit(txt[1], (145, 502))

            pygame.draw.circle(window, blue, (260, 510),5,0)
            pygame.draw.circle(window, red, (260, 510),6,1)
            window.blit(txt[2], (270, 502))

            pygame.draw.circle(window, blue, (385, 510),5,0)
            pygame.draw.circle(window, yellow, (385, 510),2,0)              #human infected
            window.blit(txt[3], (395, 502))

            pygame.draw.circle(window, blue, (10, 530),5,0)
            window.blit(txt[4], (20, 522))

            pygame.draw.circle(window, aqua, (135, 530),5,0)
            window.blit(txt[5], (145, 522))

            pygame.draw.circle(window, cyan, (260, 530),5,0)
            window.blit(txt[6], (270, 522))

            pygame.draw.circle(window, dark_blue, (385, 530),5,0)
            window.blit(txt[7], (395, 522))

            for s in safe_zone_list:
                if s.alive == True:
                    pygame.draw.rect(window, brown, (s.x,s.y,50,50))        #safe zone drawing
            
        
            for h in human_list:
                if h.alive == True:   #human alive
                    if h.last_choice == 0: # Moving towards "food"
                        pygame.draw.circle(window, blue, (h.x,h.y),5,0)
                        pygame.draw.circle(window, white, (h.x,h.y),6,1)
                    elif h.last_choice == 1: # Attack Zombie
                        pygame.draw.circle(window, blue, (h.x,h.y),5,0)
                        pygame.draw.circle(window, green, (h.x,h.y),6,1)
                    elif h.last_choice == 2: # Attack Human
                        pygame.draw.circle(window, blue, (h.x,h.y),5,0)
                        pygame.draw.circle(window, red, (h.x,h.y),6,1)
                    elif h.last_choice == 3: # Suicide (Won't be seen)
                        pygame.draw.circle(window, blue, (h.x,h.y),5,0)
                    elif h.last_choice == 4: # Wandering
                        pygame.draw.circle(window, blue, (h.x,h.y),5,0)
                    elif h.last_choice == 5: # Finding new search x/y
                        pygame.draw.circle(window, aqua, (h.x,h.y),5,0)
                    elif h.last_choice == 6: # Fleeing
                        pygame.draw.circle(window, cyan, (h.x,h.y),5,0)
                    elif h.last_choice == 7: # Hiding
                        pygame.draw.circle(window, dark_blue, (h.x,h.y),5,0)
                        
                    if h.infected == True:
                        pygame.draw.circle(window, yellow, (h.x,h.y),3,0)               #human infected
                
            for h in human_corpse_list:
                if h.suicide == True:
                    pygame.draw.circle(window, (255,127,127), (h.x,h.y),5,0)            #human suicide
                else:        
                    pygame.draw.circle(window, red, (h.x,h.y),5,0)                      #human dead
                

            for z in zombie_list:
                if z.active == True:
                    pygame.draw.circle(window, green, (z.x,z.y),5,0)                    #zombie active
                else:
                    pygame.draw.circle(window, white, (z.x,z.y),5,0)                    #BAD ZOMBIE (needs debugged)
                
            for z in zombie_corpse_list:
                    pygame.draw.circle(window, dark_green, (z.x,z.y),5,0)               #zombie non-active

            for i in food_list:
                pygame.draw.circle(window, white, (i.x,i.y),5,0)                        #food

        for h in human_list:
        
            '''
            bool_list: This is everything about a human at any time
                0 = sees food
                1 = sees zed
                2 = sees human
                3 = is infected
                4-7 = life
                8-11 = food_lvl
                12 = can attack
                13-16 = paranoia 
                17 = in safe zone
                18 = goalxy in safe zone
                19 = saw Z recently
                20 = smell Zombie / very close
                21 = is hiding
            '''
            h.bool_list[0],h.goalx,h.goaly = hsight(h,food_list,h.bool_list[0],h.goalx,h.goaly)         #sees food
            h.bool_list[1],h.zgoalx,h.zgoaly = hsight(h,zombie_list,h.bool_list[1],h.zgoalx,h.zgoaly)   #sees zombie
            if h.bool_list[1] == True:                                                                  #currently sees zombie
                h.bool_list[19] = True                                                                  #has scene zombie recently
                h.saw_zombie = 30                                                                       #set human saw zombie counter
            if h.bool_list[19] == True:
                h.saw_zombie -= 1
            if h.saw_zombie <= 0:
                h.bool_list[19] = False
            h.bool_list[2],h.hgoalx,h.hgoaly = hsight(h,human_list,h.bool_list[2],h.hgoalx,h.hgoaly)
                                                                                                        #look for humans 


            #updating bool_list
            h.bool_list[3] = h.infected
            if h.life < 75:
                h.bool_list[4] = True
            if h.life < 50:
                h.bool_list[5] = True
            if h.life < 25:
                h.bool_list[6] = True
            if h.life < 10:
                h.bool_list[7] = True
                
            if h.food_level < 10:
                h.bool_list[8] = True
                h.bool_list[9] = True
                h.bool_list[10] = True
                h.bool_list[11] = True
            elif h.food_level < 25:
                h.bool_list[8] = True
                h.bool_list[9] = True
                h.bool_list[10] = True
                h.bool_list[11] = False
            elif h.food_level < 50:
                h.bool_list[8] = True
                h.bool_list[9] = True
                h.bool_list[10] = False
                h.bool_list[11] = False
            elif h.food_level < 75:
                h.bool_list[8] = True
                h.bool_list[9] = False
                h.bool_list[10] = False
                h.bool_list[11] = False
            else:
                h.bool_list[8] = False
                h.bool_list[9] = False
                h.bool_list[10] = False
                h.bool_list[11] = False
                
               
               
            if h.attack_delay > 0:
                h.bool_list[12] = False
            else:
                h.bool_list[12] = True   
               
            '''
            paranoia := attempt to simulate real paranoia by simulating fear/adrenaline 
            ** more testing is needed to determin if this var has any affect **
            '''   
            h.paranoia *= 0.99                                                              #lim of paranoia -> 0
            
                
            if h.paranoia < .10:                                                            #updating h.paranoia bool_list
                h.bool_list[13] = True
                h.bool_list[14] = True
                h.bool_list[15] = True
                h.bool_list[16] = True
            elif h.paranoia < .25:
                h.bool_list[13] = True
                h.bool_list[14] = True
                h.bool_list[15] = True
                h.bool_list[16] = False
            elif h.paranoia < .50:
                h.bool_list[13] = True
                h.bool_list[14] = True
                h.bool_list[15] = False
                h.bool_list[16] = False
            elif h.paranoia < .75:
                h.bool_list[13] = True
                h.bool_list[14] = False
                h.bool_list[15] = False
                h.bool_list[16] = False
            else:
                h.bool_list[13] = False
                h.bool_list[14] = False
                h.bool_list[15] = False
                h.bool_list[16] = False
                    
            h.bool_list[17] = False
            h.consomption_rate = .05
            for s in safe_zone_list:                                                            #human inside safe zone
                if s.alive == True:
                    if h.x >= s.x and h.y >= s.y and h.x <= s.x + 50 and h.y <= s.y + 50:
                        h.bool_list[17] = True
                        h.consomption_rate = h.consomption_rate / 2
                        if h.life < 95:
                            h.life += .05                                                       #give food and health
                        
            h.bool_list[18] = False
            for s in safe_zone_list:                                                            #goal inside safe zone
                if s.alive == True:
                    if h.goalx >= s.x and h.goaly >= s.y and h.goalx <= s.x + 50 and h.goaly <= s.y + 50:
                        h.bool_list[18] = True
                        
                        
            h.bool_list[20] = False                                                             #aware of Zed / very clsoe         
            for z in zombie_list: 
                deltax = h.x - z.x
                deltay = h.y - z.y           
                if deltax**2 + deltay**2 <= 20**2:                                              #Zed within 20 of human
                    h.bool_list[20] = True
                    h.zgoalx = z.x
                    h.zgoaly = z.y                                                              # Let human know where smelled zombie is
                    
            
            h.bool_list[21] = h.hiding                                                          #check if h is hiding
                
            

        for z in zombie_list:
            zsight(z,human_list)                                                                #look for human food
            zsight(z,human_corpse_list)                                                         #look for human corpse 
            
        if len(human_list) == 0:                                                                #END SIMULATION, EVERYONES DEAD
            pygame.quit()
            #return alive_timer / human_max                                                     #all humans dead, leave simulation , return alive_timer
            
            
            return return_tuple
                
       
              
        '''
        Loops through all humans updating condition and activity 
        '''
        for h in human_list:                                                                  
            if h.alive == True:
                
                choice = h.Brain.choice(h.bool_list,nodes_per_layer,num_layers,num_outputs)         
                h.alive_timer += 1                                                              #update alive timer for each human
                h.hiding = False
                if h.last_choice != choice:
                    h.total_choice += 1
                h.last_choice = choice
                if choice == 0:                                                                 #attack food
                
                    if h.bool_list[8] == False or h.bool_list[20] == True:  
                        h.life -= .05                                                           #dont look for food if full or Z close
                    if h.bool_list[11] == True:
                        h.life += .05                                                           #if looking for food when starving
                    
                
                    if h.x < h.goalx:
                        h.x += 1
                    elif h.x > h.goalx:
                        h.x -= 1
                    if h.y < h.goaly:
                        h.y += 1
                    elif h.y > h.goaly:
                        h.y -= 1
              
      
                    if h.x == h.goalx and h.y == h.goaly:                                       #found food remove food 
                        h.food_gathered += 1                                                    #total food collected in simulation
                        h.bool_list[0] = False
                        for f in food_list:
                            if h.x == f.x and h.y == f.y:
                                food_list.remove(f)
                                if h.food_level < 75:
                                    h.food_level += 25                                          #increase food level
                                else:
                                    h.food_level = 100
                        h.goalx = random.randint(0,maxx)
                        h.goaly = random.randint(0,maxy)
                                    
                
                elif choice == 1:                                                               #choice: updates human via choice of current actions 
                    if not attack(h,h.zgoalx,h.zgoaly) and h.bool_list[12] == True:             #attack zombie
                        h.attack_counter -= 0.1                                                 # Penalty for attacking nothing
                    else:
                        if h.bool_list[12] == True:
                            h.attack_counter += 20                                              #how many zombies has he shot 
                    
                elif choice == 2:
                    if not attack(h,h.hgoalx,h.hgoaly) and h.bool_list[12] == True:             #attack human
                        h.attack_counter -= 0.1                                                 # Penalty for attacking nothing
                    else:
                        if h.bool_list[12] == True:
                            h.attack_counter -= 10                                              #how many human on human attacked

                    for hh in human_list:                                                       #can hear gunfire
                        if (hh.x - h.x)**2 + (hh.y - h.y)**2 <= 100**2:
                            hh.paranoia *= 1.50

                elif choice == 3:                                                               #suicide option (human kills self)
                    h.damage = 100
                    attack(h,h.x,h.y)
                    h.suicide = True
                    
                    
                     
                elif choice == 4:                                                               #wandering (no goal state)
                    h.x,h.y = walk(h)
                    if h.x == h.searchx and h.y == h.searchy:
                        h.searchx,h.searchy = search(h.searchx,h.searchy)
                    if h.bool_list[20] == True:                                                 #aware of Zed
                        h.life -= .05
                
                elif choice == 5:                                                               #give up on target
                    h.searchx,h.searchy = search(h.searchx,h.searchy) 
                    
                elif choice == 6:                                                                #run away from zombie
                    if h.x < h.zgoalx and h.x - 1 >= 0:
                        h.x -= 1
                    elif h.x > h.zgoalx and h.x + 1 <= maxx:
                        h.x += 1
                    if h.y < h.zgoaly and h.y - 1 >= 0:
                        h.y -= 1
                    elif h.y > h.zgoaly and h.y + 1 <= maxy:
                        h.y += 1
                    
                    
                elif choice == 7:                                                               #h is hiding
                    h.hiding = True  
                    if h.bool_list[11] == True or h.bool_list[20] == True:
                                                                                                #penalty: starving / to close to Zed
                        h.life -= .5     
              
                if h.food_level > 0:
                    h.food_level -= h.consomption_rate                                          #decreasing food level always
                
                if h.attack_delay > 0:
                    h.attack_delay -= 1                                                         #decrease attack delay if not attacking
                
                
                
                
                
                if h.life <= 0:
                    
                    return_tuple.append((h.Brain,h.end_score()))                                #append dead human data
                    h.alive = False
                    human_corpse_list.append(h)
                    human_list.remove(h)        
                    continue
                if h.food_level <= 0:
                    h.life -= 1                                                                 #if starving then dying
                if h.infected == True:
                    h.life -= .1
                    if h.life <= 0:                                                             #human turned into zombie
                        z = Zed()   
                        z.x = h.x
                        z.y = h.y
                        return_tuple.append((h.Brain,h.end_score()))                            #append dead human data
                        zombie_list.append(z)
                        human_list.remove(h)
                        
                        
                
                
               

        '''
        Loops through all Zombies updating status and conditions based on current 
        actions
        '''
        for z in zombie_list:                                            
            if z.active == True: 
                
                if z.found == False:                                                        #in search of human food
                    newx,newy =  walk(z)
                    for s in safe_zone_list:                                                #check if zed can walk inside safezone
                        if s.alive == True:
                            if newx >= s.x and newy >= s.y and newx <= s.x + 50 and newy <= s.y + 50:
               
                                s.life -= 0.3
                                newx = z.x
                                newy = z.y
                                z.searchx,z.searchy = search(z.searchx,z.searchy)           #Z bumps into S.Z., walks away
                        if s.life <= 0:
                            s.alive = False
                    z.x = newx  
                    z.y = newy
                    if z.x == z.searchx and z.y == z.searchy:
                        z.searchx,z.searchy = search(z.searchx,z.searchy)
                
                else:                                                                       #has spotted human food
                    newx = z.x
                    newy = z.y
                    if z.x < z.goalx:
                        newx += 1
                    elif z.x > z.goalx:
                        newx -= 1
                    if z.y < z.goaly:
                        newy += 1
                    elif z.y > z.goaly:
                        newy -= 1
                    for s in safe_zone_list:                                                #check if zed can walk inside safezone
                        if s.alive == True:
                            if newx >= s.x and newy >= s.y and newx <= s.x + 50 and newy <= s.y + 50:
               
                                s.life -= 1
                                newx = z.x
                                newy = z.y
                        if s.life <= 0:
                            s.alive = False
                    z.x = newx  
                    z.y = newy
              
      
                    if z.x == z.goalx and z.y == z.goaly:                                   #found food remove food 
                        z.found = False
                        for c in human_corpse_list:
                            if abs(z.x - c.x) <= 1 and abs(z.y - c.y) <= 1 and c.suicide == False:
                                
                                newz = Zed()
                                newz.x = c.x
                                newz.y = c.y
                                zombie_list.append(newz)
                                human_corpse_list.remove(c)
                                
                        for f in human_list:
                            if abs(z.x - f.x) <= 1 and abs(z.y - f.y) <= 1:
                                
                                f.infected = True
                                f.life -= 15
                                f.paranoia *= 1.2
                                if f.life <= 0:
                                    return_tuple.append((f.Brain,f.end_score()))            #append dead human data
                                    newz = Zed()
                                    newz.x = f.x
                                    newz.y = f.y
                                    zombie_list.append(newz)
                                    human_list.remove(f)
                                for h in human_list:                                        #can hear human being infected
                                    if (h.x - z.x)**2 + (h.y - z.y)**2 <= 100**2:
                                        h.paranoia *= 1.05
                                if z.food_level < 75:
                                    z.food_level += 25                                      #increase food level
                                else:
                                    z.food_level = 100
                z.food_level -= 0.005                                                       #decreasing food level always
                if z.food_level <= 0:
                    z.life -= 0.5                                                           #if starving then dying
                if z.life <= 0:
                    z.active = False
                    zombie_corpse_list.append(z)                                            #add dead zombie to corpse list
                    zombie_list.remove(z)                                                   #remove dead zombie from active list
        
        
        if drawing == True:  
            pygame.display.update()                                                         #updates screen
            
            
            elapse = clock.tick(70)                                                         #slows to 30fps
            clock_time += 1                                                                 #update in game timer

###out of main loop ###

#fitness = 1500              #min fitness level to have kids

def run_simulate(gen_brains,fit_score):
    '''
    Check if existing brains (file) and use; otherwise create new random brains to begin simulation from
    scratch.  After each generation (allow n children per generation), pull best and use their brains
    to create next generation until maximum has been reached
    '''
    def cmp_tuple(x,y):                                                                     #compares tuples and sorts by score
        if x[1] < y[1]:                                                                     #passes into sorting funct
            return -1
        elif x[1] == y[1]:
            return 0
        else:
            return 1

    if gen_brains == None:

        B = []
        b_temp = []
        if os.path.exists('best_brain.txt') == True:                                        #load prev best , go from there
            prev_best_brain = brains(num_inputs,nodes_per_layer,num_layers,num_outputs)  
            prev_best_brain.load('best_brain.txt')
            #prev_best_score = simulate(prev_best_brain,False)
            #B.append((prev_best_brain,prev_best_score))
            for i in range(0,90):                                                           #add 10 clones of saved best brain to new simulation
                b_temp.append(prev_best_brain)                                              #add prev best brain to list b_temp
        for i in range(0,10):   
            b = brains(num_inputs,nodes_per_layer,num_layers,num_outputs)                   #create brain object to store network state
            b_temp.append(b)
        for i in range(0,100/human_max):    
                
            score = simulate(b_temp[i*human_max:(i+1)*human_max],True)  
           
           
            for s in score:
                if s[1] > fit_score:                                                        #brain must meet min stand to have kids
                    B.append(s)                                                             #append brain and score of that brain

        B.sort(cmp_tuple, reverse=True)                                                     #B is sorted with best brains at 0,1,2,...
        
        
        if len(B) >= 20:
            return B[:20]                                                                   #B now holds first n (best n) brains
        else:
            return B[:len(B)-1]

    else:
        print "len(gen_brains) = ",len(gen_brains)      
        C = []
        c_temp = []
        while len(gen_brains) < 25: 
            '''
            include 5 random brains within the 20 already returned
            make sure gen_brains has at least 25 in pool.  if len(gen_brains) < 25
            load n copies of prev_best_brain from file to use as clones
            '''
            child_brain = brains(num_inputs,nodes_per_layer,num_layers,num_outputs)
            #gen_brains.append((child_brain,0))                                             #create n random child brains to add to pool
            child_brain.load('best_brain.txt')
            gen_brains.append((child_brain,0))
            


        for i in range(0,100):  
            child_brain = brains(0,0,0,0)
            #child_brain.make_child(gen_brains[i][0])
            child_brain.make_child(gen_brains[random.randint(0,len(gen_brains)-1)][0])
            #pick random mom/dad from gen_brains list
            
            
            c_temp.append(child_brain)
        for i in range(0,100/human_max):    
                
            child_score = simulate(c_temp[i*human_max:(i+1)*human_max],False) 
            
            #child_score = simulate(child_brain,False)                                      #simulate child brain without visual
            for c in child_score:
                if c[1] > fit_score:
                    C.append(c)                                                             #append brain and score of that brain
        
        C.sort(cmp_tuple, reverse=True)
        if len(C) >= 20:
            return C[:20]                                                                   #get top 10 kids for next gen
        else:
            return C[:len(C)-1]                                                             #if <10 kids met fitness std
        


if __name__ == '__main__':
    '''
    Main: check if previous brain file exists and load; Begin simulation with random new brains
    starting at generation 1
    '''
    best_score = 0
    best_brain = None
    no_improve = 50
    if os.path.exists('best_brain.txt') == False:
        best_brain = brains(num_inputs,nodes_per_layer,num_layers,num_outputs)
        best_brain.save('best_brain.txt')
        file_exists = False
    else:
        file_exists = True
        best_brain = brains(num_inputs,nodes_per_layer,num_layers,num_outputs)
    b = None
    current_generation = 0
    fit_test = 50

    while 1:
        print universe_string, "Generation:", current_generation
        b = run_simulate(b,fit_test)              #b list of n best brains
        
        if len(b) > 0 and b != None and b[0][1] > best_score:
            best_score = b[0][1]
            best_brain = b[0]
            no_improve = 50
        else:
            no_improve -= 1
        print "NO_IMPROVE = ",no_improve,'\n'


        current_generation += 1
        if no_improve <= 0:
            simulate([best_brain[0] for i in range(human_max)],True)                        #draw new simulation that didn't improve
            bnew = brains(num_inputs,nodes_per_layer,num_layers,num_outputs)
            bnew.load('best_brain.txt')
            no_improve = 50
            current_generation = 0
            b = None
            print "..............."                                                         #no improve, start over
            bnew_list = simulate([bnew for i in range(human_max)],False)                    #run sim 10 copies of brain
            bnew_best_score = 0
            for bb in bnew_list:
                if bb[1] > bnew_best_score:
                    bnew_best_score = bb[1]
            if bnew_best_score < best_brain[1]:
                best_brain[0].save('best_brain.txt')
        if no_improve %10 == 0 and no_improve > 0:                                          #test current best brain with saved best brain
            bsaved = brains(num_inputs,nodes_per_layer,num_layers,num_outputs)
            bsaved.load('best_brain.txt')
            bsaved_list = simulate([bsaved for i in range(human_max)],False)                #run sim 10 copies of brain
            bsaved_best_score = 0
            for bb in bsaved_list:
                if bb[1] > bsaved_best_score:
                    bsaved_best_score = bb[1]
            if bsaved_best_score < best_brain[1]:
                best_brain[0].save('best_brain.txt')
        print best_score
        #fit_test = best_score - 500

    b = brains(num_inputs,nodes_per_layer,num_layers,num_outputs)                           #create brain object to store network state
    print simulate(b,False)
