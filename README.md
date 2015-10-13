# MAD

### Overview
1. What's in a name
2. Basic usage
3. Resources

### What's in a name
Hello, it's nice to meet you.  I'm MAD.  My name represents a number of things.  All of them however, tie back into my main mission.  I exist, to assist Computer Network Defenders.  
I was created to fill an obvious void in defensive methodologies.  It should be obvious to anyone.  You can never win a swordfight by attempting nothing more than parrying your adversary's attacks.  Eventually, you will mess up.  Eventually you will miss something.  And eventually, you will go down.
Active Defense offers the answer to this conundrum.  Though we may not be "hacking back."  There are plenty of things we can do to stop an attacker in his tracks, that go well above and beyond simple "hardening."  
The reason why I was created, was to provide a contral hub, through which Computer Network Defenders could operate.  Seamlessly, simply, and powerfully, to deploy Active Defense tools on their networks.
I was created to democratize Active Defense.  To give everyone a shot at protecting their turf.

So, what's in my name?
MAD stands for MAD Active Defense.  Now, my creator though this was quite funny.  As the MAD in MAD Active Defense, also stands for MAD Active Defense.  Meaning that if you were to expand my name outwards, it would go on into infinity.  Like two mirrors on opposite ends of a room.  My expanded name would never reach an end.  And so, would result in an infinite string, reading "Active Defense Active Defense Active Defense Active Defense Active..."; you get the idea.  
But my name exists for more than just that reason.  My name exists because I AM MAD.  And you should be too.  I'm MAD at the current state of affairs in information security.  I'm mad at the prices we're expected to pay to buy useless 'next-generation' tools that aren't worth the silicon on which they reside.  I'm MAD at the way in which customer information is collected and abused, with barely any mention made to the idea of protecting it.  I'm MAD at the mystique of the "hacker" which has driven so many people into thinking there is something grand an noble about getting root on a box that doesn't belong to them.  I'm MAD that in the minds of our world, nothing is more important that fame, or foture.  I don't exist to assist in the creation of an empire.  I don't exist to bring glory to the virtual kiling fields.  I exist to make you safer.  I exist for a brighter world.

It's nice to meet you.  I'm MAD.

### Basic Usage
MAD can be launched by running the main console *mad.py*  It's really that simple.  Once you get into the console, you can type *help* to see a list of available commands.  My creator has attempted make me as smart as possible.  As such, I have built in shell features, such as command line history you can go through with your arrow keys.  I have smart autocomplete.  I come with aliased commands in case your human brain accidentally types in something synonymous to a command instead of the actual command.  
I function in a way very similar to many frameworks of the past.  Two frameworks which my creator had good knowledge of when he wrote me are as follows: The Metasploit Framework, and Recon-ng.
When first learning how to navigate your way through the console, don't be afraid to use the help command audaciously.  My creator has programmed the ability for the help command to bring up information about a number of things, such as specific commands, and modules.

#### The basic workflow
Here's how deploying a module usually works inside the MAD console.
1. Load the module
2. Set the variables
3. Run the module 

###### Loading a module
To load a module, simply type `load <module_name>`
For example
```
load local/honeyports/basic
```
A number of aliases exist for this command.  These will also work.
```
module local/honeyports/basic
```
or
```
use local/honeyports/basic
```
You will know the module is loaded, when your prompt changes to read the name for the module.  
From `MAD>>>` to this `local/honeyports/basic>>>`

###### Setting the variables
Setting the variables is also very simple.
To start with, you will want to list the available variables.
`list variables`

Each variable has four fields.  The name, the value, whether or not it is required, and a brief description.
If the description is too long, an error message will be displayed.  And you will have to run `more <variable_name>` to get the full printout.

To change a variable simply run `set <variable_name> <value>`
For example.
```
local/honeyports/basic>>> list variables
Variables
Name      Value             Required  Description
----------------------------------------------------------------------------
host                        no        Leave blank for 0.0.0.0 'all'
whitelist 127.0.0.1,8.8.8.8 no        hosts to whitelist (cannot be blocked)
port                        yes       port to listen on
----------------------------------------------------------------------------
local/honeyports/basic>>> set port 445
local/honeyports/basic>>> list variables
Variables
Name      Value             Required  Description
----------------------------------------------------------------------------
host                        no        Leave blank for 0.0.0.0 'all'
whitelist 127.0.0.1,8.8.8.8 no        hosts to whitelist (cannot be blocked)
port      445               yes       port to listen on
----------------------------------------------------------------------------
local/honeyports/basic>>>
```
###### Running your module
The interface between a module and the console for the purposes of execution is specified in the manual as so.  Each module will include in it a class of commands.  These commands are required to parse the variables sent from the console, into terms that are understandable for the module.  These commands then execute the module in the manner specified by the specific command.
Though many modules contain specialty commands, the most common command to see is the *run* command.
You can get a listing of the command for your currently loaded module by running `list commands`
If the module supports the defaultl *run* command, you will also notice the command *run -j* in the output to `list commands`.  This permutation of *run* tells the module to fork an individual process and run in the background.
This feature can be incredibly useful if you need to run more than one module at a time.
To execute your module, simply run the desired module specific command, as printed in the output of `list commands`.
Most of the time this will be a simple `run` or `run -j`

### Resources
For now, the resources are pretty simple.  You have this file.  You have the docs inside the docs folder.  You have the scripts inside the scripts folder (which are great if you need example commands).  The modules are all located in the modules folder (and subpaths).  
You can contact my creator on Twitter if you need his help with anything.
@zaeyx





