# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (GML)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

import os
import sys
import logging
import shutil
from gzip import GzipFile

sys.path.insert(0, '..')
from base.subdayprecip import SubDayPrecipProcess
from grass.pygrass.modules import Module

class Process(SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
                                       identifier="subdayprecip-design-gml",
                                       description="Vrací vyčíslené návrhové srážky jako vektorová data ve formátu GML.")
          
          self.output = self.addComplexOutput(identifier = "output",
                                              title = "Výsledek ve formátu GML",
                                              formats = [ {"mimeType":"text/xml"} ],
                                              asReference = True)
          
     def export(self, dbf_only=False):
          self.output_file = '{}/{}.gml.gz'.format(self.output_dir, self.map_name)
          Module('v.out.ogr',
                 flags='sm',
                 input=self.map_name,
                 output='{}/{}.gml'.format(self.output_dir, self.map_name),
                 overwrite=True, format="GML")

          os.chdir(self.output_dir)
          with open('{}.gml'.format(self.map_name), 'rb') as gml, GzipFile(self.output_file, 'wb') as gmlgz:
               shutil.copyfileobj(gml, gmlgz)
          
          self.output.setValue(self.output_file)

if __name__ == "__main__":
     process = Process()
     process.execute()
