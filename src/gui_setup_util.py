# -*- coding: utf-8 -*-
"""
Set of functions to assist in general GUI setup

Created on Sun Jul 05 14:46:34 2020

@author: Fruit Flies
"""
# =============================================================================
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if sys.version_info[0] < 3:
    from Tkinter import *
    import tkFileDialog
    from ttk import *
    import tkMessageBox
else:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox

from v_expresso_gui_params import (initDirectories, guiParams, trackingParams)

# allows drag and drop functionality. if you don't want this, or are having 
#  trouble with the TkDnD installation, set to false.
try:
    from TkinterDnD2 import *
except ImportError:
    print('Error: could not load TkDnD libraries. Drag/drop disabled')
# =============================================================================
"""Class for pop-up entry widget """
# https://stackoverflow.com/questions/33158292/how-do-you-make-a-custom-popup-in-tkinter-using-two-seperate-classes-and-inherit


# =============================================================================
class myEntryOptions(Toplevel):
    def __init__(self, master, app, entry_list=[], title_str='Options', init_vals=[], chkbtn_list=[]):
        Toplevel.__init__(self, master)
        self.master = master
        self.app = app  # this is a stand in for e.g. the "Expresso" class, which isn't itself a Tk object

        # sets the title of the Toplevel widget
        self.title(title_str)

        # configure column weights
        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        # ----------------------------------------------------------------
        # add entry widgets for list
        self.entry_list = entry_list
        self.entry_labels = {}
        self.entry_fields = {}
        self.entry_vars = {}

        # loop through entries and labels to fill entry pop-up window
        for rowCurr, ent in enumerate(entry_list):
            # configure weight of current grid row
            Grid.rowconfigure(self, rowCurr, weight=1)

            # initialize variable for this entry box and store in entryWindow struct
            var = StringVar()
            var.set(init_vals[rowCurr])
            self.entry_vars[ent] = var

            # generate label and entry widgets
            lbl = Label(self, text=ent)
            lbl.grid(column=0, row=rowCurr, sticky=NSEW)
            e = Entry(self, textvariable=self.entry_vars[ent])
            e.grid(column=1, row=rowCurr, sticky=NSEW)

            # add entry and label widgets to entryWindow struct
            self.entry_labels[ent] = lbl
            self.entry_fields[ent] = e

        # ---------------------------------------------------------------
        # get current row counter to keep track of new rows we might add
        row_counter = (len(entry_list)+1)

        # -------------------------------------------------------------
        # add any additional stuff (e.g. checkbuttons) if given as input
        self.chkbtn_list = chkbtn_list
        if len(chkbtn_list) > 0:
            # initialize dict fields for checkbuttons in frame
            # self.chkbtn_labels = {}
            self.chkbtn_fields = {}
            self.chkbtn_vars = {}

            # loop over checkbuttons
            for (ith, cb) in enumerate(chkbtn_list):
                # configure weight of checkbutton row
                Grid.rowconfigure(self, row_counter, weight=1)

                # initialize variable for this checkbutton and store in entryWindow struct
                var = BooleanVar()
                var.set(False)
                self.chkbtn_vars[cb] = var

                # generate label and entry widgets
                # lbl = Label(self, text=cb)
                # lbl.grid(column=0, row=row_counter, sticky=NSEW)
                c = Checkbutton(self, text=cb, variable=self.chkbtn_vars[cb])
                c.grid(column=1, row=row_counter, columnspan=2, sticky=NSEW)

                # add entry and label widgets to entryWindow struct
                # self.chkbtn_labels[c] = lbl
                self.chkbtn_fields[cb] = c

                # increment row counter
                row_counter += 1
        # ---------------------------------------------------------------
        # add "OK" and "Cancel" buttons
        button_row = row_counter   # row number for buttons
        # configure row weight
        Grid.rowconfigure(self, button_row, weight=1)
        # add OK button
        b_ok = Button(self, text='OK', command=self.ok_button_pressed)
        b_ok.grid(column=0, row=button_row, sticky=NSEW)

        # add Cancel button
        b_cancel = Button(self, text='Cancel', command=self.cancel_button_pressed)
        b_cancel.grid(column=1, row=button_row, sticky=NSEW)

    # callback for "OK" button
    def ok_button_pressed(self):
        # return entry values to master window in dict form
        self.app.popup_entry_values = {}
        for ent in self.entry_list:
            self.app.popup_entry_values[ent] = self.entry_fields[ent].get()

        # return checkbutton values to master window in dict form
        self.app.popup_chkbtn_values = {}
        for cb in self.chkbtn_list:
            self.app.popup_chkbtn_values[cb] = self.chkbtn_fields[cb].instate(['selected'])

        # exit pop-up
        self.exit_popup()

    # callback for "Cancel" button
    def cancel_button_pressed(self):
        # just exit
        print('Process canceled -- exiting')

        # exit pop-up
        self.exit_popup()

    # function to exit pop-up gui
    def exit_popup(self):
        self.destroy()
        # self.quit()

