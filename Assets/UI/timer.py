def reset(self):
    """Reset the timer to its initial state"""
    self.start_time = pygame.time.get_ticks()
    self.time_left = self.initial_time
    self.is_running = True
    self.game_over_triggered = False 