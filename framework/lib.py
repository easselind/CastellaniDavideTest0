import threading
import time
from math import ceil

from PIL import ImageDraw, Image
from queue import LifoQueue

from framework.struct import Page as _Page, Element as _Element, Book as _Book, Base as _Base
from enviroment.touchscreen import Clicked, SlideX, SlideY


class Elements:
    class Image(_Element):
        def __init__(self, page, location=(0, 0), image=None):
            super().__init__(page, location)
            self._image = image

        @property
        def image(self):
            return self._image

        @image.setter
        def image(self, value, update=True):
            self._image = value
            if update:
                self.page.update()

        def render(self):
            return self._image

    class TextElement(_Element):
        def __init__(self, page, location=(0, 0), text="", font_size=13, color="black", background=None):
            super().__init__(page, location)
            self.font_size = font_size
            self.color = color
            self._background = background
            self.text = text
            self.background = None
            self._font = None
            self.image = None
            self._image_draw = None
            self.update(False)

        def update(self, update=True):
            self.background = Image.new("RGBA", (296, 128), self._background) if self._background else \
                Image.new("RGBA", (296, 128), (255, 255, 255, 0))
            self.image = self.background.copy()
            self._image_draw = ImageDraw.ImageDraw(self.image)
            self._image_draw.text((0, 0), self.text, self.color, self._font)
            if update:
                self.page.update()

        def set_text(self, value, update=True):
            self.text = value
            self.update(update)

        def set_color(self, value, update=True):
            self.color = value
            self.update(update)

        def set_background(self, value, update=True):
            self._background = value
            self.update(update)

        def set_font_size(self, value, update=True):
            self.font_size = value
            self._font = self.page.book.get_font(value)
            self.update(update)

        def render(self) -> Image:
            return self.image

    class Label(TextElement):
        def __init__(self, page, size, location=(0, 0), border=(0, 0), text="", font_size=13, color="black",
                     background=None):
            self.size = size
            self.border = border
            super().__init__(page, location, text, font_size, color, background)

        def set_size(self, value, update=True):
            self.size = value
            self.update(update)

        def set_border(self, value, update=True):
            self.border = value
            self.update(update)

        def update(self, update=True):
            self.background = Image.new("RGBA", self.size, self._background) if self._background else \
                Image.new("RGBA", self.size, (255, 255, 255, 0))
            self.image = self.background.copy()
            self._image_draw = ImageDraw.ImageDraw(self.image)
            self._image_draw.text(self.border, self.text, self.color, self._font)
            if update:
                self.page.update()

    class Button(Label):
        def __init__(self, page, size, func=lambda: None, location=(0, 0), border=(0, 0), text="", font_size=13,
                     color="black",
                     background=None):
            super().__init__(page, size, location, border, text, font_size, color, background)
            self.func = func
            self.touch_records.append(Clicked((location[0], location[0]+size[0], location[1], location[1]+size[1]),
                                              func))

        def set_func(self, func):
            self.func = func

    class MultipleLinesLabel(Label):
        def __init__(self, page, size, location=(0, 0), border=(0, 0), text="", font_size=13, color="black",
                     background=None, space=0):
            super().__init__(page, size, location, border, text, font_size, color, background)
            self.space = space

        def set_text(self, value, update=True):
            self.text = value.replace("\n", "")
            self.update(update)

        def update(self, update=True):
            line_length = (self.size[0] - 2 * self.border[0]) // self._font.size
            line_num = min(ceil((self.size[1] - 2 * self.border[1]) / self._font.size),
                           ceil((len(self.text) / line_length)))
            new_text = ""
            self.image = self.background.copy()
            self._image_draw = ImageDraw.ImageDraw(self.image)
            for i in range(line_num):
                new_text += f"{self.text[i*line_length: (i+1)*line_length]}\n"
            self._image_draw.text(self.border, new_text, self.color, self._font)
            if update:
                self.page.update()