# =============================================================================
""" Function to build basic button + listbox panel """


# =============================================================================
def buildButtonListboxPanel(frame, root, btn_names, btn_labels, label_str,
                            row=0, col=0, padx=10, pady=2, lb_width=64,
                            lb_height=8):
    # first configure weights of frame in root grid setup to allow re-sizing
    Grid.rowconfigure(root, row, weight=1)
    Grid.columnconfigure(root, col, weight=1)
    Grid.columnconfigure(root, col + 1, weight=3)  # listbox (2nd column)

    # --------------------------------------------------------------------
    # build button frame
    # --------------------------------------------------------------------
    # initialize frame for buttons
    frame.button_frame = Frame(root)
    frame.button_frame.grid(column=col, row=row, sticky=NSEW)
    N_buttons = len(btn_names) + 1  # adding 1 for label row

    # set weight of button frame column and label row
    Grid.columnconfigure(frame.button_frame, 0, weight=1)
    Grid.rowconfigure(frame.button_frame, 0, weight=1)

    # label for button frame
    frame.button_label = Label(frame.button_frame, text=label_str,
                               font=guiParams['labelfontstr'])
    frame.button_label.grid(column=0, row=0, padx=padx, pady=pady, sticky=NSEW)

    # set weight of button frame column
    Grid.columnconfigure(frame.button_frame, 0, weight=1)

    # populate frame with buttons
    frame.buttons = {}
    for rowCurr, (bname, blabel) in enumerate(zip(btn_names, btn_labels), 1):
        # set weight of current row
        Grid.rowconfigure(frame.button_frame, rowCurr, weight=1)

        # generate button and place in grid
        b = Button(frame.button_frame, text=blabel)
        b.grid(column=col, row=rowCurr, padx=padx, pady=pady, sticky=NSEW)  # NSEW

        # store buttons in frame object
        frame.buttons[bname] = b

    # --------------------------------------------------------------------
    # build listbox frame
    # --------------------------------------------------------------------
    # initialize frame for listbox
    frame.listbox_frame = Frame(root)
    frame.listbox_frame.grid(column=col + 1, row=row, padx=padx, pady=pady,
                             sticky=NSEW)

    # set weights for listbox frame rows and columns
    Grid.columnconfigure(frame.listbox_frame, 0, weight=1)
    for rowCurr in range(N_buttons):
        Grid.rowconfigure(frame.listbox_frame, rowCurr, weight=1)

    # define listbox 
    frame.listbox = Listbox(frame.listbox_frame, width=lb_width,
                            height=lb_height, selectmode=EXTENDED)
    # exportselection=False)

    # define scrollbars and place them (pack)
    frame.hscroll = Scrollbar(frame.listbox_frame)
    frame.hscroll.pack(side=BOTTOM, fill=X)

    frame.vscroll = Scrollbar(frame.listbox_frame)
    frame.vscroll.pack(side=RIGHT, fill=Y)

    # link listbox and scrollbars -- also back listbox
    frame.listbox.config(xscrollcommand=frame.hscroll.set,
                         yscrollcommand=frame.vscroll.set)
    frame.listbox.pack(side=TOP, fill=BOTH, expand=True)

    frame.hscroll.configure(orient=HORIZONTAL, command=frame.listbox.xview)
    frame.vscroll.configure(orient=VERTICAL, command=frame.listbox.yview)

    # -------------------------------------
    # return modified frame
    return frame


# =============================================================================
""" Function to build basic button + listbox panel """


