import os
from random import shuffle
import pygame
import threading
import time


class MusicPlayer:
    def __init__(self, music_files):
        self.music_files = music_files
        shuffle(self.music_files)
        self.music_ls_final_index = len(self.music_files) - 1
        self.current_index = 0
        self.is_playing = False
        self.thread = None
        pygame.mixer.init()

    def play_music(self):
        while self.is_playing:
            if not pygame.mixer.music.get_busy():
                self.play_next()
            time.sleep(0.1)

    def play_next(self):
        if self.current_index >= self.music_ls_final_index:
            shuffle(self.music_files)
            self.current_index = 0
        else:
            self.current_index += 1
        pygame.mixer.music.load(self.music_files[self.current_index])
        pygame.mixer.music.play()

    def start(self):
        if not self.is_playing:
            self.is_playing = True
            pygame.mixer.music.load(self.music_files[self.current_index])
            pygame.mixer.music.play()
            self.thread = threading.Thread(target=self.play_music)
            self.thread.start()

    def stop(self):
        if self.is_playing:
            self.is_playing = False
            pygame.mixer.music.stop()
            if self.thread:
                self.thread.join()

    def toggle(self):
        if self.is_playing:
            self.stop()
        else:
            self.start()

    def next_song(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.play_next()

    def previous_song(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            if 1 <= self.current_index <= self.music_ls_final_index:
                self.current_index -= 1
            else:
                self.current_index = self.music_ls_final_index
            pygame.mixer.music.load(self.music_files[self.current_index])
            pygame.mixer.music.play()


# 使用示例
if __name__ == "__main__":
    playlist = [f'bgm\{music}' for music in os.listdir('bgm') if music.endswith('.mp3')]
    player = MusicPlayer(playlist)
    player.start()
