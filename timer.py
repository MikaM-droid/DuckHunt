import pygame
import time

################################################ Class Timer ##############################################################

class GameTimer:
    """
    Game timer class to keep track of the time in the game
    
    Attributes:
        start_time: Time when the timer started
        paused_time: Time when the timer was paused
        is_paused: Whether the timer is paused
    """
    def __init__(self):
        """
        Initializes the GameTimer.
        """
        self.start_time = 0 
        self.paused_time = 0 
        self.is_paused = False 
        self.is_running = False 
        self.total_paused_time = 0 # Total time spent in paused state
        self.countdown_time = 0 # Time to countdown from

#--------------------------------------------------------------------------------------------------------------------------

    def start(self, countdown_seconds=60):
        """
        Start the timer with a specified countdown time.
        
        Args:
            countdown_seconds: Time in seconds for the timer to run
        """
        if not self.is_running:
            self.countdown_time = countdown_seconds
            self.start_time = time.time()                #Set the start time to the current time
            self.is_running = True                       #Set to running
            self.is_paused = False                       #Set to not paused
            self.total_paused_time = 0                   #Reset the total paused time

#--------------------------------------------------------------------------------------------------------------------------

    def pause(self):
        """
        Pause the timer.
        
        If the timer is running and not already paused, store the current time as the pause time.
        """
        if self.is_running and not self.is_paused:
            self.paused_time = time.time()  #Store the time when the pause started.
            self.is_paused = True

#--------------------------------------------------------------------------------------------------------------------------

    def resume(self):
        """
        Resume the timer.
        
        If the timer is running and paused, add the time spent in paused state to the total paused time.
        """
        if self.is_running and self.is_paused: #Only resume if the timer is running and paused
            self.total_paused_time += time.time() - self.paused_time
            self.is_paused = False

#--------------------------------------------------------------------------------------------------------------------------

    def reset(self):
        """
        Reset the timer.
        
        Set all timer attributes to their initial values.
        """
        self.start_time = 0
        self.paused_time = 0
        self.is_paused = False
        self.is_running = False
        self.total_paused_time = 0
        self.countdown_time = 0

#--------------------------------------------------------------------------------------------------------------------------

    def get_time_remaining(self):
        """
        Get the remaining time in seconds.
        
        Returns:
            int: Remaining time in seconds
        """
        if not self.is_running:
            return self.countdown_time
        if self.is_paused:
            elapsed = self.paused_time - self.start_time - self.total_paused_time
        else:
            elapsed = time.time() - self.start_time - self.total_paused_time
        remaining = self.countdown_time - elapsed
        return max(0, remaining)  # Never return negative time
    
#--------------------------------------------------------------------------------------------------------------------------

    def get_formatted_time(self):
        """
        Get the remaining time formatted as MM:SS.
        
        Returns:
            str: Formatted time string
        """
        remaining = self.get_time_remaining()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return f"{minutes:02d}:{seconds:02d}"







            