# =============================================================================
def buildBatchPanel(frame, btn_names, btn_labels, tboxFlag=False, row=0, col=0,
                    padx=4, pady=4, lb_width=90, lb_height=16):
    # -----------------------------------------------------------------------
    # first configure weights of frame  to allow re-sizing
    Grid.rowconfigure(frame, row, weight=1)
    Grid.rowconfigure(frame, row + 1, weight=1)
    Grid.rowconfigure(frame, row + 2, weight=1)
    Grid.columnconfigure(frame, col, weight=1)
    Grid.columnconfigure(frame, col + 1, weight=1)
    Grid.columnconfigure(frame, col + 2, weight=1)

    # --------------------------------------------------------------------
    # build listbox frame
    # --------------------------------------------------------------------
    # initialize frame for listbox
    px = 10
    py = 10  # 35
    cs = 2
    rs = 2
    frame.listbox_frame = Frame(frame)
    frame.listbox_frame.grid(column=col, row=row, columnspan=cs, rowspan=rs,
                             padx=px, pady=py, sticky=NSEW)

    # set weights for listbox frame rows and columns
    for colCurr in range(cs):
        Grid.columnconfigure(frame.listbox_frame, colCurr, weight=1)
    for rowCurr in range(rs):
        Grid.rowconfigure(frame.listbox_frame, rowCurr, weight=1)

    # define listbox 
    frame.listbox = Listbox(frame.listbox_frame, width=lb_width,
                            height=lb_height, selectmode=EXTENDED)

    # define scrollbars and place them (pack)
    frame.hscroll = Scrollbar(frame.listbox_frame)
    frame.hscroll.pack(side=BOTTOM, fill=X)

    frame.vscroll = Scrollbar(frame.listbox_frame)
    frame.vscroll.pack(side=RIGHT, fill=Y)

    # link listbox and scrollbars -- also back listbox
    frame.listbox.config(xscrollcommand=frame.hscroll.set, yscrollcommand=frame.vscroll.set)
    frame.listbox.pack(side=TOP, fill=BOTH, expand=True)

    frame.hscroll.configure(orient=HORIZONTAL, command=frame.listbox.xview)
    frame.vscroll.configure(orient=VERTICAL, command=frame.listbox.yview)

    # --------------------------------------------------------------------
    # build button frame
    # --------------------------------------------------------------------
    # initialize frame for buttons
    frame.button_frame = Frame(frame)
    frame.button_frame.grid(column=col, row=row + rs, sticky=NSEW)

    # add in entry boxes for time? (min, max, bin size)
    if tboxFlag:
        # types of entry box
        t_entries = ['t_min', 't_max', 't_bin']
        # set default entries
        t_defaults = ['0', '2000', '20']

        # generate entry boxes and labels
        entry_width = 6
        frame.t_entries = {}
        frame.t_entry_labels = {}
        for r, (entType, entDefault) in enumerate(zip(t_entries, t_defaults)):
            # set weight of current row
            Grid.rowconfigure(frame.button_frame, r, weight=1)

            # generate entry box and place in grid
            lbl = Label(frame.button_frame, text=entType + ':')
            lbl.grid(column=0, row=r, padx=padx, pady=pady, sticky=E)  # NSEW
            entry_box = Entry(frame.button_frame, width=entry_width)
            # textvariable=entDefault)
            entry_box.insert(END, entDefault)
            entry_box.grid(column=1, row=r, padx=px, pady=pady, sticky=W)

            # store entry boxes and labels in frame object
            frame.t_entries[entType] = entry_box
            frame.t_entry_labels[entType] = lbl
    else:
        # ensure that the time entry space doesn't get eaten up by other 
        # columns if we don't have it
        Grid.columnconfigure(frame.button_frame, 0, minsize=100)
        # populate frame with buttons
    frame.buttons = {}
    for colCurr in range(len(btn_names)):
        for rowCurr in range(len(btn_names[colCurr])):
            # set weight of current column/row
            Grid.columnconfigure(frame.button_frame, colCurr + 2, weight=2)
            Grid.rowconfigure(frame.button_frame, rowCurr, weight=2)

            # generate button and place in grid
            b = Button(frame.button_frame, text=btn_labels[colCurr][rowCurr])
            b.grid(column=colCurr + 2, row=rowCurr, padx=padx, pady=pady,
                   sticky=NSEW)  # NSEW

            # store buttons in frame object
            frame.buttons[btn_names[colCurr][rowCurr]] = b

    # return frame
    return frame


