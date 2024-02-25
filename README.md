# Pymodoro

A simple pomodoro app implemented using [pygame-ce](https://github.com/pygame-community/pygame-ce) and retrogame art concept. This is supposed to make you feel happy and to help you control your time while you work.

The pymodoro concept is simple, you can adjust two or four parameters and then you hit the play button. The parameters are "Work Time", "Break Time", "Long Break After Work Cycles" and "Long Break Time".

|    Parameter              |                                          Description                                    |   Default Value   |
|---------------------------|-----------------------------------------------------------------------------------------|-------------------|
| Work Time                 | The time you'll spent working in minutes.                                               | 25 minutes        |
| Break Time                | The time you'll be using for resting before restarting the working cycle.               | 5 minutes         |
| Cycles Befor a Long Break | Number of Work + Break cycles before taking a long break. If zero, then no long breaks. | 0 minutes (unset) |
| Long Break Time           | The time you'll be taking a long break before restarting the whole Work + Break thing.  | 0 minutes (unset) |
