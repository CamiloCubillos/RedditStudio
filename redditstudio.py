from parser import Parser
from spoker import Spoker
from tkinter import *
import codecs


class App:

    def __init__(self, root):

        self.n_stories = 0
        self.stories_collection = []

        # --------------------------------------
        #               GUI SETUP
        # --------------------------------------

        root.title("RedditStudio")
        root.geometry("800x600")
        root.resizable(False, False)

        self.lframe = LabelFrame(root, borderwidth=0, width=50)
        self.lframe.grid(row=0, column=0)

        self.rframe = LabelFrame(root, borderwidth=0, width=50)
        self.rframe.grid(row=0, column=2)

        self.story_entry = Text(self.lframe, width=50,
                                height=35, borderwidth=2)
        self.story_entry.grid(row=0, column=0, pady=(10, 10), padx=(20, 0))

        self.stories_label = Label(
            self.rframe, width=50, height=10, text="Numero de historias: 0", font=("Arial", 10))
        self.stories_label.pack()

        self.add_story = Button(self.rframe, width=50, height=10,
                                text="Añadir Historia", borderwidth=5, command=self.add_story_COMMAND)
        self.add_story.pack()

        self.generate_media = Button(self.rframe, width=50, height=10,
                                     text="Generar Audios", borderwidth=5, command=self.generate_media_COMMAND)
        self.generate_media.pack()

    def add_story_COMMAND(self):
        self.n_stories += 1
        self.stories_label["text"] = f"Numero de historias: {self.n_stories}"
        parser = Parser(self.story_entry.get("1.0", END))
        self.story_entry.delete("1.0", END)
        parser.parse()
        self.stories_collection.append(
            {"id": self.n_stories, "autor": parser.autor, "story": parser.story})

    def generate_media_COMMAND(self):
        spoker = Spoker("")
        for story in self.stories_collection:
            # Generate audio files
            print(f"[!] Generating audio files for {story['autor']}...")
            spoker.src_text = story['story']
            spoker.filename = story['autor']
            spoker.save_mp3()
            # Generate a .txt with all the stories and autors
            print(f"[!] Generating text files for {story['autor']}...")
            with codecs.open("stories.txt", "a", "utf-8") as output:
                story_log = f"{story['autor']}\n{spoker.trans_text}\n--------------------------------------\n"
                output.write(story_log)

        print("[+] All stories generated.")


root = Tk()
app = App(root)
root.mainloop()