# =============================================================================
""" Function to perform TKDND bindings """


# =============================================================================

def bindToTkDnD(frame, listbox_name):
    # bind dragging and dropping to listbox
    frame.listbox.drop_target_register(DND_FILES, DND_TEXT)
    frame.listbox.dnd_bind('<<DropEnter>>', drop_enter)
    frame.listbox.dnd_bind('<<DropPosition>>', drop_position)
    frame.listbox.dnd_bind('<<DropLeave>>', drop_leave)
    frame.listbox.dnd_bind('<<Drop:DND_Files>>',
                           lambda event: any_drop(event, listbox_name))
    frame.listbox.dnd_bind('<<Drop:DND_Files>>',
                           lambda event: any_drop(event, listbox_name))
    frame.listbox.dnd_bind('<<Drop:DND_Text>>',
                           lambda event: any_drop(event, listbox_name))
    frame.listbox.drag_source_register(1, DND_TEXT, DND_FILES)
    frame.listbox.dnd_bind('<<DragInitCmd>>', drag_init_listbox)
    frame.listbox.dnd_bind('<<DragEndCmd>>', drag_end)

    return frame


# =============================================================================
""" General drag/drop functions (require TkDnD) """


# =============================================================================

# @staticmethod
def drop_enter(event):
    event.widget.focus_force()
    # print('Entering widget: %s' % event.widget)
    # print_event_info(event)
    return event.action


# @staticmethod
def drop_position(event):
    # print('Position: x %d, y %d' %(event.x_root, event.y_root))
    # print_event_info(event)
    return event.action


# @staticmethod
def drop_leave(event):
    # print('Leaving %s' % event.widget)
    # print_event_info(event)
    return event.action


# define drag callbacks

# @staticmethod
def drag_init_listbox(event):
    # print_event_info(event)
    # use a tuple as file list, this should hopefully be handled gracefully
    # by tkdnd and the drop targets like file managers or text editors

    data = ()
    #    if listbox.curselection():
    #        data = tuple([listbox.get(i) for i in listbox.curselection()])
    #        print('Dragging :', data)
    if event.widget.curselection():
        data = tuple([event.widget.get(i) for i in event.widget.curselection()])
        print('Dragging :', data)
    # tuples can also be used to specify possible alternatives for
    # action type and DnD type:
    return ((ASK, COPY), (DND_FILES, DND_TEXT), data)


# @staticmethod
def drag_init_text(event):
    # print_event_info(event)
    # use a string if there is only a single text string to be dragged
    data = ''
    sel = text.tag_nextrange(SEL, '1.0')
    if sel:
        data = text.get(*sel)
        print('Dragging :\n', data)
    # if there is only one possible alternative for action and DnD type
    # we can also use strings here
    return (COPY, DND_TEXT, data)


# @staticmethod
def drag_end(event):
    # print_event_info(event)
    # this callback is not really necessary if it doesn't do anything useful
    print('Drag ended for widget:', event.widget)


# specific functions for different listboxes
# @staticmethod
def file_drop(event):
    if event.data:
        # print('Dropped data:\n', event.data)
        # print(event.widget['text'])
        # print("widget name:", str(event.widget).split("."))

        files = event.widget.tk.splitlist(event.data)
        for f in files:
            if os.path.exists(f) and f.endswith(".hdf5"):
                # print('Dropped file: "%s"' % f)
                f_norm = os.path.normpath(f)

                event.widget.insert('end', f_norm)
            else:
                print('Not dropping file "%s": file does not exist or is invalid.' % f)

    return event.action


# @staticmethod
def vid_file_drop(event):
    if event.data:
        valid_ext = [".avi", ".mov", ".mp4", ".mpg", ".mpeg", \
                     ".rm", ".swf", ".vob", ".wmv"]

        files = event.widget.tk.splitlist(event.data)
        for f in files:
            exist_chk = os.path.exists(f)
            ext_chk = f.endswith(tuple(valid_ext))
            crop_chk = ('channel' in f) and ('XP' in f)
            if exist_chk and ext_chk and crop_chk:
                # print('Dropped file: "%s"' % f)
                f_norm = os.path.normpath(f)
                event.widget.insert('end', f_norm)
            else:
                print('Not dropping file "%s": file does not exist or is invalid.' % f)


