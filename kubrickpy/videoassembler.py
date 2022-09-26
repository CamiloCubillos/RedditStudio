import os
import multiprocessing
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from moviepy.audio.fx.all import audio_loop
from moviepy.audio.fx.volumex import volumex
from math import ceil


class VideoAssembler:

    def __init__(self, **kwargs):
        self.wd = f"{os.getcwd()}/{kwargs['src_folder']}"
        self.autors = kwargs["autors"]

    def assemble(self):
        clips = []

        for autor in self.autors:
            # Add transition to video render pipeline
            audio_transition = AudioFileClip("kubrickpy/transition_sfx.mp3")
            image_transition = ImageClip(
                "kubrickpy/transition_image.jpg").set_duration(audio_transition.duration)
            transition_clip = concatenate_videoclips(
                [image_transition], method="compose")
            transition_clip.audio = CompositeAudioClip([audio_transition])
            clips.append(transition_clip)

            # Add story to video render pipeline
            audio_file = AudioFileClip(
                f"{self.wd}/{autor}.wav")
            image_clip = ImageClip(
                f"{self.wd}/kubrickpy_images/{autor}.png").set_duration(audio_file.duration)
            video_clip = concatenate_videoclips(
                [image_clip], method="compose")
            video_clip.audio = CompositeAudioClip([audio_file])
            clips.append(video_clip)

        # Concatenate all the clips
        output = concatenate_videoclips(clips, method='compose')

        # Add background music to the video
        bg_musicFile = AudioFileClip("kubrickpy/music/happy_track.mp3")
        bg_music = audio_loop(
            bg_musicFile, duration=output.duration).fx(volumex, 0.05)
        output.audio = CompositeAudioClip([output.audio, bg_music])

        # Render the video
        output.write_videofile(f'{self.wd}/OUTPUT.mp4',
                               fps=5,
                               codec='libx264',
                               audio_codec='aac',
                               temp_audiofile='temp-audio.m4a',
                               remove_temp=True,
                               threads=multiprocessing.cpu_count(),
                               preset="ultrafast"
                               )
