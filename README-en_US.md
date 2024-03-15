# Pymodoro 🍅 (ver em [🇧🇷](./README.md))

A simple pomodoro app implemented using [pygame-ce](https://github.com/pygame-community/pygame-ce) and retrogame art concept. This is supposed to make you feel happy and to help you control your time while you work. 😊

Check this [section](#how-to-run-pymodoro-on-my-computer) to learn how to run this application.

The Pymodoro concept is simple, you can adjust two or four parameters and then you hit the play button. The parameters are "Work Time", "Break Time", "Cycles Before a Long Break" and "Long Break Time".

|    Parameter               |                                          Description                                    |   Default Value   |
|----------------------------|-----------------------------------------------------------------------------------------|-------------------|
| Work Time                  | The time you'll spent working in minutes.                                               | 25 minutes        |
| Break Time                 | The time you'll be using for resting before restarting the working cycle.               | 5 minutes         |
| Cycles Before a Long Break | Number of Work + Break cycles before taking a long break. If zero, then no long breaks. | 0 minutes (unset) |
| Long Break Time            | The time you'll be taking a long break before restarting the whole Work + Break thing. If zero, then no long breaks.  | 0 minutes (unset) |

## Using the Pymodoro

### The setup scene

Consider reading what the Pymodoro 🍅 has to say to you, it'll explain to you how to setup and use the application: 

<img src=screenshots/setup.png>

### The show scene

In this scene you have a timer with the cycle description. The info button will give you the statistics about the Pymodoro use. 
The green button (⬅️) will allow you to return to the Pymodoro setup scene. Remember that when you go back to setup, the progress you've made so far in the current pomodoro will be lost.

<img src=screenshots/show.png>

## How to run Pymodoro on my computer?

You can choose two ways to run Pymodoro. One way is by [downloading the release](#downloading-a-release), which is a quick and easy method; however, there may not be a suitable version for your operating system. The other way is by [downloading the repository](#downloading-the-repository), which may require a bit more experience with setting up the Python programming language environment.

### Downloading a release

In the [Github](https://github.com/Blendify-Games/Pymodoro) repository, go to the right corner and look for the link `Pomodoro v1.0.1`. Choose the release version you want, whether for Windows or Linux (both only for x86_64). Then, simply extract the file and click on it to run Pymodoro.

### Downloading the repository

This app was developed using python 3.12.1. After the python installation, it is recomended that you create an execution virtual environment for the libraries used by this project. Use virtualenv for this. Install virtualenv package using pip an then create a virtual environment inside the Pymodoro repository directory. With an access to a terminal just type:

```bash
> pip install virtualenv     # virtualenv installation
> virtualenv .venv           # virtual environment creation
#------ Alternatively
> pip3 install virtualenv    # use pip3 when python2 and python3 are both available in the system
> python3 -m venv .venv      # virtual environment creation
```

After the first execution if you want to run the game again just repeat steps 1 and 3.

1. Activate the virtual environment

    ```bash
    # On windows
    > .\.venv\Scripts\activate

    # On GNU/Linux or other unix-like systems
    $ source ./.venv/bin/activate
    ```
    
    * Notice that by activating the virtual environment something like `(.venv)` appears at the beginning of the command line on terminal. This indicates that the virtual environment is activated. To deactivate, type `deactivate`.

2. If this is your first time running Pymodoro in this virtual environment, then you should install the dependencies:

    ```bash
    > pip install -r requirements.txt
    #------ Alternatively
    > pip3 install -r requirements.txt      # use pip3 when python2 and python3 are both available in the system
    ```

3. Inside the `src` directory execute Pymodoro:

    ```bash
    > python main.py
    #------ Alternatively
    > python3 main.py                       # use python3 when python2 and python3 are both available in the system
    ```