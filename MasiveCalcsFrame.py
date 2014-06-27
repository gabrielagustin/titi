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

        # Set the current directory as the initial
        self.mc_gDir.SetPath(os.getcwd())

        # Global data structures to store points and files
        self.files2process = {'files':[]}
        self.point2extract = {}

        # Global names for the project files
        self.POINTS_FN = 'points.json'
        self.FILES_FN = 'files.json'

    def onTreeItemRClick( self, event ):
        '''
        Right click over a tree item add files or
        directorys to the listbox and to the global variable
        files2process['files'] to be processed
        '''
        if self.mc_gDir.GetPath() not in self.mc_LBox_Files2Process.GetStrings():
            self.mc_LBox_Files2Process.Append(self.mc_gDir.GetPath())
            self.files2process['files'].append(self.mc_gDir.GetPath())


    def onStartExtractionClick( self, event ):
        outfilename = self.mc_txt_filename_out.GetValue()
        self.mc_txt_log.AppendText("Saving results into file: "+outfilename+"\n")
        #print self.dat
        files = []
        for i in self.files2process:
            imgs = os.path.join(i,"*.*")
            fileLst = glob.glob(imgs)
            for fn in fileLst:
                files.append(fn)
        band = int(self.mc_txt_band.GetValue())

        m.SaveMasiveValues(outfilename,files,self.point2extract, band)
        self.mc_txt_log.AppendText("Fished")

    def onBtnAddPointClick( self, event ):
        '''
            Add a point (lat, lon) to a listbox and to
            the global dict self.point2extract
            Only works with Lat Lon pairs, row and col are
            not implemented yet
        '''
        n_points = len(self.point2extract)

        # get lat/row and lon/col
        lat_row = self.mc_txt_lat.GetValue()
        lon_col = self.mc_txt_lon.GetValue()
        po_label = self.mc_txt_po_label.GetValue()
        point =  po_label+ ':' +lat_row + ',' + lon_col

        # concatenate the type of point: lat/lon or row/col
        choice = self.mc_rBox_points_type.GetStringSelection()

        '''
        if choice == "Row/Col":
            point += " (RC)"
        else:
            point += " (LL)"
        '''

        # append a point into listbox and to the global dict
        if point not in self.mc_LBox_points.GetStrings():
            self.mc_LBox_points.Append(point)
            self.point2extract[po_label] = [float(lat_row),float(lon_col)]

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
        to the listbox and to the global dict self.point2extract
        '''
        points_filename = self.mc_btn_file_points.GetPath()
        with open(points_filename) as json_data:
            self.point2extract = json.load(json_data)
        for po in self.point2extract.keys():
            point = str(po)+':'+str(self.point2extract[po][0])+','+str(self.point2extract[po][1])
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
            if item_str in self.files2process['files']:
                self.files2process['files'].remove(item_str)


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
            if self.point2extract.has_key(key):
                self.point2extract.pop(key)

    def onSaveProjectClicked( self, event ):
        '''
        Create the user written dir to the proyect with two files
        files.json containing the files and directories to be processed
        points.json with the points to be extracted from the previous files
        '''

        # Create the dialog. In this case the current directory is forced as
        # the starting directory for the dialog.
        dlg = wx.FileDialog(
            self, message="Save proyect",
            defaultDir=os.getcwd(),
            defaultFile="my_proyect",
            style=wx.SAVE
            )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path_proj_name = dlg.GetPath()
            # Create the project dir if not exists
            if not os.path.exists(path_proj_name):
                os.makedirs(path_proj_name)
                # Save two json files with points and files
                with open(os.path.join(path_proj_name,  self.POINTS_FN), 'wb') as pfile:
                    json.dump(self.point2extract, pfile)
                with open(os.path.join(path_proj_name, self.FILES_FN), 'wb') as dfile:
                    json.dump(self.files2process, dfile)

        # Destroy the dialog
        dlg.Destroy()

    def onOpenProjectClicked( self, event ):
        '''
        Load from proyect dir the two files
        files.json containing the files and directories to be processed
        points.json with the points to be extracted from the previous files
        '''
        # dialog is set up to change the current working directory to the path chosen.
        dlg = wx.DirDialog(
            self, message="Choose a proyect file",
            defaultPath=os.getcwd(),
            style=wx.OPEN
            )

        if dlg.ShowModal() == wx.ID_OK:
            # Clean both ListBox
            self.mc_LBox_points.Clear()
            self.mc_LBox_Files2Process.Clear()

            path_proj_name = dlg.GetPath()
            # A. Reads points from POINTS_FN to global self.point2extract
            # and stores into listbox
            with open(os.path.join(path_proj_name, self.POINTS_FN), 'r') as pfile:
                self.point2extract = json.load(pfile)
            for po in self.point2extract.keys():
                point = str(po)+':'+str(self.point2extract[po][0])+','+str(self.point2extract[po][1])
                self.mc_LBox_points.Append(point)

            # B.  Reads dir from FILES_FN to global self.files2process
            # and stores into listbox
            with open(os.path.join(path_proj_name, self.FILES_FN), 'r') as dfile:
                self.files2process = json.load(dfile)
            for f in self.files2process['files']:
                self.mc_LBox_Files2Process.Append(f)

        dlg.Destroy()