# CPSC 454 Project

Something about firewalls

- [Setup](#setup)
- [Run](#run)
- [Files](#files)
- [Outstanding Issues](#outstanding-issues)

# Setup

Requirements: 

- Mininet VM (aka "guest") running on VirtualBox
- Your local machine (aka "host") 

## Prepare the Host Machine 

Set up VirtualBox's shared folder if you haven't already.

Clone the repository in that shared folder: 

```
$ cd /path/to/your/shared/folder
$ git clone <URL to this repo> 
```

## Prepare the Guest VM

Note: don't forget to run `mount -t vboxsf <shared folder name> /path/to/folder` in the guest machine to actually mount the host's shared folder in the guest VM. For some godforsaken reason, this isn't done automagically.

### Symbolic Links 

POX doesn't like running modules by filenames. For example, if you wanted to run `~/pox/pox/forwarding/l2_learning.py` (built-in layer-2 learning switch), then you'd have to do the following:

```
$ ~/pox/pox.py forwarding.l2_learning
```

Note that you don't have to do this if the module in question does not touch POX at all.

To enable similar behavior with this project, create a symbolic link `~/pox/pox/project` and point it to the repository:

```
$ ln -s /path-to-shared-folder/repo-folder-name ~/pox/pox/project
```

The above symlink allows for POX invocations like this: 

```
$ ~/pox/pox.py project.ctrltest
```

# Run 

Start `LXTerminal` in the Mininet VM. 

First, start the controller: 

```
$ ~/pox/pox.py project.ctrltest
POX 0.7.0 (gar) / Copyright 2011-2020 James McCauley, et al.
WARNING:version:Support for Python 3 is experimental.
INFO:core:POX 0.7.0 (gar) is up.
```

Then, start the test topology: 

```
$ sudo python ~/pox/pox/project/topotest.py
mininet> 
```

# Files 

## topotest.py

A simple network topology involving one switch (`s1`), three virtual hosts (`h1`-`h3`), and one remote controller for the switch (`c0`). 

## ctrltest.py 

Starts a POX controller to control the switch. It registers two components with the main POX instance:

- `l2_learning`: a built-in layer-2 learning switch module that comes with POX. Basically makes the switch behave like a home router.
- `TestFW`: a custom firewall module. It's supposed to guide traffic like a BGP I think. 

On top of that, in the `launch()` callback, it *attempts* to start the UI:
- `core.tk`: this is SUPPOSED to be POX's entrypoint for Tkinter. I suspect that this is dysfunctional. 
- `core.tk.do(setup)`: run the UI-drawing logic as defined by the `setup()` function.

The UI doesn't work for now. See the [issues section](#outstanding-issues) for explanation.

## firewall.py 

Code borrowed heavily from online resources. 

Theoretically, the finished project should allow button clicks to change rules or create new ones in firewall modules like this. Or maybe even create and register new ones entirely. 

## ui.py

First attempt at spawning a user interface. I forgot to consider that an idle UI is, by definition, blocking. See next section for possible fixes.

# Outstanding Issues

## UI doesn't work 

Whenever the controller is started, this message shows up: 

```
$ ~/pox/pox.py project.ctrltest
POX 0.7.0 (gar) / Copyright 2011-2020 James McCauley, et al.
WARNING:version:Support for Python 3 is experimental.
WARNING:core:Still waiting on 1 component(s)
INFO:core:POX 0.7.0 (gar) is up.
```

That's definitely the UI component sitting idle doing nothing. Thus, there's no UI. 

The UI spawning code is ripped straight out of `~/pox/pox/misc/mac_blocker.py` and I was reasonably confident that it should work. So, I tried running `mac_blocker` to see if it does: 

```
$ ~/pox/pox.py forwarding.l2_learning misc.mac_blocker
POX 0.7.0 (gar) / Copyright 2011-2020 James McCauley, et al.
WARNING:version:Support for Python 3 is experimental.
WARNING:core:Still waiting on 1 component(s)
INFO:core:POX 0.7.0 (gar) is up.
```

So, it apparently doesnt work with `mac_blocker` either. This might be an issue with `~/pox/pox/tk.py` or maybe I'm doing something wrong in both cases. 

## Old attempt: UI is blocking 

The older version of this code used to register a UI module to POX, which is definitely something not intended. 

This *was* successful in spawning a UI, but it blocked the only thread this thing works off of. I guess registered modules are executed in sequence? 

## POX's documentation is godawful 

https://noxrepo.github.io/pox-doc/html/#tk

The official documentation has nothing on how to use the `core.tk` endpoint. 

As a last resort, we could consider abandoning POX in favor of some other controller. I chose POX because it's supposedly easy to use, so I don't know how much success we'd see from moving to another controller.
