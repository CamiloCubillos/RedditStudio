import codecs
import os
import shutil
import translators as ts
from parser import Parser
from spoker import Spoker
from tkinter import *
from tkinter import messagebox


class App:

    def __init__(self, root):

        self.n_stories = 0
        self.stories_collection = []
        self.using_gtts = IntVar()

        # --------------------------------------
        #               GUI SETUP
        # --------------------------------------

        self.bg_color = "#242424"
        self.add_bg = PhotoImage(file="media/add_bg.png")
        self.remove_bg = PhotoImage(file="media/remove.png")

        root.title("RedditStudio")
        root.geometry("650x450")
        root.configure(bg=self.bg_color)
        root.resizable(False, False)

        # FRAMES

        self.lframe = LabelFrame(
            root, borderwidth=0, width=50, bg=self.bg_color)
        self.lframe.grid(row=0, column=0)

        self.rframe = LabelFrame(
            root, borderwidth=0, width=50, bg=self.bg_color)
        self.rframe.grid(row=0, column=2, padx=(30, 0))

        # INPUTS

        self.story_entry = Text(self.lframe, width=50,
                                height=25, borderwidth=2)
        self.story_entry.grid(row=0, column=0, pady=(10, 10), padx=(20, 0))

        self.name_label = Label(self.rframe, width=20,
                                text="Nombre del proyecto:", bg=self.bg_color, font=("Arial", 11), foreground="#ffffff")
        self.name_label.pack(pady=(50, 0))

        self.name_entry = Entry(self.rframe, width=20,
                                borderwidth=5, relief="flat")
        self.name_entry.pack(pady=20)

        self.stories_label = Label(
            self.rframe, width=20, text="Numero de historias: 0", bg=self.bg_color, font=("Arial", 11), foreground="#ffffff")
        self.stories_label.pack()

        self.add_story = Button(self.rframe, borderwidth=0,
                                image=self.add_bg, command=self.add_story_COMMAND)
        self.add_story.pack(pady=(10, 10))

        self.remove_story = Button(self.rframe, borderwidth=0,
                                   image=self.remove_bg, command=self.remove_story_COMMAND)
        self.remove_story.pack(pady=(10, 10))

        self.checkbox = Checkbutton(
            self.rframe, text="Use gTTS", bg=self.bg_color, foreground="#15E100", variable=self.using_gtts)
        self.checkbox.pack()

        self.generate_media = Button(self.rframe, width=20, height=1, bg="#43afde",
                                     text="Generar Archivos Media", command=self.generate_media_COMMAND)
        self.generate_media.pack(pady=(35, 0))

    def check_inputs(self):
        if (self.n_stories == 0):
            return "No ingresado ningun comentario de reddit."
        if (self.name_entry.get() == ""):
            return "No ha ingresado un nombre para el proyecto."
        return True

    def add_story_COMMAND(self):
        # story_entry has the end position at 2.0 when empty. Don't ask me why xd.
        if (self.story_entry.index("end") != "2.0"):
            self.n_stories += 1
            self.stories_label["text"] = f"Numero de historias: {self.n_stories}"
            parser = Parser(self.story_entry.get("1.0", END))
            self.story_entry.delete("1.0", END)
            parser.parse()
            self.stories_collection.append(
                {"id": self.n_stories, "autor": parser.autor, "story": parser.story})
        else:
            messagebox.showinfo(
                message="Copie y pegue en el recuadro de la izquierda un comentario de reddit.", title="Error")

    def remove_story_COMMAND(self):
        if (self.stories_collection):
            self.stories_collection.pop()
            self.n_stories -= 1
            self.stories_label["text"] = f"Numero de historias: {self.n_stories}"

    def generate_media_COMMAND(self):
        inputs_status = self.check_inputs()
        if inputs_status == True:
            # Create project folder
            proj_folder = self.name_entry.get()
            if os.path.isdir(proj_folder):
                # Clean previous session data if exists
                shutil.rmtree(proj_folder)
            os.mkdir(proj_folder)

            # Create project media
            i = 1
            for story in self.stories_collection:

                # Translate story
                translated_story = ts.bing(
                    story['story'], from_language="en", to_language="es")

                # Generate a .txt with all the stories and autors
                print(f"[!] Adding data of {story['autor']}...")
                with codecs.open(f'{proj_folder}/stories_data.txt', 'a', "utf-8") as output:
                    story_log = f"{story['autor']}\n{translated_story}\n|-|-|"
                    output.write(story_log)

                # Generate files for selected TTS

                if self.using_gtts.get():
                    # Generate .wav audios if 'gTTS' flag is on
                    print("[!] USING GTTS")
                    print(
                        f"[!] Generating audio files for {story['autor']}...")
                    spoker = Spoker(translated_story)
                    spoker.filename = f"{proj_folder}/{i}"
                    spoker.save_audio()
                else:
                    # Generate a .txt to be used by Balabolka TTS
                    print("[!] USING BALABOKLA")
                    print(
                        f"[!] Generating balabolka file for {story['autor']}...")
                    with codecs.open(f'{proj_folder}/{i}.txt', 'a', "utf-8") as balabolka_file:
                        balabolka_file.write(translated_story)
                i += 1

            # Clear session data
            self.stories_collection.clear()
            self.n_stories = 0
            self.stories_label["text"] = f"Numero de historias: {self.n_stories}"
            self.name_entry.delete(0, END)
            print("[+] All stories generated.")
        else:
            messagebox.showinfo(
                message=inputs_status, title="Error")


root = Tk()
app = App(root)
root.mainloop()
