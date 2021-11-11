import wx, math, threading as thread
from time import sleep

app = wx.App()
frm = wx.Frame(None, title="Shitty Calculator", size=(300, 60))
frm.SetMaxSize((300, 60))
frm.SetMinSize((90, 60))
label = wx.StaticText(frm, label="Answer: ")
label_font: wx.Font = label.GetFont()
label_font.PointSize += 10
label.SetFont(label_font)

ID_ANS = 1337

def create_operator_menu():
  """
  Create a submenu to select operator.
  """
  menu = wx.Menu()
  menu.AppendRadioItem(wx.ID_ANY, "Add")
  menu.AppendRadioItem(wx.ID_ANY, "Subtract")
  menu.AppendRadioItem(wx.ID_ANY, "Multiply")
  menu.AppendRadioItem(wx.ID_ANY, "Divide")
  return menu

def create_number_menu(menu: wx.Menu):
  """
  Create a list of number to select through the menu
  """
  menu.AppendSeparator()
  for i in range(11):
    menu.AppendRadioItem(wx.ID_ANY, str(i))
  return menu
  
class WxMenuBarCalculator():
  """
  Class to create a calculator with wx.MenuBar.
  """ 
  def __init__(self, frm):
    """
    Initalizer class. There should two number menu and one operator menu in the following order:
    1. Number menu
    2. Operator menu
    3. Number menu
    4. Result menu
    """
    self.frm = frm
    # Create the menu bar menus
    self.number_menu_1 = create_number_menu(wx.Menu())
    self.number_menu_1_ans_btn: wx.MenuItem = self.number_menu_1.AppendRadioItem(ID_ANS, "ans")
    self.number__menu_1_no_after_0: wx.Menu = create_number_menu(wx.Menu())
    # Add the number after the 0 to the number menu
    self.number_menu_1.AppendSubMenu(self.number__menu_1_no_after_0, "Number after 0")

    self.number_menu_2 = create_number_menu(wx.Menu())
    self.number_menu_2_ans_btn: wx.MenuItem = self.number_menu_2.AppendRadioItem(ID_ANS, "ans")
    self.number__menu_2_no_after_0: wx.Menu = create_number_menu(wx.Menu())
    # Add the number after the 0 to the number menu
    self.number_menu_2.AppendSubMenu(self.number__menu_2_no_after_0, "Number after 0")

    self.operator_menu = create_operator_menu()
    # Create a result menu
    self.result_menu = wx.Menu()
    self.calc_result: wx.MenuItem = self.result_menu.Append(wx.ID_ANY, "Calculate result")
    self.result_label: wx.MenuItem = self.result_menu.Append(wx.ID_ANY, "Result: ", kind=wx.ITEM_NORMAL)
    self.result_label.Enable(False)

    # Create menu bar
    self.menubar = wx.MenuBar()
    self.menubar.Append(self.number_menu_1, "Number 1")
    self.menubar.Append(self.operator_menu, "Operator")
    self.menubar.Append(self.number_menu_2, "Number 2")
    self.menubar.Append(self.result_menu, "Result")
    
    # Bind events
    self.operator_menu.Bind(wx.EVT_MENU, self.on_operator_select)
    self.number_menu_1.Bind(wx.EVT_MENU, self.on_number_1_select)
    self.number_menu_2.Bind(wx.EVT_MENU, self.on_number_2_select)
    self.result_menu.Bind(wx.EVT_MENU, self.on_calculate_result)
    # Set the menu bar
    self.frm.SetMenuBar(self.menubar)
    # Set the default operator and number
    self.selected_operator = "+"
    self.number_1 = "0"
    self.number_2 = "0"
    self.ans = "0"
    # Make it so the ans is always shown in it's label
    def update_ans_thread():
      while True:
        self.number_menu_1_ans_btn.SetItemLabel(f"ans ({self.ans})")
        self.number_menu_2_ans_btn.SetItemLabel(f"ans ({self.ans})")
        sleep(0.1)
    thread.Thread(target=update_ans_thread).start()
  # Getters and setter
  @property
  def answer(self):
    try:
      ans = eval(f"{self.number_1} {self.selected_operator} {self.number_2}") 
    except:
      ans = math.nan
    finally:
      self.ans = str(ans)
      return ans
  # Event handlers
  def on_operator_select(self, event: wx.MenuEvent):
    self.selected_operator = ""
    for menu_item  in self.operator_menu.GetMenuItems():
      if menu_item.IsChecked():
        self.selected_operator = menu_item.GetItemLabel()
        break
    # find the selected operator symbol
    if self.selected_operator == "Add":
      self.selected_operator = "+"
    elif self.selected_operator == "Subtract":
      self.selected_operator = "-"
    elif self.selected_operator == "Multiply":
      self.selected_operator = "*"
    elif self.selected_operator == "Divide":
      self.selected_operator = "/"
  def on_number_1_select(self, event: wx.MenuEvent):
    sel_menu = ""
    # Get the selected number
    for menu_item in self.number_menu_1.GetMenuItems():
      if menu_item.IsChecked():
        if menu_item.GetId() == ID_ANS:
          sel_menu = self.ans
        else:
          sel_menu = str(menu_item.GetItemLabel())
        break
    # Get the selected value to know the number after the 0
    no_after_0 = 0
    for menu_item in self.number__menu_1_no_after_0.GetMenuItems():
      if menu_item.IsChecked():
        no_after_0 = int(menu_item.GetItemLabel())
        break

    # Set the number 1 value
    self.number_1 = sel_menu + (no_after_0 * "0")
  def on_number_2_select(self, event: wx.MenuEvent):
    selected_number = ""
    # Get the selected number
    for menu_item in self.number_menu_2.GetMenuItems():
      if menu_item.IsChecked():
        if menu_item.GetId() == ID_ANS:
          selected_number = self.ans
        else:
          selected_number = str(menu_item.GetItemLabel())
        break
    # Get the selected value to know the number after the 0
    no_after_0 = 0
    for menu_item in self.number__menu_2_no_after_0.GetMenuItems():
      if menu_item.IsChecked():
        no_after_0 = int(menu_item.GetItemLabel())
        break

    # Set the number 2 value
    self.number_2 = selected_number + (no_after_0 * "0")
    print(self.number_2, self.number_1, self.selected_operator)
  def on_calculate_result(self, event: wx.MenuEvent):
    answer_text = f"Answer: {self.answer}"
    self.result_label.SetItemLabel(answer_text)
    label.SetLabel(answer_text)
    
shit_calculator = WxMenuBarCalculator(frm)
frm.Show()
app.MainLoop()