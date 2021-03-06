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
data['rama'] = [('A', '  49 ', 'MET', 0.00044994836290566644, (13.724000000000002, -1.3839999999999995, 29.831))]
data['omega'] = []
data['rota'] = [('A', '   1 ', 'SER', 0.27223940133485497, (-1.9750000000000014, 5.525, -16.447)), ('A', '  27 ', 'LEU', 0.21921877937082918, (5.461000000000004, -9.666, 19.143)), ('A', '  47 ', 'GLU', 0.10725751251890871, (12.325999999999999, -2.443999999999999, 34.622)), ('A', '  50 ', 'LEU', 0.0239512469263802, (15.952999999999996, 1.721, 30.498000000000005)), ('A', '  72 ', 'ASN', 0.13830671843726003, (-2.7360000000000007, -22.324, 15.522)), ('A', ' 200 ', 'ILE', 0.2540717191335492, (15.565000000000005, 12.274999999999999, -1.017)), ('A', ' 216 ', 'ASP', 0.250943626024495, (0.7770000000000001, 16.112999999999996, -14.853))]
data['cbeta'] = []
data['probe'] = [(' A 294  PHE  CD2', ' A 739  HOH  O  ', -0.731, (16.483, 3.181, -8.481)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.658, (1.581, -3.836, 15.328)), (' A 217  ARG  NH2', ' A 507  HOH  O  ', -0.593, (3.679, 11.958, -21.492)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.583, (14.162, -12.949, -0.408)), (' A  40  ARG  HD3', ' A  85  CYS  HA ', -0.568, (19.65, -7.594, 19.64)), (' A 245  ASP  HB3', ' A 740  HOH  O  ', -0.534, (24.994, 6.527, -8.321)), (' A  50  LEU  O  ', ' A 188  ARG  NE ', -0.532, (18.847, 2.662, 28.439)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.488, (8.088, -3.58, -11.831)), (' A  19  GLN  NE2', ' A 119  ASN  HB3', -0.483, (-0.13, -13.292, 18.87)), (' A 141  LEU  HG ', ' A 684  HOH  O  ', -0.481, (-0.764, 0.649, 14.624)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.478, (18.448, -8.001, 14.436)), (' A  41  HIS  HE1', ' A 164  HIS  O  ', -0.475, (11.469, -2.991, 19.322)), (' A 117  CYS  O  ', ' A 144  SER  HA ', -0.464, (2.815, -6.109, 14.42)), (' A 110  GLN  HG3', ' A 708  HOH  O  ', -0.458, (19.506, 0.527, -1.125)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.455, (0.445, -8.94, 6.142)), (' A  50  LEU HD22', ' A 189  GLN  O  ', -0.45, (14.526, 4.059, 29.328)), (' A 286  LEU  C  ', ' A 286  LEU HD12', -0.448, (4.376, 16.452, -1.769)), (' A 137  LYS  NZ ', ' A 197  ASP  OD2', -0.445, (10.373, 12.207, 7.624)), (' A 243  THR  HA ', ' A 731  HOH  O  ', -0.44, (26.93, 15.049, -7.126)), (' A 155  ASP  O  ', ' A 501  HOH  O  ', -0.436, (10.203, -16.7, -4.472)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.434, (10.437, -21.38, 5.639)), (' A  22  CYS  SG ', ' A  61  LYS  HD2', -0.434, (12.43, -15.179, 27.324)), (' A  56  ASP  HA ', ' A  59  ILE HD12', -0.433, (23.712, -12.975, 31.752)), (' A  19  GLN HE21', ' A 119  ASN  HB3', -0.433, (-0.025, -13.057, 18.881)), (' A 262  LEU  HA ', ' A 262  LEU HD23', -0.427, (19.616, 18.825, -13.519)), (' A  28  ASN  O  ', ' A 146  GLY  HA3', -0.422, (8.723, -9.576, 15.09)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.419, (16.053, -10.999, 20.967)), (' A  40  ARG  CD ', ' A  85  CYS  HA ', -0.419, (19.405, -7.309, 20.361)), (' A 165  MET  SD ', ' A 187  ASP  HA ', -0.418, (15.376, -0.436, 20.883)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.413, (0.8, -22.784, 13.178)), (' A 259  ILE  HA ', ' A 600  HOH  O  ', -0.41, (14.277, 17.441, -21.309)), (' A 272  LEU  HA ', ' A 272  LEU HD23', -0.405, (10.371, 23.378, -3.041)), (' A 104  VAL  O  ', ' A 160  CYS  HA ', -0.405, (17.934, -5.595, 4.284)), (' A 165  MET  HB2', ' A 173  ALA  HB3', -0.404, (13.793, 2.676, 16.729)), (' A  68  VAL HG12', ' A  75  LEU HD12', -0.403, (7.313, -20.635, 15.531)), (' A  31  TRP  CD2', ' A  95  ASN  HB2', -0.403, (8.824, -21.374, 8.819))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
