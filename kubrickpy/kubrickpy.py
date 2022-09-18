#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32com.client
import os

psApp = win32com.client.Dispatch("Photoshop.Application")

psApp.Open(
    r"C:\Users\ccubi\Documents\RedditStudio\RedditStudio\kubrickpy\template_test.psd")
doc = psApp.Application.ActiveDocument

# Change story data

autor = doc.layerSets["story"].artLayers["autor"]
autor.TextItem.contents = "Domassimo"
#autor.TextItem.contents = "---"

story = doc.layerSets["story"].artLayers["story"]
story.TextItem.contents = """Para algunos, también puede ser útil apagar los camiones y Kerbals que caminan en el VAB y el hangar. Descubrí que mi máquina comenzó a tartamudear después de un tiempo, desactivar esa opción en algún lugar de la configuración ayudó a aliviar ese problema. Y, por supuesto, si el rendimiento no es demasiado bueno, esfuércese por mantener un recuento bajo de piezas en cada embarcación (en estaciones particulares) , ya que eso realmente ayuda a mantener bajos los cálculos."""
#story.TextItem.contents = "---"

# Move footer


def MoveLayerTo(fLayer, fX, fY):

    dX = fX - fLayer.bounds[0]
    dY = fY - fLayer.bounds[1]

    print(dX)
    print(dY)

    fLayer.Translate(dX, dY)  # Contant x=180 position


footer = doc.layerSets["footer"]
print(footer.bounds[0])
MoveLayerTo(footer, 180, story.bounds[3] + 100)
