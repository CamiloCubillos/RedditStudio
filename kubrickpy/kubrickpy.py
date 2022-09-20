#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32com.client
import os
import codecs
import sys
import getopt
from videoassembler import VideoAssembler


def main(argv):

    # Photoshop API initial settings

    print("[+] Opening PS file...")

    psApp = win32com.client.Dispatch("Photoshop.Application")
    psApp.Open(
        r"C:\Users\ccubi\Documents\RedditStudio\RedditStudio\kubrickpy\template_test.psd")
    doc = psApp.Application.ActiveDocument

    options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
    options.Format = 13   # PNG Format
    options.PNG8 = False  # Sets it to PNG-24 bit

    # Photoshop layers to be modified:

    autor_layer = doc.layerSets["story"].artLayers["autor"]
    story_layer = doc.layerSets["story"].artLayers["story"]
    footer_layer = doc.layerSets["footer"]

    # Current project data

    print("[+] Gathering data...")

    src_folder = ""
    opts, args = getopt.getopt(sys.argv[1:], "s:")
    for opt, arg in opts:
        if opt in ("-s"):
            src_folder = arg

    # Gathering data from 'stories.txt' of current project

    raw_stories = codecs.open(f"{src_folder}/stories.txt",
                              "r", "utf-8").read()
    stories = []

    for story in raw_stories.split("...")[0:-1]:
        data = story.split("\n")
        stories.append({"autor": data[0], "story": "".join(data[1:])})

    # Generate stories images

    print("[+] Generating images...")

    out_folder = f"{src_folder}\kubrickpy_images"
    os.system(f"mkdir {out_folder}")
    i = 1
    for story in stories:
        autor_layer.TextItem.contents = story["autor"]
        story_layer.TextItem.contents = story["story"]
        # Constant values of 105 and 50 for (1280x720) res
        MoveLayerTo(footer_layer, 105, story_layer.bounds[3] + 50)
        image = f"{os.getcwd()}\\{out_folder}\\{i}_{story['autor']}.png"
        doc.Export(ExportIn=image, ExportAs=2, Options=options)
        i += 1

    # Generate final video output

    print("[+] Generating video...")

    autors = [f"{int(idx)+1}_{story['autor']}" for idx,
              story in enumerate(stories)]
    vass = VideoAssembler(src_folder=src_folder, autors=autors)
    vass.assemble()


def MoveLayerTo(fLayer, fX, fY):

    dX = fX - fLayer.bounds[0]
    dY = fY - fLayer.bounds[1]

    fLayer.Translate(dX, dY)  # Contant x=180 position


if __name__ == "__main__":
    main(sys.argv[1:])
