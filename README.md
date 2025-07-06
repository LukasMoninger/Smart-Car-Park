# Smart-Car-Park

## Setup Instructions
GrovePi requires a Raspberry Pi with Raspberry Pi OS installed.
In my experience, only the 32-bit legacy version of Raspberry Pi OS works with GrovePi.
The installation script also requires a user with the name `pi` and sudo privileges.

```curl -kL dexterindustries.com/update_grovepi | bash```

The PDDL planner used in this project is `pyperplan`.
To install it, run:

```pip install pyperplan```

and set the PATH variable to include the directory where `pyperplan` is installed:

```echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc source ~/.bashrc```