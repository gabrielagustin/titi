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

        # Default filenames, temporary method, it will be from a
        # config file in the future

        POINTS_FN = 'points.json'
        FILES_FN = 'files.json'

        # A. Reads points from POINTS_FN to global self.dat and stores into
        # listbox
        points_filename = POINTS_FN
        with open(points_filename) as json_data:
            self.dat = json.load(json_data)
        for po in self.dat.keys():
            point = str(po)+':'+str(self.dat[po][0])+','+str(self.dat[po][1])
            self.mc_LBox_points.Append(point)

        # B.  Reads dir from FILES_FN to global self.dir_files and stores into
        # listbox
        files_filename = FILES_FN
        with open(files_filename) as json_files_data:
            self.dir_files = json.load(json_files_data)['files']
        for f in self.dir_files:
            self.mc_LBox_Files2Process.Append(f)

        # A and B have to be modularized with a function which receive the
        # listbox object and the json file to be loaded

    def onTreeItemRClick( self, event ):
        '''
        Right click over a tree item add files or
        directorys to the listbox to be processed
        '''
        if self.mc_gDir.GetPath() not in self.mc_LBox_Files2Process.GetStrings():
            self.mc_LBox_Files2Process.Append(self.mc_gDir.GetPath())
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
        outfilename = self.mc_txt_filename_out.GetValue()
        self.mc_txt_log.AppendText("Saving results into file: "+outfilename+"\n")
        m.SaveMasiveValues(outfilename,files,self.dat, band)
        self.mc_txt_log.AppendText("Fished")

    def onBtnAddPointClick( self, event ):
        '''
            Add a point (lat, lon) to a listbox and to
            the global dict self.dat
            Only works with Lat Lon pairs, row and col are
            not implemented yet
        '''
        n_points = len(self.dat)

        # get lat/row and lon/col
        lat_row = self.mc_txt_lat.GetValue()
        lon_col = self.mc_txt_lon.GetValue()
        point =  'PO'+str(n_points+1)+ ':' +lat_row + ',' + lon_col

        # concatenate the type of point: lat/lon or row/col
        choice = self.mc_rBox_points_type.GetStringSelection()

        '''
        if choice == "Row/Col":
            point += " (RC)"
        else:
            point += " (LL)"
        '''

        # append a point into listbox and to the global dict
        self.mc_LBox_points.Append(point)
        self.dat['PO'+str(n_points+1)] = [float(lat_row),float(lon_col)]

    def onPointsTypeClick( self, event ):
        '''
        Set and unset labels
        '''
        choice = self.mc_rBox_points_type.GetStringSelection()
        if choice == "Row/Col":
            self.mc_stxt_lat.SetLabel("Row")
            self.mc_stxt_lon.SetLabel("Column")
        else:
            self.mc_stxt_lat.SetLabel("Latitude")
            self.mc_stxt_lon.SetLabel("Longitude")

    def onOpenPointsFile( self, event ):
        '''
        Load points (lat, lon) from a json file
        to the listbox and to the gloab dict self.dat
        '''
        points_filename = self.mc_btn_file_points.GetPath()
        with open(points_filename) as json_data:
            self.dat = json.load(json_data)
        for po in self.dat.keys():
            point = str(po)+':'+str(self.dat[po][0])+','+str(self.dat[po][1])
            self.mc_LBox_points.Append(point)
        #self.m_txt_log.AppendText("#### Opened File #### \n"+self.filename)
        #self.m_statusBar.SetStatusText(self.filename)

    def onFiles2ProcessRightDown( self, event ):
        '''
        Delete files or dirs from listbox and the global list called
        self.dir_files when an item is right clicked
        '''
        item_num = self.mc_LBox_Files2Process.GetSelection()
        item_str = self.mc_LBox_Files2Process.GetString(item_num)
        if item_num>0:
            self.mc_LBox_Files2Process.Delete(item_num)
            if item_str in self.dir_files:
                self.dir_files.remove(item_str)


    def onPoints2ExtractRightDown( self, event ):
        '''
        Delete points from listbox and the global dict called self.dat
        when an item is right clicked
        '''
        item_num = self.mc_LBox_points.GetSelection()
        item_str = self.mc_LBox_points.GetString(item_num)
        if item_num>0:
            self.mc_LBox_points.Delete(item_num)
            key = item_str.split(':')[0]
            if self.dat.has_key(key):
                self.dat.pop(key)
