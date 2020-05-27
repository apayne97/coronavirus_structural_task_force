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
data['rama'] = [('A', '  31 ', 'SER', 0.018841205960069052, (165.627, 207.976, 168.692)), ('A', '  32 ', 'PHE', 0.0017303096477011798, (167.453, 206.339, 165.825)), ('A', '  87 ', 'ASN', 0.0, (161.489, 201.70499999999996, 183.953)), ('A', ' 571 ', 'ASP', 0.0021489053084982972, (135.289, 167.366, 170.141)), ('C', ' 857 ', 'GLY', 0.018239697058434052, (152.238, 139.88, 166.478))]
data['omega'] = [('A', '  32 ', 'PHE', None, (166.985, 206.612, 167.187)), ('A', '  87 ', 'ASN', None, (162.18500000000003, 203.023, 184.117)), ('C', '  87 ', 'ASN', None, (193.006, 138.486, 187.82700000000003))]
data['rota'] = [('A', ' 193 ', 'VAL', 0.27145287506179416, (172.49600000000004, 202.17599999999993, 178.26900000000006)), ('A', ' 569 ', 'ILE', 0.19946279550893653, (132.208, 168.066, 165.17100000000002)), ('A', ' 856 ', 'ILE', 0.2764311286734629, (179.977, 167.066, 165.89000000000001)), ('B', ' 570 ', 'LEU', 0.0, (166.061, 136.633, 166.119)), ('B', ' 856 ', 'ILE', 0.023744381298150305, (143.124, 174.663, 166.336)), ('C', ' 856 ', 'ILE', 0.026859665542025204, (155.341, 138.407, 168.166))]
data['cbeta'] = []
data['probe'] = [(' C 856  ILE  CD1', ' C 858  LEU HD13', -1.293, (157.474, 140.312, 165.135)), (' A 589  PRO  CG ', ' B 855  TYR  CE2', -1.281, (138.101, 179.846, 166.802)), (' A 589  PRO  CG ', ' B 855  TYR  HE2', -1.24, (136.915, 180.702, 166.988)), (' A 589  PRO  CD ', ' B 855  TYR  HE2', -1.19, (136.17, 180.604, 166.984)), (' A 589  PRO  HG3', ' B 855  TYR  CD2', -1.149, (138.009, 178.873, 166.388)), (' C 856  ILE HD11', ' C 858  LEU HD13', -1.101, (157.614, 141.054, 165.673)), (' C 856  ILE  CG1', ' C 858  LEU HD13', -1.084, (156.308, 139.866, 166.31)), (' A 589  PRO  CD ', ' B 855  TYR  CE2', -1.06, (136.538, 179.822, 166.372)), (' C 856  ILE HD11', ' C 858  LEU  CD1', -1.02, (156.974, 141.126, 164.723)), (' C 856  ILE  CG1', ' C 858  LEU  CD1', -0.992, (156.251, 141.051, 165.727)), (' C 856  ILE HG12', ' C 858  LEU  CD1', -0.988, (155.411, 141.062, 166.744)), (' A 589  PRO  HG2', ' B 855  TYR  CE2', -0.975, (137.957, 180.059, 166.812)), (' A 589  PRO  HD2', ' B 855  TYR  CE2', -0.954, (135.323, 179.85, 166.567)), (' A 589  PRO  HD2', ' B 855  TYR  HE2', -0.937, (135.99, 180.563, 166.736)), (' A 589  PRO  HG3', ' B 855  TYR  HD2', -0.909, (138.21, 178.061, 166.937)), (' A 589  PRO  CG ', ' B 855  TYR  CD2', -0.906, (138.29, 179.523, 166.956)), (' C 856  ILE  CD1', ' C 858  LEU  CD1', -0.89, (156.475, 141.356, 165.822)), (' C 856  ILE HG12', ' C 858  LEU HD13', -0.849, (156.003, 140.495, 166.636)), (' A 589  PRO  HG2', ' B 855  TYR  HE2', -0.766, (137.355, 180.448, 166.977)), (' B 572  ILE HD11', ' C 963  VAL  CG1', -0.723, (161.377, 138.499, 167.742)), (' B 856  ILE  CG1', ' B 858  LEU HD13', -0.722, (143.193, 171.628, 164.536)), (' B 572  ILE HD11', ' C 963  VAL HG13', -0.712, (161.054, 138.953, 167.968)), (' C 856  ILE HD12', ' C 963  VAL HG22', -0.709, (159.018, 139.91, 166.5)), (' C 599  THR HG22', ' C 601  GLY  H  ', -0.696, (187.403, 140.651, 151.434)), (' B 106  PHE  HB2', ' B 117  LEU  HB3', -0.666, (117.074, 150.667, 195.49)), (' C 856  ILE HG12', ' C 858  LEU HD12', -0.662, (154.919, 141.076, 166.019)), (' B 856  ILE HD11', ' B 963  VAL HG22', -0.638, (142.493, 169.47, 164.269)), (' C 856  ILE  CD1', ' C 963  VAL HG22', -0.623, (158.726, 140.168, 165.773)), (' A  34  ARG  NH1', ' A 191  GLU  OE2', -0.62, (175.09, 206.95, 168.927)), (' A 131  CYS  SG ', ' A 166  CYS  N  ', -0.618, (176.337, 202.826, 200.948)), (' C 569  ILE HG23', ' C 570  LEU  CD2', -0.617, (177.646, 177.009, 160.799)), (' B  81  ASN  N  ', ' B 265  TYR  HH ', -0.602, (105.987, 141.976, 189.385)), (' C 980  ILE HG23', ' C 984  LEU HD12', -0.596, (158.917, 147.304, 186.279)), (' C  44  ARG  HB2', ' C 279  TYR  HD2', -0.595, (172.699, 129.072, 169.008)), (' A 720  ILE HG13', ' A 923  ILE HG23', -0.594, (168.925, 175.117, 112.483)), (' A 401  VAL HG22', ' A 509  ARG  HG2', -0.591, (141.221, 161.474, 214.006)), (' A 328  ARG HH21', ' A 580  GLN  HB2', -0.584, (124.273, 183.791, 185.561)), (' C 720  ILE HG13', ' C 923  ILE HG23', -0.583, (168.43, 137.82, 114.802)), (' A 960  ASN  OD1', ' C 570  LEU HD11', -0.576, (174.763, 175.202, 160.283)), (' C 569  ILE HG23', ' C 570  LEU HD22', -0.574, (177.481, 177.841, 160.935)), (' A 856  ILE  O  ', ' A 856  ILE HD12', -0.574, (177.725, 165.954, 164.358)), (' B 707  TYR  HB3', ' C 792  PRO  HG3', -0.573, (149.814, 128.478, 116.858)), (' A 570  LEU  O  ', ' A 571  ASP  CB ', -0.572, (136.181, 166.089, 169.19)), (' B 815  ARG HH11', ' B 823  PHE  HD2', -0.567, (132.873, 173.135, 138.375)), (' A 856  ILE HD12', ' A 858  LEU  HG ', -0.566, (177.317, 166.465, 163.002)), (' A 592  PHE  HZ ', ' B 855  TYR  HA ', -0.565, (140.836, 177.947, 164.094)), (' C 722  VAL HG22', ' C1065  VAL HG22', -0.562, (165.983, 138.205, 122.736)), (' A 239  GLN  NE2', ' A 240  THR  O  ', -0.56, (169.75, 215.711, 187.987)), (' C 905  ARG  NH1', ' C1035  GLY  O  ', -0.56, (157.102, 145.191, 119.782)), (' B 726  ILE HG12', ' B1061  VAL HG22', -0.558, (139.132, 162.014, 135.203)), (' A 563  GLN  O  ', ' A 577  ARG  NH1', -0.558, (121.719, 172.667, 179.991)), (' A 104  TRP  HE1', ' A 119  ILE HD12', -0.556, (174.807, 205.272, 187.307)), (' B 720  ILE HG13', ' B 923  ILE HG23', -0.555, (136.485, 157.307, 114.139)), (' B 856  ILE HG13', ' B 858  LEU HD13', -0.553, (144.233, 171.969, 165.056)), (' C 193  VAL  HB ', ' C 204  TYR  HB2', -0.55, (185.322, 127.812, 181.423)), (' B  95  THR HG22', ' B 189  LEU  HB3', -0.55, (104.108, 150.311, 175.954)), (' A1030  SER  HB3', ' C1041  ASP  HB2', -0.546, (168.726, 155.176, 126.993)), (' A  44  ARG HH21', ' C 567  ARG  HD2', -0.544, (177.133, 182.059, 170.483)), (' C1116  THR HG22', ' C1138  TYR  HB3', -0.544, (169.498, 153.539, 87.901)), (' A 826  VAL  HB ', ' A1057  PRO  HG2', -0.541, (177.284, 174.671, 140.61)), (' A1028  LYS  NZ ', ' A1042  PHE  O  ', -0.541, (163.068, 166.005, 128.892)), (' C 815  ARG  HD2', ' C 823  PHE  HE2', -0.536, (157.071, 129.838, 138.77)), (' A 908  GLY  O  ', ' A1038  LYS  NZ ', -0.536, (160.436, 161.452, 113.805)), (' A 787  GLN  OE1', ' C 703  ASN  ND2', -0.535, (185.218, 152.656, 120.828)), (' C 406  GLU  OE2', ' C 409  GLN  NE2', -0.534, (158.661, 177.572, 203.735)), (' C  86  PHE  HB2', ' C 238  PHE  HB2', -0.534, (193.025, 134.337, 190.321)), (' A 329  PHE  O  ', ' A 580  GLN  NE2', -0.532, (126.526, 183.121, 189.097)), (' C 326  ILE HG23', ' C 541  PHE  HA ', -0.531, (192.556, 171.418, 178.377)), (' C 908  GLY  O  ', ' C1038  LYS  NZ ', -0.53, (160.675, 151.987, 114.719)), (' A 326  ILE HG23', ' A 541  PHE  HA ', -0.53, (134.279, 184.784, 180.472)), (' A 960  ASN  CB ', ' C 570  LEU HD11', -0.528, (173.395, 175.315, 160.117)), (' B 856  ILE HG12', ' B 858  LEU HD13', -0.528, (143.329, 172.222, 164.329)), (' A 960  ASN  CG ', ' C 570  LEU HD11', -0.528, (173.814, 175.766, 160.371)), (' A 403  ARG  HD3', ' A 405  ASP  H  ', -0.524, (152.117, 155.78, 213.092)), (' C 366  SER  O  ', ' C 370  ASN  ND2', -0.521, (184.832, 167.416, 203.242)), (' B 193  VAL HG23', ' B 223  LEU HD22', -0.521, (115.888, 154.257, 179.535)), (' A 856  ILE  CD1', ' A 858  LEU  HG ', -0.517, (176.992, 167.036, 163.356)), (' A 193  VAL HG12', ' A 223  LEU HD22', -0.517, (174.236, 201.298, 175.578)), (' A 535  LYS  NZ ', ' A 554  GLU  OE1', -0.516, (121.372, 187.388, 174.057)), (' C 448  ASN  N  ', ' C 495  TYR  O  ', -0.516, (160.377, 182.765, 219.882)), (' A 448  ASN  N  ', ' A 497  PHE  O  ', -0.516, (144.77, 154.962, 224.199)), (' B  64  TRP  HE1', ' B 264  ALA  HB1', -0.514, (103.302, 142.879, 179.352)), (' B 715  PRO  HA ', ' B1072  GLU  HA ', -0.514, (139.907, 141.813, 110.95)), (' B 570  LEU  CD1', ' B 570  LEU  N  ', -0.511, (165.441, 135.545, 164.291)), (' A 825  LYS  HB2', ' A 945  LEU HD12', -0.511, (175.362, 178.74, 137.941)), (' A 596  SER  HB2', ' A 611  LEU  HB3', -0.509, (150.651, 187.237, 153.55)), (' C1028  LYS  NZ ', ' C1042  PHE  O  ', -0.506, (163.513, 149.784, 129.543)), (' C  33  THR  OG1', ' C 219  GLY  O  ', -0.503, (191.851, 126.622, 167.969)), (' C 231  ILE HD12', ' C 233  ILE  HB ', -0.503, (183.866, 134.232, 196.865)), (' C 210  ILE HG21', ' C 217  PRO  HG3', -0.502, (195.769, 119.546, 171.863)), (' C 773  GLU  OE2', ' C1019  ARG  NH2', -0.5, (153.069, 153.714, 147.011)), (' C 379  CYS  HA ', ' C 432  CYS  HA ', -0.498, (172.237, 171.882, 197.355)), (' B 570  LEU  O  ', ' B 571  ASP  HB2', -0.497, (166.961, 137.604, 169.164)), (' B 533  LEU HD11', ' B 585  LEU HD11', -0.497, (156.625, 120.135, 178.712)), (' A 403  ARG  NH1', ' A 504  GLY  O  ', -0.496, (153.109, 157.53, 215.367)), (' A  53  ASP  OD2', ' A 195  LYS  NZ ', -0.492, (170.525, 193.302, 178.094)), (' B  39  PRO  HG2', ' B  51  THR HG21', -0.49, (126.298, 157.368, 174.55)), (' B 557  LYS  HB2', ' B 584  ILE HG21', -0.488, (164.156, 120.624, 171.61)), (' B  48  LEU  HB3', ' B 276  LEU HD21', -0.485, (128.599, 157.04, 163.985)), (' A 707  TYR  HB3', ' B 792  PRO  HG3', -0.482, (137.867, 178.196, 113.993)), (' B 858  LEU HD23', ' B 959  LEU HD22', -0.481, (144.048, 169.637, 160.023)), (' A1011  GLN  OE1', ' A1014  ARG  NH1', -0.481, (167.683, 166.301, 153.584)), (' C 448  ASN  HB3', ' C 451  TYR  HD2', -0.478, (164.138, 183.257, 219.08)), (' C 856  ILE HG21', ' C 966  LEU  CD1', -0.477, (158.585, 140.784, 169.415)), (' C  48  LEU  HB3', ' C 276  LEU HD21', -0.477, (177.986, 134.909, 163.091)), (' B 666  ILE HD11', ' B 672  ALA  HB2', -0.475, (135.3, 136.138, 149.39)), (' C 276  LEU HD11', ' C 304  LYS  HA ', -0.475, (178.624, 138.245, 163.111)), (' C 303  LEU HD22', ' C 308  VAL HG12', -0.474, (181.251, 140.14, 155.826)), (' A1081  ILE HG21', ' A1135  ASN HD22', -0.474, (144.905, 168.916, 93.328)), (' C 341  VAL HG22', ' C 356  LYS  HD3', -0.471, (178.879, 185.508, 204.596)), (' B 722  VAL HG22', ' B1065  VAL HG22', -0.47, (137.99, 160.359, 122.014)), (' A 656  VAL HG12', ' A 658  ASN  H  ', -0.469, (144.817, 196.901, 136.311)), (' B 980  ILE HG23', ' B 984  LEU HD12', -0.468, (148.177, 169.773, 185.124)), (' C 656  VAL HG12', ' C 658  ASN  H  ', -0.467, (199.291, 150.909, 138.12)), (' A 381  GLY  HA3', ' A 430  THR HG23', -0.466, (143.408, 165.94, 191.371)), (' C 128  ILE  HB ', ' C 170  TYR  HB3', -0.465, (182.323, 122.137, 196.457)), (' A 303  LEU HD12', ' A 308  VAL HG22', -0.465, (164.156, 188.029, 154.236)), (' C  44  ARG  HB2', ' C 279  TYR  CD2', -0.463, (173.364, 129.432, 169.36)), (' C 948  LEU HD21', ' C1059  GLY  HA3', -0.461, (160.964, 141.141, 141.057)), (' B 215  ASP  N  ', ' B 266  TYR  HH ', -0.459, (105.275, 142.814, 174.268)), (' A 858  LEU HD13', ' A 959  LEU HD23', -0.459, (176.373, 168.188, 158.918)), (' C 569  ILE HG23', ' C 570  LEU HD23', -0.459, (177.708, 176.913, 161.044)), (' C 741  TYR  HD1', ' C 856  ILE HG13', -0.459, (156.156, 142.556, 167.883)), (' C 108  THR HG22', ' C 236  THR HG23', -0.457, (190.462, 140.011, 196.425)), (' C1011  GLN  OE1', ' C1014  ARG  NH1', -0.457, (160.346, 147.762, 154.96)), (' C 856  ILE HD11', ' C 858  LEU HD11', -0.456, (156.999, 141.958, 165.875)), (' B 381  GLY  HA3', ' B 430  THR  HA ', -0.456, (161.632, 140.645, 211.041)), (' B 206  LYS  HB2', ' B 223  LEU  HG ', -0.454, (113.564, 157.014, 176.943)), (' B1039  ARG  NE ', ' C1031  GLU  OE2', -0.452, (155.878, 155.532, 127.468)), (' A 743  CYS  HB3', ' A 749  CYS  HB3', -0.452, (177.522, 159.753, 175.135)), (' C 374  PHE  HA ', ' C 436  TRP  HB3', -0.451, (173.967, 170.632, 210.215)), (' A 811  LYS  NZ ', ' A 820  ASP  OD2', -0.45, (186.98, 177.772, 132.248)), (' B 598  ILE HG23', ' B 664  ILE HG21', -0.449, (134.396, 140.747, 150.798)), (' B 276  LEU HD11', ' B 304  LYS  HA ', -0.449, (131.276, 155.04, 163.625)), (' C 101  ILE  HA ', ' C 242  LEU  HA ', -0.449, (198.925, 119.752, 191.089)), (' B 570  LEU  N  ', ' B 570  LEU HD13', -0.449, (165.557, 135.253, 164.685)), (' A  56  LEU HD12', ' A  57  PRO  HD2', -0.448, (164.237, 202.095, 172.965)), (' A1086  LYS  HD2', ' A1122  VAL HG11', -0.448, (142.488, 156.198, 90.611)), (' A 564  GLN  OE1', ' A 577  ARG  NH2', -0.447, (122.849, 172.684, 183.019)), (' A 366  SER  O  ', ' A 370  ASN  ND2', -0.447, (142.952, 180.548, 204.269)), (' B  38  TYR  HE1', ' B 285  ILE HG13', -0.445, (119.809, 161.171, 171.875)), (' C 752  LEU HD11', ' C 990  GLU  HG2', -0.444, (150.977, 151.351, 184.15)), (' B 327  VAL HG22', ' B 542  ASN  HB3', -0.443, (154.929, 129.278, 186.258)), (' C 726  ILE HG13', ' C1061  VAL HG22', -0.443, (165.282, 139.805, 136.511)), (' B 908  GLY  O  ', ' B1038  LYS  NZ ', -0.443, (152.458, 156.83, 114.498)), (' B1074  ASN  OD1', ' C 895  GLN  NE2', -0.441, (143.131, 133.791, 112.003)), (' A 231  ILE HD12', ' A 233  ILE  HB ', -0.441, (169.001, 198.617, 194.779)), (' B 310  LYS  HG3', ' B 600  PRO  HA ', -0.441, (130.338, 144.642, 148.723)), (' B 880  GLY  O  ', ' B 884  SER  OG ', -0.439, (146.182, 173.688, 118.382)), (' A 569  ILE HG23', ' A 570  LEU  HG ', -0.439, (134.845, 169.175, 163.884)), (' B 743  CYS  HB3', ' B 749  CYS  HB3', -0.438, (151.296, 176.276, 175.443)), (' A 201  PHE  N  ', ' A 229  LEU  O  ', -0.438, (173.783, 194.642, 189.003)), (' C 331  ASN  N  ', ' C 331  ASN  OD1', -0.437, (195.415, 183.194, 188.63)), (' C 902  MET  HE1', ' C1049  LEU HD13', -0.437, (164.332, 140.999, 116.344)), (' A  32  PHE  HA ', ' A  32  PHE  HD1', -0.437, (166.392, 206.894, 164.588)), (' A 960  ASN  OD1', ' C 570  LEU HD21', -0.436, (175.519, 175.85, 159.884)), (' A 856  ILE  H  ', ' A 856  ILE HG13', -0.435, (179.239, 168.888, 164.243)), (' A 193  VAL HG13', ' A 204  TYR  HB2', -0.435, (174.879, 199.721, 177.693)), (' C 743  CYS  HB3', ' C 749  CYS  HB3', -0.434, (150.294, 145.633, 177.312)), (' C 393  THR  HA ', ' C 522  ALA  HA ', -0.434, (182.5, 183.716, 187.496)), (' B 725  GLU  OE1', ' B1064  HIS  NE2', -0.433, (145.103, 158.535, 129.778)), (' C 106  PHE  HB2', ' C 117  LEU  HB2', -0.433, (188.689, 130.6, 195.749)), (' A 598  ILE HG23', ' A 664  ILE HG21', -0.432, (154.517, 188.878, 147.445)), (' C 565  PHE  HB2', ' C 576  VAL HG12', -0.428, (185.379, 180.187, 174.822)), (' A 880  GLY  O  ', ' A 884  SER  OG ', -0.427, (178.503, 159.27, 118.616)), (' C 900  MET  HB3', ' C 900  MET  HE2', -0.424, (154.395, 138.948, 108.119)), (' A 570  LEU  HB3', ' B 963  VAL HG11', -0.423, (138.556, 168.16, 165.93)), (' B 570  LEU HD23', ' C 963  VAL HG11', -0.423, (162.018, 138.286, 166.029)), (' B 106  PHE  O  ', ' B 117  LEU  N  ', -0.423, (116.735, 149.781, 198.508)), (' B 736  VAL HG22', ' B 858  LEU  HG ', -0.422, (146.632, 171.595, 160.763)), (' A 727  LEU HD11', ' A1028  LYS  HD2', -0.421, (166.221, 165.566, 132.228)), (' B 752  LEU HD11', ' B 990  GLU  HG2', -0.421, (155.762, 173.597, 181.91)), (' C 130  VAL HG22', ' C 168  PHE  HB3', -0.421, (181.916, 128.035, 200.774)), (' A1074  ASN  OD1', ' B 895  GLN  NE2', -0.42, (145.733, 180.884, 108.958)), (' A 644  GLN  NE2', ' A 645  THR  O  ', -0.42, (139.345, 188.641, 151.293)), (' B 319  ARG HH21', ' C 740  MET  HB2', -0.419, (148.089, 141.151, 169.788)), (' C 568  ASP  HB3', ' C 572  ILE HG13', -0.418, (180.015, 176.359, 165.81)), (' B 131  CYS  HB2', ' B 133  PHE  CE1', -0.416, (113.645, 153.424, 205.56)), (' A 357  ARG  NH2', ' A 394  ASN  OD1', -0.416, (127.243, 165.517, 195.618)), (' A 360  ASN  H  ', ' A 523  THR HG22', -0.416, (126.196, 171.204, 195.246)), (' B 189  LEU HD23', ' B 210  ILE HD13', -0.415, (104.486, 150.583, 173.11)), (' B 811  LYS  NZ ', ' B 820  ASP  OD2', -0.414, (127.702, 172.641, 133.039)), (' A1086  LYS  HB3', ' A1122  VAL HG13', -0.413, (141.718, 157.859, 91.942)), (' C 642  VAL HG22', ' C 651  ILE HG12', -0.413, (199.072, 153.219, 156.589)), (' A 412  PRO  HB3', ' A 429  PHE  HB3', -0.41, (145.736, 159.394, 194.403)), (' A 365  TYR  CD2', ' A 387  LEU  HB3', -0.409, (139.726, 174.765, 197.112)), (' C  34  ARG HH21', ' C 217  PRO  HG2', -0.407, (194.037, 122.43, 170.85)), (' A 727  LEU HD12', ' A1062  PHE  HE2', -0.407, (168.704, 166.067, 132.697)), (' B 222  ALA  HB2', ' B 285  ILE  HB ', -0.407, (118.277, 158.782, 170.46)), (' C 342  PHE  HE1', ' C 511  VAL HG11', -0.406, (175.834, 179.067, 204.77)), (' A  37  TYR  OH ', ' A  54  LEU  O  ', -0.406, (169.299, 195.481, 176.828)), (' A 271  GLN HE21', ' A 273  ARG HH21', -0.405, (158.452, 199.005, 171.958)), (' C 344  ALA  HB3', ' C 347  PHE  HE1', -0.405, (176.798, 183.608, 211.491)), (' C 377  PHE  HE2', ' C 384  PRO  HB3', -0.404, (177.253, 168.111, 199.057)), (' C 357  ARG  HG3', ' C 396  TYR  HE1', -0.404, (176.951, 188.108, 195.683)), (' A 980  ILE HG23', ' A 984  LEU HD12', -0.404, (173.276, 166.374, 185.142)), (' C 530  SER  OG ', ' C 580  GLN  NE2', -0.403, (196.773, 178.302, 187.1)), (' B 596  SER  HB2', ' B 611  LEU  HB3', -0.402, (138.577, 138.763, 156.748)), (' C 409  GLN  HG3', ' C 416  GLY  HA3', -0.402, (156.694, 175.857, 203.398)), (' C 117  LEU  HG ', ' C 130  VAL HG12', -0.401, (185.303, 129.436, 197.474)), (' C 201  PHE  N  ', ' C 229  LEU  O  ', -0.401, (179.82, 131.981, 192.051)), (' B1029  MET  HE2', ' B1053  PRO  HB3', -0.4, (145.179, 167.793, 129.484)), (' B1040  VAL HG21', ' C1035  GLY  HA3', -0.4, (153.723, 148.801, 121.685)), (' C  36  VAL HG22', ' C 275  PHE  HE2', -0.4, (186.935, 132.635, 171.919)), (' B  92  PHE  HB3', ' B 192  PHE  HB2', -0.4, (111.956, 151.372, 183.77))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