# @staticmethod
def dir_drop(event):
    if event.data:
        # print('Dropped data:\n', event.data)
        # print_event_info(event)

        dirs = event.widget.tk.splitlist(event.data)
        for d in dirs:
            if os.path.isdir(d):
                # print('Dropped folder: "%s"' % d)
                d_norm = os.path.normpath(d)
                event.widget.insert('end', d_norm)
            else:
                print('Not dropping folder "%s": folder does not exist or is invalid.' % d)

    return event.action


# @staticmethod
def any_drop(event, lbox_name):
    if event.data:
        # valid file extensios for different data tyoes
        vid_valid_ext = [".avi", ".mov", ".mp4", ".mpg", ".mpeg",
                         ".rm", ".swf", ".vob", ".wmv"]
        ch_valid_ext = [".hdf5"]

        # get list of things currently trying to be dropped
        entries = event.widget.tk.splitlist(event.data)

        # also get list of current listbox content
        curr_entries = event.widget.get(0, END)
        # loop through entries to drop, check depending on listbox
        for ent in entries:
            # check if file exists
            exist_chk = os.path.exists(ent)

            # necessary conditions for valid entry (per lb type)
            valid_dir = all([(lbox_name == 'directories'),
                             os.path.isdir(ent)])
            valid_vid = all([(lbox_name == 'videos'),
                             ent.endswith(tuple(vid_valid_ext)),
                             ('channel' in ent), ('XP' in ent),
                             exist_chk])
            valid_channel = all([(lbox_name == 'channels'),
                                 ent.endswith(tuple(ch_valid_ext)),
                                 exist_chk])

            # add entry if it meets criteria for one of the listboxes
            if any([valid_dir, valid_vid, valid_channel]):
                ent_norm = os.path.normpath(ent)
                if (ent_norm not in curr_entries):
                    event.widget.insert('end', ent_norm)
            else:
                print('Error dropping object {}'.format(ent))

    return event.action

## =============================================================================
# """ General button callbacks that get used often """
## =============================================================================
#
## ---------------------------------------------------------------------------
## enable/disable remove button upon cursor selection in listbox
# def generic_on_select(frame, selection):
#    if frame.listbox.curselection():
#        frame.buttons['remove']['state'] = NORMAL
#    else:
#        frame.buttons['remove']['state'] = DISABLED
#
## ---------------------------------------------------------------------------
## populate a listbox with entries gathered by "func"
# def generic_add_item(frame, parent, func):
#    current_entries = frame.listbox.get(0, END)
#    new_entry = func(parent)
#    # prevent duplicate directories by checking existing items
#    if new_entry not in current_entries:
#        frame.listbox.insert(END, new_entry)
#
## ---------------------------------------------------------------------------   
## remove selected element(s) from listbox
# def generic_remove_item(frame):
#    # Reverse sort the selected indexes to ensure all items are removed
#    selected = sorted(frame.listbox.curselection(), reverse=True)
#    for item in selected:
#        frame.listbox.delete(item)
#
## ---------------------------------------------------------------------------
## clear all elements of listbox
# def generic_clear_all(frame):
#    frame.listbox.delete(0, END)
# def openEntryWindow(master, entry_list, title_str='Entry Window'):
#     # Toplevel object which will be treated as a new window
#     entryWindow = Toplevel(master)
#
#     # sets the title of the Toplevel widget
#     entryWindow.title(title_str)
#
#     # loop through entries and labels to fill entry pop-up window
#     entryWindow.entry_fields = {}
#     entryWindow.entry_vars = {}
#     entryWindow.entry_labels = {}
#     for rowCurr, ent in enumerate(entry_list):
#         # initialize variable for this entry box and store in entryWindow struct
#         var = StringVar()
#         entryWindow.entry_vars[ent] = var
#
#         # generate label and entry widgets
#         l = Label(entryWindow, textvariable=ent).grid(column=0, row=rowCurr)
#         e = Entry(entryWindow, textvariable=entryWindow.entry_vars[ent]).grid(column=1, row=rowCurr)
#
#         # add entry and label widgets to entryWindow struct
#         entryWindow.entry_labels[ent] = l
#         entryWindow.entry_fields[ent] = e