import wx
import wx.grid as gridlib
import csv


class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title,
                                        size=(350, 250))
        self.content_saved = True
        self.main_grid = None
        self.init_ux()

    def init_ux(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()

        file_menu.AppendSeparator()
        menu_bar.Append(file_menu, '&File')

        # add open file menu
        open_menu = wx.Menu()
        csv_btn = open_menu.Append(wx.ID_ANY, 'Load CSV File')
        pipe_btn = open_menu.Append(wx.ID_ANY, 'Load Piped File')
        tabd_btn = open_menu.Append(wx.ID_ANY, 'Load Tabbed File')

        # append open_menu to the file_menu
        file_menu.Append(wx.ID_OPEN, '&Open', open_menu)

        # append quit button to file menu
        quit_button = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.quit_program, quit_button)
        self.Bind(wx.EVT_MENU, lambda event: self.open_dialog(file_type='csv'), csv_btn)
        self.Bind(wx.EVT_MENU, lambda event: self.open_dialog(file_type='pipe'), pipe_btn)
        self.Bind(wx.EVT_MENU, lambda event: self.open_dialog(file_type='tab'), tabd_btn)
        self.SetSize((300, 200))
        self.Centre()

    def open_dialog(self, file_type):

        file_type_dct = {
            'csv': {
                'extension': '.csv',
                'delimiter': ',',
                'wildcard': 'CSV Files (*.csv)|*.csv'
            },
            'pipe': {
                'extension': 'ANY',
                'delimiter': '|',
                'wildcard': 'Any File|*'
            },
            'tab': {
                'extension': 'ANY',
                'delimiter': '\t',
                'wildcard': 'Any File|*'
            }
        }
        if not self.content_saved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        with wx.FileDialog(self, "Open " + file_type + " delimited file",
                           wildcard=file_type_dct[file_type]['wildcard'],
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            file_path = fileDialog.GetPath()
            try:
                data_rows = self.get_data_rows(file_path, file_type_dct[file_type]['delimiter'])

                self.set_grid_data(data_rows)
            except IOError:
                wx.LogError("Cannot open file '%s'." % file_path)

    def get_data_rows(self, file_path, delimiter):
        with open(file_path, 'r') as file:
            list_of_text_lines = csv.reader(file, delimiter=delimiter)

            list_of_data_rows = []
            for line in list_of_text_lines:
                list_of_data_rows.append(line)

        return list_of_data_rows

    def create_grid_view(self, row_count, col_count):
        # set up grid panel
        panel = wx.Panel(self)
        self.main_grid = gridlib.Grid(panel)
        self.main_grid.CreateGrid(row_count, col_count)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.main_grid, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        panel.Fit()

    def set_grid_data(self, row_list):
        if not self.main_grid:
            self.create_grid_view(len(row_list), len(row_list[0]))

        for row_index in range(len(row_list)):
            for col_index in range(len(row_list[row_index])):
                self.main_grid.SetCellValue(row_index, col_index, row_list[row_index][col_index])

    def quit_program(self, e):
        self.Close()
