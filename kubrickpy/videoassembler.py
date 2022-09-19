import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate


class VideoAssembler:

    def __init__(self, **kwargs):
        self.wd = f"{os.getcwd()}/{kwargs['src_folder']}"
        self.autors = kwargs["autors"]

    def assemble(self):
        clips = []
        for autor in self.autors:
            audio_file = AudioFileClip(f"{self.wd}/{autor}.mp3")
            image_clip = ImageClip(
                f"{self.wd}/kubrickpy_images/{autor}.png").set_duration(audio_file.duration + 0.5)
            video_clip = concatenate([image_clip], method="compose")
            video_clip.audio = CompositeAudioClip([audio_file])
            clips.append(video_clip)

        output = concatenate(clips, method='compose')
        output.write_videofile(f'{self.wd}/OUTPUT.mp4',
                               fps=30,
                               codec='libx264',
                               audio_codec='aac',
                               temp_audiofile='temp-audio.m4a',
                               remove_temp=True
                               )
