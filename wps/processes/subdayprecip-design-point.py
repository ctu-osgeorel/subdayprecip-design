# -*- coding: utf-8 -*-

####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: WPS processes (Shapefile)
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

import os
import glob
from zipfile import ZipFile
import logging
import types
from subprocess import PIPE

from subdayprecip import SubDayPrecipProcess
from grass.pygrass.modules import Module

class Process(SubDayPrecipProcess):
     def __init__(self):
          SubDayPrecipProcess.__init__(self,
                                       identifier="subdayprecip-design-point",
                                       description="Service returns compulted value for observation point.",
                                       skip_input=True)

          self.obs_x=self.addLiteralInput(identifier = "obs_x",
                                          title = "Observation point (X)",
                                          type = types.FloatType)
          self.obs_y=self.addLiteralInput(identifier = "obs_y",
                                          title = "Observation point (Y)",
                                          type = types.FloatType)
          
          self.output = self.addLiteralOutput(identifier = "output",
                                              title = "Output value",
                                              type = types.FloatType) # TODO

     def execute(self):
          rasters = self.raster.getValue().split(',')
          Module('g.region', raster=rasters[0])

          map_name = 'obs'
          p = Module('m.proj', coordinates=[self.obs_x.getValue(), self.obs_y.getValue()],
                     proj_in='+init=epsg:4326', proj_out='+init=epsg:5514', stdout_=PIPE)
          x, y, z = p.outputs.stdout.split('|')
          vector_input="1|{}|{}".format(x, y)
          logging.info(vector_input)
          Module('v.in.ascii', input='-', output=map_name, cat=1, x=2, y=3, stdin_=vector_input)
          Module('v.db.addtable', map=map_name)
          logging.debug("Subday computation started")
          Module('r.subdayprecip.design',
                 map=map_name, raster=rasters, rainlength=self.rainlength.getValue())
          logging.debug("Subday computation finished")

          p = Module('v.db.select', map=map_name, flags='c', stdout_=PIPE)
          logging.info(p.outputs.stdout)
          self.output.setValue(p.outputs.stdout.split('|')[1].rstrip())
          
if __name__ == "__main__":
     process = Process()
     process.execute()