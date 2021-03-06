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
data['rama'] = [('A', ' 184 ', 'PRO', 0.04317556240022559, (6.880000000000001, -9.653999999999998, 6.590000000000002)), ('A', ' 302 ', 'GLY', 0.012038027240375934, (-10.883999999999997, -23.87399999999999, 35.931)), ('B', '  51 ', 'ASN', 0.04095236395994277, (-34.931000000000004, -35.491, 45.75100000000001)), ('B', ' 154 ', 'TYR', 0.022960018725321194, (-26.83700000000001, -1.9749999999999996, 21.661)), ('B', ' 275 ', 'GLY', 0.010180269465824038, (-20.216, -36.893, 2.152))]
data['omega'] = []
data['rota'] = [('A', '  24 ', 'THR', 0.2972016895351662, (-12.861, 10.964, 7.221)), ('A', '  27 ', 'LEU', 0.12750729720101328, (-10.749, 3.7350000000000003, 13.567)), ('A', '  45 ', 'THR', 0.13039835116581872, (-7.093999999999998, 9.453, 3.479)), ('A', '  49 ', 'MET', 0.12701823279036928, (-2.808, 4.154999999999999, 1.694)), ('A', '  59 ', 'ILE', 0.008733728746002725, (4.92, 16.347999999999992, 10.282000000000004)), ('A', '  73 ', 'VAL', 0.25408137029812083, (-16.998, 12.623999999999995, 25.653)), ('A', '  77 ', 'VAL', 0.15156510151113464, (-5.1359999999999975, 15.118, 22.513)), ('A', ' 104 ', 'VAL', 0.049846988470859034, (4.341000000000002, -8.695, 24.620000000000008)), ('A', ' 106 ', 'ILE', 0.06885002509188524, (3.6179999999999994, -13.247999999999998, 20.496)), ('A', ' 107 ', 'GLN', 0.16465467664429065, (5.132999999999997, -16.202999999999992, 18.611)), ('A', ' 121 ', 'SER', 0.15618160173890708, (-17.419, 0.372, 20.639)), ('A', ' 141 ', 'LEU', 0.0015019300567900866, (-15.089000000000002, -5.631999999999998, 8.661)), ('A', ' 142 ', 'ASN', 0.014192311260909956, (-13.867000000000003, -2.145, 7.762)), ('A', ' 153 ', 'ASP', 0.17050723001029677, (-2.8599999999999977, -13.589, 33.429)), ('A', ' 169 ', 'THR', 0.2721599731661606, (-6.281, -13.896999999999998, 0.999)), ('A', ' 190 ', 'THR', 0.2622090328937816, (0.9780000000000002, -2.516, -1.9680000000000002)), ('A', ' 254 ', 'SER', 0.06547890421867196, (2.0660000000000016, -35.260999999999996, 29.426000000000005)), ('A', ' 268 ', 'LEU', 8.693788451822121e-05, (-1.2889999999999993, -38.658, 15.849)), ('A', ' 276 ', 'MET', 0.15759233737187944, (-10.667, -40.717, 11.748)), ('A', ' 289 ', 'ASP', 0.14082558934413653, (-4.912, -26.74199999999999, 15.821)), ('B', '   6 ', 'MET', 0.10680655936938796, (-18.209, -14.697999999999995, 18.187)), ('B', '  27 ', 'LEU', 0.2256073992957729, (-21.651000000000003, -21.258, 43.161)), ('B', '  49 ', 'MET', 0.08610268605974658, (-29.89700000000001, -33.453999999999986, 46.097000000000016)), ('B', '  77 ', 'VAL', 0.003150532575091347, (-28.315999999999995, -10.526999999999996, 52.512)), ('B', '  93 ', 'THR', 0.2864419986478819, (-25.936, -2.726999999999999, 48.715)), ('B', ' 106 ', 'ILE', 0.008812156776962772, (-35.08899999999999, -18.039, 24.422)), ('B', ' 121 ', 'SER', 0.22278880889881747, (-14.739999999999998, -14.891999999999994, 39.043)), ('B', ' 136 ', 'ILE', 0.08134371832370675, (-26.425999999999995, -26.768, 25.776)), ('B', ' 141 ', 'LEU', 0.28705584720783944, (-16.745999999999995, -28.061, 35.289)), ('B', ' 153 ', 'ASP', 0.2470547221828883, (-28.567, -5.333999999999998, 21.854)), ('B', ' 165 ', 'MET', 0.03833792024926716, (-26.386000000000003, -28.914999999999992, 36.194)), ('B', ' 167 ', 'LEU', 0.13653919923395003, (-26.599000000000004, -34.47699999999998, 32.522)), ('B', ' 189 ', 'GLN', 0.0772870883752256, (-29.97700000000001, -35.978, 41.459)), ('B', ' 196 ', 'THR', 0.0009391766436530678, (-32.858999999999995, -36.803, 21.155)), ('B', ' 222 ', 'ARG', 0.005095818713156894, (-27.519000000000005, -26.057, -10.331)), ('B', ' 227 ', 'LEU', 0.0026977042880725064, (-39.506, -27.522999999999996, 0.586)), ('B', ' 245 ', 'ASP', 0.11453427363158068, (-41.101, -19.368, 8.216)), ('B', ' 268 ', 'LEU', 0.08291912690705147, (-27.363000000000007, -28.784999999999997, 1.516)), ('B', ' 297 ', 'VAL', 0.138577480869803, (-25.94, -10.954999999999997, 9.003))]
data['cbeta'] = []
data['probe'] = [(' A  49  MET  HA ', ' A  49  MET  HE2', -0.864, (-1.753, 3.638, 2.662)), (' B  20  VAL HG22', ' B  68  VAL HG22', -0.796, (-24.748, -14.177, 47.454)), (' B 153  ASP  HB2', ' B 338  HOH  O  ', -0.79, (-31.558, -5.106, 22.993)), (' A 303  VAL HG12', ' A 361  HOH  O  ', -0.784, (-6.942, -18.171, 34.921)), (' A 142  ASN  H  ', ' A 142  ASN HD22', -0.784, (-15.431, -3.256, 6.635)), (' A 186  VAL  H  ', ' A 192  GLN HE22', -0.743, (3.48, -4.948, 4.128)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.729, (-30.672, -23.953, 16.625)), (' B  22  CYS  SG ', ' B  61  LYS  NZ ', -0.726, (-27.42, -22.564, 52.615)), (' A  48  ASP  O  ', ' A  52  PRO  HB3', -0.718, (-0.06, 7.232, 1.706)), (' A 231  ASN  O  ', ' A 235  MET  HG3', -0.706, (7.783, -34.546, 8.37)), (' A 142  ASN  N  ', ' A 142  ASN HD22', -0.703, (-15.281, -3.091, 7.388)), (' B 140  PHE  HB2', ' B 172  HIS  NE2', -0.673, (-20.859, -28.316, 31.224)), (' B 165  MET  HE3', ' B 187  ASP  HA ', -0.661, (-31.21, -30.316, 38.403)), (' B 276  MET  HE3', ' B 281  ILE HG13', -0.66, (-17.995, -28.62, 3.889)), (' B  52  PRO  HD2', ' B 188  ARG  HG2', -0.659, (-35.219, -32.606, 44.743)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.655, (-0.482, 6.478, 13.106)), (' A   8  PHE  HE1', ' A 305  PHE  CZ ', -0.653, (-6.783, -16.911, 31.379)), (' A 305  PHE  HB2', ' B 358  HOH  O  ', -0.651, (-9.862, -13.247, 33.3)), (' B  60  ARG  HD3', ' B 323  HOH  O  ', -0.628, (-36.234, -28.634, 59.397)), (' A 276  MET  HE3', ' A 281  ILE HD12', -0.62, (-9.225, -37.176, 16.251)), (' A  76  ARG  NH1', ' A  92  ASP  OD2', -0.62, (-7.658, 18.289, 27.859)), (' A 111  THR HG22', ' A 129  ALA  HB2', -0.609, (-4.622, -19.644, 17.885)), (' A  52  PRO  HD2', ' A 188  ARG  HG2', -0.608, (2.45, 3.523, 2.339)), (' B 140  PHE  HB2', ' B 172  HIS  CE1', -0.603, (-21.004, -27.269, 31.144)), (' A  31  TRP  CE2', ' A  75  LEU HD11', -0.593, (-8.463, 8.417, 27.244)), (' A  49  MET  CE ', ' A  49  MET  HA ', -0.593, (-2.336, 3.551, 3.636)), (' A  31  TRP  CZ2', ' A  75  LEU HD11', -0.586, (-9.168, 8.955, 27.431)), (' B  31  TRP  CE2', ' B  95  ASN  HB2', -0.586, (-24.804, -5.352, 42.615)), (' B  49  MET  HA ', ' B  49  MET  HE2', -0.582, (-30.278, -32.466, 45.019)), (' B  76  ARG  HB3', ' B  92  ASP  OD1', -0.58, (-26.083, -6.14, 53.227)), (' A 169  THR  HB ', ' A 171  VAL HG22', -0.577, (-4.986, -13.612, 3.805)), (' B 239  TYR  CE1', ' B 272  LEU HD21', -0.573, (-27.981, -32.785, 7.63)), (' A  19  GLN HE21', ' A  26  THR HG21', -0.573, (-15.78, 6.514, 13.945)), (' B 217  ARG  HB2', ' B 220  LEU HD12', -0.56, (-21.455, -21.097, -5.009)), (' B 269  LYS  HG2', ' B 273  GLN HE22', -0.559, (-30.473, -34.594, -1.631)), (' B  60  ARG  NH1', ' B 323  HOH  O  ', -0.559, (-36.809, -29.251, 59.065)), (' B  66  PHE  HB2', ' B  77  VAL HG11', -0.549, (-27.236, -14.849, 52.458)), (' B 186  VAL  H  ', ' B 192  GLN HE22', -0.548, (-34.441, -32.762, 35.365)), (' B 274  ASN  O  ', ' B 275  GLY  C  ', -0.547, (-20.275, -35.613, 0.5)), (' B 175  THR HG22', ' B 181  PHE  HA ', -0.536, (-34.566, -23.892, 34.322)), (' B 187  ASP  O  ', ' B 188  ARG  HG3', -0.536, (-34.017, -31.321, 41.984)), (' B 230  PHE  HZ ', ' B 268  LEU HD13', -0.532, (-30.608, -28.465, 4.62)), (' B 113  SER  O  ', ' B 149  GLY  HA2', -0.531, (-24.768, -16.828, 27.962)), (' B 205  LEU HD21', ' B 268  LEU HD12', -0.53, (-30.029, -25.969, 4.061)), (' A 207  TRP  CE2', ' A 288  GLU  HB2', -0.529, (-9.321, -29.979, 18.084)), (' B 105  ARG  NH1', ' B 180  LYS  HB3', -0.528, (-38.518, -21.903, 31.778)), (' A 140  PHE  O  ', ' B   1  SER  N  ', -0.527, (-12.973, -8.893, 7.489)), (' B  56  ASP  OD2', ' B  60  ARG  NH2', -0.527, (-37.475, -29.916, 55.286)), (' B 108  PRO  HA ', ' B 130  MET  HG2', -0.527, (-32.998, -23.633, 22.039)), (' A  86  LEU  HG ', ' A 179  GLY  HA2', -0.526, (3.012, -0.131, 15.983)), (' A   3  PHE  HA ', ' A 322  HOH  O  ', -0.526, (-14.052, -26.968, 26.306)), (' B 205  LEU  CD2', ' B 268  LEU HD12', -0.524, (-29.401, -26.226, 4.108)), (' B  73  VAL HG12', ' B  74  GLN  O  ', -0.518, (-19.688, -6.963, 51.012)), (' B 291  PHE  HB2', ' B 307  HOH  O  ', -0.518, (-24.341, -21.518, 11.585)), (' A 167  LEU HD21', ' A 185  PHE  CE1', -0.516, (0.38, -10.842, 4.324)), (' A 132  PRO  HD2', ' A 197  ASP  OD2', -0.516, (0.023, -21.159, 9.346)), (' B 269  LYS  HG2', ' B 273  GLN  NE2', -0.512, (-30.195, -34.087, -1.598)), (' A 187  ASP  O  ', ' A 188  ARG  HG3', -0.51, (1.939, 1.627, 4.17)), (' B 207  TRP  CE2', ' B 288  GLU  HB2', -0.508, (-20.766, -24.229, 9.959)), (' B 132  PRO  HD2', ' B 197  ASP  OD2', -0.504, (-30.903, -30.207, 19.119)), (' A   3  PHE  HE1', ' A 300  CYS  HG ', -0.503, (-9.636, -28.442, 28.669)), (' B 230  PHE  CZ ', ' B 268  LEU HD13', -0.496, (-30.993, -28.757, 4.249)), (' A 184  PRO  HD2', ' A 185  PHE  CE2', -0.496, (3.398, -11.462, 6.602)), (' A 107  GLN  HA ', ' A 107  GLN HE21', -0.492, (6.754, -15.869, 17.614)), (' B 269  LYS  CG ', ' B 273  GLN HE22', -0.488, (-30.793, -34.021, -1.883)), (' A 100  LYS  HD2', ' A 155  ASP  OD2', -0.486, (-3.17, -6.763, 38.775)), (' A 126  TYR  CD1', ' B   4  ARG  HG3', -0.486, (-12.189, -14.381, 15.615)), (' A  21  THR  HB ', ' A  67  LEU  HB3', -0.485, (-11.972, 12.633, 14.844)), (' B  31  TRP  CD2', ' B  95  ASN  HB2', -0.482, (-24.233, -5.978, 42.514)), (' A  84  ASN  ND2', ' A 180  LYS  HD2', -0.48, (8.548, -1.31, 15.891)), (' B  44  CYS  SG ', ' B  49  MET  HE3', -0.48, (-30.26, -29.575, 45.64)), (' B  63  ASN  O  ', ' B  77  VAL HG13', -0.479, (-27.943, -13.724, 54.584)), (' A 142  ASN  H  ', ' A 142  ASN  ND2', -0.478, (-15.824, -2.883, 6.588)), (' B 148  VAL HG22', ' B 320  HOH  O  ', -0.477, (-22.839, -15.236, 33.642)), (' A  52  PRO  HG2', ' A  54  TYR  CE1', -0.475, (2.119, 5.131, 4.757)), (' B 140  PHE  HD1', ' B 172  HIS  CG ', -0.473, (-22.766, -26.63, 30.86)), (' B 227  LEU HD12', ' B 231  ASN  ND2', -0.473, (-39.897, -28.517, 4.016)), (' A  27  LEU HD11', ' A  42  VAL  HB ', -0.471, (-6.566, 5.532, 13.202)), (' A 108  PRO  HA ', ' A 130  MET  HG3', -0.47, (2.494, -17.15, 15.135)), (' A 140  PHE  H  ', ' B   1  SER  N  ', -0.469, (-13.078, -9.884, 9.11)), (' B 141  LEU  N  ', ' B 141  LEU HD12', -0.469, (-16.577, -27.457, 33.369)), (' B  21  THR  OG1', ' B  26  THR HG23', -0.468, (-19.743, -19.488, 48.157)), (' B  27  LEU HD11', ' B  42  VAL  HB ', -0.468, (-26.02, -21.317, 44.831)), (' A  19  GLN  O  ', ' A  68  VAL  HA ', -0.468, (-11.001, 9.173, 19.006)), (' B 238  ASN  HB3', ' B 313  HOH  O  ', -0.466, (-28.793, -35.751, 12.434)), (' A   9  PRO  HD3', ' B 124  GLY  HA2', -0.466, (-12.794, -15.44, 29.966)), (' A   3  PHE  HE1', ' A 300  CYS  SG ', -0.463, (-9.919, -28.865, 28.651)), (' B 276  MET  CE ', ' B 281  ILE HG13', -0.461, (-17.795, -28.549, 4.141)), (' B  84  ASN  HB2', ' B 179  GLY  HA3', -0.46, (-37.957, -20.599, 38.474)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.458, (-6.655, 4.095, 31.434)), (' A   8  PHE  CE1', ' A 305  PHE  CZ ', -0.456, (-7.463, -16.057, 30.947)), (' A   5  LYS  HA ', ' A 291  PHE  CZ ', -0.455, (-11.563, -23.716, 22.096)), (' B 141  LEU  O  ', ' B 142  ASN  C  ', -0.454, (-17.867, -26.855, 38.265)), (' B 163  HIS  CE1', ' B 172  HIS  HB3', -0.453, (-24.642, -27.237, 32.057)), (' A  30  LEU  HB3', ' A  37  TYR  HB2', -0.447, (-3.499, 1.618, 21.894)), (' A 276  MET  CE ', ' A 281  ILE HD12', -0.447, (-10.098, -37.039, 16.103)), (' A 207  TRP  CD2', ' A 288  GLU  HB2', -0.446, (-8.621, -30.329, 18.53)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.445, (-14.114, -3.924, 12.103)), (' B  40  ARG  HD3', ' B  85  CYS  HA ', -0.443, (-35.476, -23.436, 42.179)), (' A  49  MET  HE1', ' A  54  TYR  OH ', -0.441, (-0.802, 2.965, 5.492)), (' A 136  ILE  O  ', ' A 136  ILE HG13', -0.441, (-6.013, -12.677, 11.318)), (' A   1  SER  HB2', ' B 140  PHE  H  ', -0.438, (-17.412, -28.141, 30.729)), (' B 263  ASP  O  ', ' B 266  ALA  HB3', -0.435, (-29.894, -25.797, -3.885)), (' A  74  GLN  HB3', ' A 349  HOH  O  ', -0.433, (-12.209, 15.971, 22.049)), (' A 106  ILE HD12', ' A 160  CYS  SG ', -0.43, (-0.655, -12.284, 21.877)), (' B   4  ARG  HA ', ' B   4  ARG  HD3', -0.427, (-13.894, -17.988, 13.356)), (' A 111  THR HG21', ' A 290  GLU  O  ', -0.427, (-5.769, -21.688, 19.745)), (' B 274  ASN  O  ', ' B 275  GLY  O  ', -0.425, (-20.743, -35.134, 1.201)), (' A 138  GLY  O  ', ' B   2  GLY  HA3', -0.424, (-12.183, -13.888, 9.684)), (' A 235  MET  HE3', ' A 241  PRO  HG3', -0.424, (8.782, -29.547, 8.943)), (' A 154  TYR  HB2', ' A 155  ASP  H  ', -0.422, (-2.822, -11.449, 37.182)), (' A  41  HIS  HB2', ' A  49  MET  HE3', -0.422, (-2.73, 4.126, 5.972)), (' B 234  ALA  O  ', ' B 239  TYR  HB2', -0.42, (-32.155, -33.51, 8.269)), (' A 276  MET  O  ', ' A 277  ASN  HB2', -0.419, (-12.058, -43.596, 12.418)), (' B 161  TYR  CE1', ' B 174  GLY  HA3', -0.419, (-29.654, -23.608, 32.044)), (' B  40  ARG  HA ', ' B  87  LEU  HG ', -0.417, (-31.669, -21.242, 45.389)), (' B 217  ARG  HG2', ' B 217  ARG HH11', -0.417, (-17.717, -18.355, -5.202)), (' B 115  LEU HD11', ' B 122  PRO  HB3', -0.415, (-15.842, -13.715, 33.102)), (' B 121  SER  HA ', ' B 122  PRO  HD3', -0.413, (-15.037, -13.22, 38.668)), (' A 136  ILE HG13', ' A 172  HIS  HB2', -0.411, (-5.915, -11.78, 11.217)), (' B 233  VAL  O  ', ' B 236  LYS  HB2', -0.41, (-32.975, -37.367, 4.81)), (' A  75  LEU  HA ', ' A  75  LEU HD23', -0.409, (-10.662, 13.552, 26.656)), (' A  43  ILE  HB ', ' A  61  LYS  HE3', -0.407, (-2.676, 12.012, 9.727)), (' A   3  PHE  CE1', ' A 300  CYS  SG ', -0.407, (-10.121, -28.794, 28.236)), (' B 176  ASP  HB2', ' B 308  HOH  O  ', -0.406, (-35.297, -16.046, 31.43)), (' A 296  VAL  O  ', ' A 297  VAL  C  ', -0.406, (-6.097, -26.023, 31.137)), (' A  43  ILE  CB ', ' A  61  LYS  HE3', -0.406, (-2.887, 11.806, 9.915)), (' A 140  PHE  HD1', ' A 172  HIS  CG ', -0.405, (-8.713, -9.834, 10.043)), (' A  40  ARG  HD3', ' A  85  CYS  HA ', -0.401, (3.412, 3.567, 11.903)), (' A  75  LEU HD13', ' A  91  VAL HG11', -0.401, (-7.199, 10.824, 25.264)), (' B 133  ASN  O  ', ' B 134  HIS  HB2', -0.401, (-33.79, -30.043, 25.847)), (' A  75  LEU HD21', ' A  93  THR  HB ', -0.401, (-8.991, 11.585, 28.878)), (' A 122  PRO  HB2', ' B   9  PRO  HG2', -0.4, (-18.144, -5.081, 22.33))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
