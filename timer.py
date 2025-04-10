import pygame
import time

#--------------------------------------------------------------------------------------------------------------------------
# Timer class to keep track of the time in the game

class GameTimer:
    def __init__(self):
        self.start_time = 0 
        self.paused_time = 0 
        self.is_paused = False 
        self.is_running = False 
        self.total_paused_time = 0 # Total time spent in paused state

#--------------------------------------------------------------------------------------------------------------------------
#Start the timer

    def start(self):
        if not self.is_running:
            self.start_time = time.time()    #Set the start time to the current time
            self.is_running = True           #Set to running
            self.is_paused = False           #Set to not paused
            self.total_paused_time = 0       #Reset the total paused time

#--------------------------------------------------------------------------------------------------------------------------
#Pause the timer

    def pause(self):
        if self.is_running and not self.is_paused:
            self.paused_time = time.time()  #Store the time when the pause started.
            self.is_paused = True

#--------------------------------------------------------------------------------------------------------------------------
#Resume the timer

    def resume(self):
        if self.is_running and self.is_paused: #Only resume if the timer is running and paused
            self.total_paused_time += time.time() - self.paused_time
            self.is_paused = False

#--------------------------------------------------------------------------------------------------------------------------
#Reset the timer

    def reset(self):
        self.start_time = 0
        self.paused_time = 0
        self.is_paused = False
        self.is_running = False
        self.total_paused_time = 0

#--------------------------------------------------------------------------------------------------------------------------
#Get the elapsed time in seconds

    def get_elapsed_time(self):
        if not self.is_running:
            return 0
        if self.is_paused:
            return self.paused_time - self.start_time - self.total_paused_time #Get the elapsed time while paused
        return time.time() - self.start_time - self.total_paused_time          #Get the elapsed time while running

#--------------------------------------------------------------------------------------------------------------------------
#Get the elapsed time in a formatted string (MM:SS)

    def get_formatted_time(self):
        elapsed = self.get_elapsed_time()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return f"{minutes:02d}:{seconds:02d}" 