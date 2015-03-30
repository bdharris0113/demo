AUTHOR:

Brian Harris

ABOUT:

This project was inspired by a published mathematical research paper (*1), in which all humans were 
alleged to be equally likely as to be infected via a zombie outbreak.  Disagreeing with all humans
are equally likely to succomb and that humans would be domed, I used a nueral net and supervised learning
to create a human agent who would hopefully be able to survive.  

WHAT YOU'LL SEE:

Brown squares: currently safe structures for human agents (though they can be destroyed)

Blue dots: Human agents (his color will change based on his current action, a list of which is located at the bottom of the screen)

Green dots: Zombies (lite green are active hunting , dark green are destroyed)

White dots: food (randomly spwaned , needed by humans to stay alive)

At the end of each simulation an output of the human agents simulation is printed to the terminal.  Simulations will continue until the program is exited.

METHOD:

I attemped to stay true to the evolution process (as i could); begining with a random neural net (NN), which acts as the human's brain with random weights.  I used the sigmoid function to calculate weights between nodes in the NN.  I allow n human agents per generation , score their individual outcomes (did they survive, kill zombies, starve, etc) then take the top two agents brains and merge them to create a new generation of human agents.  I continued this process until a consistant victory / survival was achieved.  I used a cluster of computers to seep up the simulations I allowed one week of continues simulations. 

NOTE: This AI was simulated completely alone (no fellow humans); I tested three general models (1,10 and 100 human agents per simulation).  Curiously, only the solo human simulation was able to reach a state of consistant survival.  Other models humans: killed one another as soon as they saw one another, refused to venture from safe structures and starved to death or clustered together leading to any human who was infected to turn several humans before being killed until all humans were zombies or dead.  Perhaps a longer trial period (longer than one week) would have lead to a consistant survival for groups.

OUTCOME:
  
With the solo human model, in under one week of trials, I was able to see a consistant survival of human agents.  While not always being able to survive, he regularly survived, and I feel, my goal was accomplished.  

Human agents behavior for survival seems to be to hide either at the edge of safe buildings (just inside where zombies cannot reach) rapidly osilating between fight and run, or hiding in the corners of the map until hunger forces him to venter into the center for food.  Tends to flee threats if approached from behind by can kill several zombies rapidly if within his field of view.  Special note is he may commit suicide if overrun (Suicide renders him unable to be turned into a zombie).






*1: "When Zombies Attack! Mathematical Modeling of an outbreak of zombie infection", (Munz,Hudea,Imad,Smith)
	http://mysite.science.uottawa.ca/rsmith43/zombies.pdf