# -*- coding: utf-8 -*-
"""Subclass of AboutFrame, which is generated by wxFormBuilder."""

import wx
import gui
import json
import glob
import os
import module as m

# Implementing AboutFrame
class MasiveCalcsFrame( gui.MasiveCalcsFrame ):
    def __init__( self, parent ):
        '''
            Al inicio carga por defecto dos archivos:
                :points.json: archivo de los puntos de observación
                :files.json: archivos y directorios para procesar
        '''
        gui.MasiveCalcsFrame.__init__( self, parent )

        POINTS_FN = 'points.json'
        FILES_FN = 'files.json'

        points_filename = POINTS_FN
        with open(points_filename) as json_data:
            self.dat = json.load(json_data)
        for po in self.dat.keys():
            point = str(po)+':'+str(self.dat[po][0])+','+str(self.dat[po][1])
            self.mc_LBox_points.InsertItems([point],1)

        files_filename = FILES_FN
        with open(files_filename) as json_files_data:
            self.dir_files = json.load(json_files_data)['files']
        for f in self.dir_files:
            self.mc_LBox_Files2Process.InsertItems([f],1)

    def onTreeItemRClick( self, event ):
        '''
        Right click over a tree item add files or
        directorys to the listbox to be processed
        '''
        if self.mc_gDir.GetPath() not in self.mc_LBox_Files2Process.GetStrings():
            self.mc_LBox_Files2Process.InsertItems([self.mc_gDir.GetPath()],1)
            self.dir_files.append(self.mc_gDir.GetPath())

    def onStartExtractionClick( self, event ):
        #print self.dat
        files = []
        for i in self.dir_files:
            imgs = os.path.join(i,"*.*")
            fileLst = glob.glob(imgs)
            for fn in fileLst:
                files.append(fn)
            #for point in self.points:
                #print point
        band = int(self.mc_txt_band.GetValue())
        m.GetMasiveValues(files,self.dat, band)

    def onBtnAddPointClick( self, event ):
        # get lat/row and lon/col
        lat_row = self.mc_txt_lat.GetValue()
        lon_col = self.mc_txt_lon.GetValue()
        point =  lat_row + "," + lon_col

        # concatenate the type of point: lat/lon or row/col
        choice = self.mc_rBox_points_type.GetStringSelection()

        '''
        if choice == "Row/Col":
            point += " (RC)"
        else:
            point += " (LL)"
        '''

        # insert into the points listbox
        self.mc_LBox_points.InsertItems([point],1)

    def onPointsTypeClick( self, event ):
        choice = self.mc_rBox_points_type.GetStringSelection()
        if choice == "Row/Col":
            self.mc_stxt_lat.SetLabel("Row")
            self.mc_stxt_lon.SetLabel("Column")
        else:
            self.mc_stxt_lat.SetLabel("Latitude")
            self.mc_stxt_lon.SetLabel("Longitude")

    def onOpenPointsFile( self, event ):
        points_filename = self.mc_btn_file_points.GetPath()
        with open(points_filename) as json_data:
            self.dat = json.load(json_data)
        for po in self.dat.keys():
            point = str(po)+':'+str(self.dat[po][0])+','+str(self.dat[po][1])
            self.mc_LBox_points.InsertItems([point],1)
        #self.m_txt_log.AppendText("#### Opened File #### \n"+self.filename)
        #self.m_statusBar.SetStatusText(self.filename)