class Pages:
    class ListPage(_Page):
        def __init__(self, book, title, items: [str], icons=None, funcs=None):
            super().__init__(book)
            self._background = book.base.env.list_img
            self.more_img = book.base.env.list_more_img
            self.old_render = self.background
            self.title = title
            self.items = items
            self.font = book.base.env.get_font(16)
            self.icons = icons if icons else [None] * len(items)
            self.funcs = funcs if funcs else [lambda: None] * len(items)
            self.at = 0
            if not len(items) == len(self.icons) == len(self.funcs):
                raise ValueError("Quantity asymmetry!")
            self.touch_records = [
                Clicked((0, 296, 31, 60), self._handler, 0),
                Clicked((0, 296, 61, 90), self._handler, 1),
                Clicked((0, 296, 91, 120), self._handler, 2),
                SlideY((0, 296, 0, 128), self._slide)
            ]

        def add_element(self, element):
            raise Exception("No support.")

        def append(self, item, icon=None, func=lambda: None, update=True):
            self.items.append(item)
            self.icons.append(icon)
            self.funcs.append(func)
            if update:
                self.update()

        def remove(self, item, update=True):
            for i in range(len(self.items)):
                if self.items[i] == item:
                    del self.items[i]
                    del self.icons[i]
                    del self.funcs[i]
                    self.at = 0
                    break
            else:
                raise ValueError("Item not found!")
            if update:
                self.update()

        def insert(self, index, item, icon=None, func=lambda: None, update=True):
            self.items.insert(index, item)
            self.icons.insert(index, icon)
            self.funcs.insert(index, func)
            if update:
                self.update()

        def clear(self, update=True):
            self.items = []
            self.icons = []
            self.funcs = []
            self.at = 0
            if update:
                self.update()

        def set_items(self, items: [str], icons=None, funcs=None, update=True):
            self.items = items
            self.icons = icons if icons else [None] * len(items)
            self.funcs = funcs if funcs else [lambda: None] * len(items)
            self.at = 0
            if not len(items) == len(self.icons) == len(self.funcs):
                raise ValueError("Quantity asymmetry!")
            if update:
                self.update()

        def _handler(self, index):
            self.funcs[self.at*3+index]()

        def _slide(self, dis):
            if dis < 0:
                self.go_next()
            else:
                self.go_prev()

        def go_next(self):
            if (self.at+2) * 3 - len(self.items) < 3:
                self.at += 1
                self.update()

        def go_prev(self):
            if self.at > 0:
                self.at -= 1
                self.update()

        def render(self):
            if self._update:
                new_image = self.background.copy()
                draw = ImageDraw.ImageDraw(new_image)
                draw.text((10, 8), self.title, "black", self.font)
                draw.text((254, 8), f"{self.at+1}/{ceil(len(self.items)/3)}", "black", self.font)
                for i in range(3):
                    index = self.at * 3 + i
                    if index + 1 > len(self.items):
                        break
                    y = 37 + i * 30
                    if self.icons[index]:
                        new_image.paste(self.icons[index], (8, y))
                        draw.text((35, y+1), self.items[index], "black", self.font)
                    else:
                        draw.text((8, y+1), self.items[index], "black", self.font)
                if self.at * 3 + 3 < len(self.items):
                    new_image.paste(self.more_img, (105, 122))
                self.old_render = new_image
                self._update = False
                return new_image.copy()
            else:
                return self.old_render.copy()


class ThemeBase(_Base):
    def __init__(self, env):
        super().__init__(env)
        self._docker_image = self.env.images.docker_image
        self._docker_status = False

        self._inactive_clicked = [Clicked((0, 296, 0, 30), self.set_docker, True)]
        self._active_clicked = [Clicked((60, 100, 0, 30), self.open_applist),
                                Clicked((0, 296, 30, 128), self.set_docker, False),
                                Clicked((195, 235, 0, 30), self.open_setting)]

    def active(self):
        self._docker_status = False
        super().active()

    def open_applist(self):
        self.env.open_app("应用抽屉")

    def open_setting(self):
        pass

    def set_docker(self, value: bool):
        self._docker_status = value
        self.display()

    def display(self):
        if self._active:
            if self._docker_status:
                new_image = self.Book.Page.render()
                new_image.paste(self._docker_image, (60, 0))
                self.env.Screen.display_auto(new_image)
            else:
                self.env.Screen.display_auto(self.Book.render())

    @property
    def touch_records_clicked(self):
        if self._docker_status:
            return self.Book.Page.touch_records_clicked + self._active_clicked
        else:
            return self.Book.Page.touch_records_clicked + self._inactive_clicked


class AppBase(_Base):
    def __init__(self, env):
        self.title = ""
        self.icon = env.images.None20px
        self.name = ""

        super().__init__(env)

        self._control_bar_font = self.env.get_font(16)
        self._control_bar_image = env.images.app_control
        self._control_bar_status = False
        self._inactive_clicked = [Clicked((266, 296, 0, 30), self.set_control_bar, True)]
        self._active_clicked = [Clicked((266, 296, 0, 30), self.env.back_home),
                                Clicked((0, 296, 30, 128), self.set_control_bar, False)]

    def active(self):
        self._control_bar_status = False
        super().active()

    def display(self):
        if self._active:
            if self._control_bar_status:
                new_image = self.Book.Page.render()
                new_image.paste(self._control_bar_image, (0, 0))
                new_image.paste(self.icon, (6, 6))
                image_draw = ImageDraw.ImageDraw(new_image)
                image_draw.text((30, 7), self.title, fill="black", font=self._control_bar_font)
                image_draw.text((224, 7), time.strftime("%H:%M", time.localtime()), fill="black",
                                font=self._control_bar_font)
                self.env.Screen.display_auto(new_image)
            else:
                self.env.Screen.display_auto(self.Book.render())

    def set_control_bar(self, value: bool):
        self._control_bar_status = value
        self.display()

    @property
    def touch_records_clicked(self):
        if self._control_bar_status:
            return self.Book.Page.touch_records_clicked + self._active_clicked
        else:
            return self.Book.Page.touch_records_clicked + self._inactive_clicked
