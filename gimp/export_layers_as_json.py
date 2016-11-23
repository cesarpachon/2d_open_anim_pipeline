#!/usr/bin/env python
'''
nothing yet
'''

'''
Exports layers info as a JSON file

Run from the GIMP menu option: File -> Export info as JSON

'''

import json
import math
import os.path

import gimpfu
from gimp import pdb

def layers_as_json_export(img, active_layer, compression, dir_name):
    ''' Plugin entry point
    '''
    name0 = os.path.splitext(os.path.basename(img.filename))[0]
    output = {
            'img': {'name': name0, 'width': img.width, 'height': img.height},
        'layers': [],
    }
    layers = output['layers']

    for layer in img.layers:
        to_save = process_layer(img, layer, layers)

    # Write the JSON output
    name = os.path.splitext(os.path.basename(img.filename))[0]
    with open(os.path.join(dir_name, '%s.json' % name), 'w') as json_file:
        json.dump(output, json_file)

def process_layer(img, layer, layers):
    layer_name = layer.name
    x, y = layer.offsets
    y = img.height - y
    layers.append({
        'name': layer_name,
        'x': x,
        'y': y,
        'width': layer.width,
        'height': layer.height,
    })
    return

gimpfu.register(
    # name
    "json-info-export",
    # blurb
    "Json info export",
    # help
    "Exports layers info as a JSON file",
    # author
    "cesar",
    # copyright
    "God no! copyleft: GPLV3",
    # date
    "2016",
    # menupath
    "<Image>/File/Export/Export Info to JSON",
    # imagetypes
    "*",
    # params
    [
        (gimpfu.PF_ADJUSTMENT, "compression", "PNG Compression level:", 0, (0, 9, 1)),
        (gimpfu.PF_DIRNAME, "dir", "Directory", "/tmp")
    ],
    # results
    [],
    # function
    layers_as_json_export
)

gimpfu.main()
