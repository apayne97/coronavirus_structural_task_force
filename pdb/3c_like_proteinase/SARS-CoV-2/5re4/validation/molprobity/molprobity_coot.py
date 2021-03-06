# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', ' 154 ', 'TYR', 0.029942770995157686, (10.329999999999998, -11.486, -9.26))]
data['omega'] = []
data['rota'] = [('A', '  27 ', 'LEU', 0.17865690228461087, (5.600000000000001, -9.776999999999997, 19.075)), ('A', '  41 ', 'HIS', 0.2951662705698459, (13.655999999999999, -7.114, 23.189)), ('A', ' 123 ', 'SER', 0.16174602686312975, (-2.907999999999999, -6.387, 9.503)), ('A', ' 216 ', 'ASP', 0.13135564093309282, (0.8729999999999989, 16.082, -14.787)), ('A', ' 267 ', 'SER', 0.2274785663403188, (11.727999999999994, 22.41, -12.443))]
data['cbeta'] = []
data['probe'] = [(' A 294  PHE  CD2', ' A 610  HOH  O  ', -0.929, (15.691, 3.184, -8.564)), (' A 110  GLN  HG3', ' A 754  HOH  O  ', -0.893, (19.192, 0.915, -1.703)), (' A 294  PHE  HD2', ' A 610  HOH  O  ', -0.892, (15.653, 2.829, -7.81)), (' A  19  GLN HE21', ' A 119  ASN  HB3', -0.785, (0.143, -13.104, 19.055)), (' A 288  GLU  OE1', ' A 501  HOH  O  ', -0.707, (5.858, 10.412, -1.565)), (' A 229  ASP  OD1', ' A 502  HOH  O  ', -0.687, (23.891, 28.821, -9.466)), (' A  19  GLN  NE2', ' A 119  ASN  HB3', -0.665, (0.001, -13.739, 18.587)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.662, (1.743, -3.811, 15.155)), (' A  41  HIS  HE1', ' A 164  HIS  O  ', -0.577, (11.1, -2.788, 18.947)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.554, (8.593, -3.367, -11.802)), (' A 403  DMS  H23', ' A 612  HOH  O  ', -0.55, (3.394, -21.466, 7.312)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.521, (0.804, -23.226, 12.788)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.501, (14.401, -12.731, -0.501)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.496, (16.388, -11.321, 20.604)), (' A 279  ARG  NH2', ' A 526  HOH  O  ', -0.471, (-1.533, 28.351, -10.803)), (' A  69  GLN HE21', ' A  72  ASN  HA ', -0.461, (-1.977, -20.845, 16.729)), (' A 111  THR  HA ', ' A 129  ALA  HA ', -0.455, (11.859, 3.618, 1.38)), (' A 104  VAL  O  ', ' A 160  CYS  HA ', -0.437, (17.941, -5.439, 4.2)), (' A 227  LEU  HA ', ' A 227  LEU HD23', -0.43, (22.937, 19.158, -9.736)), (' A 286  LEU  C  ', ' A 286  LEU HD12', -0.427, (4.542, 16.319, -1.689)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.419, (14.751, 8.118, 0.328)), (' A  36  VAL HG21', ' A  68  VAL HG11', -0.416, (9.47, -19.522, 15.069)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.413, (0.248, -9.122, 6.467)), (' A 117  CYS  O  ', ' A 144  SER  HA ', -0.413, (3.034, -5.906, 14.842)), (' A 236  LYS  NZ ', ' A 556  HOH  O  ', -0.412, (15.13, 32.017, 0.435)), (' A 199  THR HG21', ' A 239  TYR  CZ ', -0.411, (12.08, 17.515, -1.455)), (' A 239  TYR  CZ ', ' A 272  LEU HD21', -0.404, (12.17, 19.98, -2.287)), (' A 238  ASN  HA ', ' A 238  ASN HD22', -0.4, (18.425, 20.293, 4.295))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
