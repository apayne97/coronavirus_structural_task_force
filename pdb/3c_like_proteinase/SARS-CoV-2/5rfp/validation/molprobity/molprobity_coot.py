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
data['rama'] = [('A', '  46 ', 'SER', 0.03557431688303639, (10.488000000000001, -3.296, 29.689)), ('A', ' 154 ', 'TYR', 0.013131415612380142, (9.786999999999999, -11.53, -9.89))]
data['omega'] = []
data['rota'] = [('A', '  72 ', 'ASN', 0.014321320509435244, (-2.0930000000000017, -22.556, 15.298)), ('A', ' 145 ', 'CYS', 0.061126741006297294, (8.456, -5.300000000000001, 16.454)), ('A', ' 189 ', 'GLN', 0.0, (14.918000000000006, 2.853, 25.585)), ('A', ' 235 ', 'MET', 0.1169478971844475, (21.384000000000007, 23.102, -0.081)), ('A', ' 277 ', 'ASN', 0.17107087608882884, (0.7150000000000006, 27.950999999999997, -5.699))]
data['cbeta'] = []
data['probe'] = [(' A 193  ALA  O  ', ' A 501  HOH  O  ', -1.087, (19.968, 10.003, 15.72)), (' A 196  THR  O  ', ' A 502  HOH  O  ', -1.065, (20.62, 14.001, 8.094)), (' A  49  MET  HA ', ' A  49  MET  HE2', -0.931, (15.027, -2.653, 26.883)), (' A 249  ILE  O  ', ' A 503  HOH  O  ', -0.775, (16.399, 6.112, -14.571)), (' A  44  CYS  CB ', ' A  49  MET  HE3', -0.728, (14.58, -6.156, 26.69)), (' A 288  GLU  OE1', ' A 504  HOH  O  ', -0.724, (5.658, 10.833, -2.013)), (' A 290  GLU  OE1', ' A 505  HOH  O  ', -0.694, (6.803, 7.241, 1.461)), (' A  47  GLU  N  ', ' A  47  GLU  OE1', -0.645, (10.623, -3.44, 31.832)), (' A  48  ASP  OD1', ' A 506  HOH  O  ', -0.636, (17.419, -5.977, 32.484)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.605, (14.329, -13.178, -1.174)), (' A  44  CYS  HB3', ' A  49  MET  HE3', -0.581, (14.646, -6.093, 27.68)), (' A  44  CYS  SG ', ' A  49  MET  HE1', -0.569, (15.849, -6.056, 25.779)), (' A  49  MET  CA ', ' A  49  MET  HE2', -0.55, (14.803, -2.987, 27.351)), (' A  44  CYS  SG ', ' A  49  MET  CE ', -0.526, (15.175, -6.099, 26.182)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.496, (16.834, -11.453, 20.049)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.488, (15.556, 8.181, -0.209)), (' A  49  MET  CE ', ' A  49  MET  HA ', -0.471, (14.878, -3.25, 26.712)), (' A  40  ARG  HD3', ' A  85  CYS  HA ', -0.463, (20.713, -8.07, 19.337)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.46, (19.098, -7.747, 13.35)), (' A 294  PHE  CD2', ' A 737  HOH  O  ', -0.449, (16.135, 3.039, -9.036)), (' A 403  DMS  H23', ' A 547  HOH  O  ', -0.446, (3.768, -21.383, 6.972)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.44, (7.785, -3.592, -12.436)), (' A  40  ARG  O  ', ' A  43  ILE HG12', -0.431, (16.51, -10.295, 23.562)), (' A  36  VAL HG21', ' A  68  VAL HG11', -0.43, (9.84, -19.797, 14.859)), (' A  55  GLU  HG2', ' A 697  HOH  O  ', -0.424, (26.012, -8.86, 25.206)), (' A  44  CYS  HB3', ' A  48  ASP  HB2', -0.422, (14.64, -6.354, 28.822)), (' A 235  MET  HE2', ' A 825  HOH  O  ', -0.421, (25.998, 25.69, -0.433)), (' A 104  VAL  O  ', ' A 160  CYS  HA ', -0.418, (18.104, -5.648, 3.57)), (' A 191  ALA  HB3', ' A 515  HOH  O  ', -0.413, (19.727, 9.456, 26.334)), (' A  45  THR  O  ', ' A  48  ASP  N  ', -0.412, (13.704, -4.436, 31.005)), (' A  44  CYS  CB ', ' A  49  MET  CE ', -0.408, (14.542, -5.684, 26.558)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.407, (0.644, -9.046, 6.439)), (' A  25  THR  HA ', ' A 664  HOH  O  ', -0.403, (5.743, -9.008, 25.167))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
