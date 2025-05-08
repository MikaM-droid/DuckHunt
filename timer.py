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
        self.countdown_time = 0 # Time to countdown from

#--------------------------------------------------------------------------------------------------------------------------
#Start the timer

    def start(self, countdown_seconds=60):
        if not self.is_running:
            self.countdown_time = countdown_seconds
            self.start_time = time.time()                #Set the start time to the current time
            self.is_running = True                       #Set to running
            self.is_paused = False                       #Set to not paused
            self.total_paused_time = 0                   #Reset the total paused time

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
        self.countdown_time = 0

#--------------------------------------------------------------------------------------------------------------------------
#Get the remaining time in seconds

    def get_time_remaining(self):
        if not self.is_running:
            return self.countdown_time
        if self.is_paused:
            elapsed = self.paused_time - self.start_time - self.total_paused_time
        else:
            elapsed = time.time() - self.start_time - self.total_paused_time
        remaining = self.countdown_time - elapsed
        return max(0, remaining)  # Never return negative time
    
#--------------------------------------------------------------------------------------------------------------------------
#Get formatted time

    def get_formatted_time(self):
        remaining = self.get_time_remaining()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return f"{minutes:02d}:{seconds:02d}"







            