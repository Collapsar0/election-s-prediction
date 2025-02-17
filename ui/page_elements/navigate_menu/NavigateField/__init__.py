from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtWidgets import QWidget

from config.uicolor import UIColor as color
from libs.link_manager import link_manager
from ui.page_elements.navigate_menu.NavigateLabel import NavigateLabel

from .NavigateFieldUI import Ui_Form


class NavigateField(QWidget):
    def __init__(self, title: str, alias: str = ""):
        QWidget.__init__(self)
        self.menu_labels = []
        self.is_hide = True
        self.title = title
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.label_title.set_title(title, alias)
        self.ui.label_title.checkChanged.connect(self.refresh_ui)

        self.ui.label_icon.setPixmap(QPixmap("./static/svg/list.svg").scaled(30, 30))
        self.ui.label_icon.setAutoFillBackground(True)

        self.ui.label_switch.setAutoFillBackground(True)
        self.ui.label_switch.linkActivated.connect(self.switch)
        self.ui.label_switch.close()

        self.refresh_ui(False)
        self.adjustSize()

    def switch(self):
        self.is_hide = not self.is_hide
        t = self.ui.label_switch.text()
        if self.is_hide:
            t = t.replace('隐藏', '展开')
        else:
            t = t.replace('展开', '隐藏')
        self.ui.label_switch.setText(t)
        for i in self.menu_labels:
            if self.is_hide:
                i.hide()
            else:
                i.show()

    def refresh_switch_button(self, checked):
        text_color = color.NavigateHideTextHighlight if checked else color.NavigateHideText
        s = '<a href="#" style="text-decoration: none;' \
            'color: {color};">{0}</a>'.format("展开" if self.is_hide else "隐藏", color=text_color.name())
        self.ui.label_switch.setText(s)

    def append_menu(self, text: str, alias=""):
        label = NavigateLabel(self)
        label.set_title(text, alias)
        label.setParent(self)
        label.setStyleSheet("QLabel{margin-left: 10px;}")
        if self.is_hide:
            label.hide()
        label.linkActivated.connect(link_manager.activate)
        label.checkChanged.connect(self.ui.label_title.setChecked)
        self.ui.layout_menu.addWidget(label)
        self.menu_labels.append(label)
        self.ui.label_switch.show()
        return label

    def refresh_ui(self, checked):
        bgcolor = color.NavigateBackgroundHighlight if checked else color.NavigateBackground
        pal = self.ui.label_switch.palette()
        pal.setColor(QPalette.Background, bgcolor)
        self.ui.label_switch.setPalette(pal)
        self.ui.label_icon.setPalette(pal)
        self.ui.title_widget.setPalette(pal)
        self.refresh_switch_button(checked)
