# *****************************************************************************
# * | File        :	  epd2in9_V2.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-10-20
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# 已被fu1fan修改，勿直接应用于生产环境
import threading
import time

from enviroment.drivers import epdconfig

# Display resolution
EPD_WIDTH = 128
EPD_HEIGHT = 296


class Epd2in9V2:
    def __init__(self):
        self.reset_pin = epdconfig.EPD_RST_PIN
        self.dc_pin = epdconfig.EPD_DC_PIN
        self.busy_pin = epdconfig.EPD_BUSY_PIN
        self.cs_pin = epdconfig.EPD_CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        epdconfig.address = 0x48

    WF_PARTIAL_2IN9 = [
        0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x80, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x40, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0A, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x0, 0x0, 0x0,
        0x22, 0x17, 0x41, 0xB0, 0x32, 0x36,
    ]

    WF_PARTIAL_2IN9_Wait = [
        0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x80, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x40, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0A, 0x0, 0x0, 0x0, 0x0, 0x0, 0x2,
        0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
        0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x0, 0x0, 0x0,
        0x22, 0x17, 0x41, 0xB0, 0x32, 0x36,
    ]

    # Hardware reset
    def reset(self):  # 不建议进行操作
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(20)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(2)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(20)

    def send_command(self, command):  # 不建议进行操作
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):  # 不建议进行操作
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data2(self, data):  # 不建议进行操作
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte2(data)
        epdconfig.digital_write(self.cs_pin, 1)

    def wait_busy(self):  # 等待直到屏幕结束忙碌
        # logging.debug("e-Paper busy")
        while epdconfig.digital_read(self.busy_pin) == 1:  # 0: idle, 1: busy
            epdconfig.delay_ms(0.1)
        # logging.debug("e-Paper busy release")

    def is_busy(self):
        return epdconfig.digital_read(self.busy_pin)

    def turn_on_display(self):  # 不建议进行操作
        self.send_command(0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0xF7)
        self.send_command(0x20)  # MASTER_ACTIVATION
        self.wait_busy()

    def turn_on_display_partial(self):  # 不建议进行操作
        self.send_command(0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0x0F)
        self.send_command(0x20)  # MASTER_ACTIVATION
        # self.ReadBusy()

    def turn_on_display_partial_wait(self):  # 不建议进行操作
        self.send_command(0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0x0F)
        self.send_command(0x20)  # MASTER_ACTIVATION
        self.wait_busy()

    def send_lut(self, lut):  # 不建议进行操作
        self.send_command(0x32)
        # for i in range(0, 153):
        # self.send_data(self.WF_PARTIAL_2IN9[i])
        if lut:
            self.send_data2(self.WF_PARTIAL_2IN9)
        else:
            self.send_data2(self.WF_PARTIAL_2IN9_Wait)
        self.wait_busy()

    def set_window(self, x_start, y_start, x_end, y_end):  # 不建议进行操作
        self.send_command(0x44)  # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x_start >> 3) & 0xFF)
        self.send_data((x_end >> 3) & 0xFF)
        self.send_command(0x45)  # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

    def set_cursor(self, x, y):  # 不建议进行操作
        self.send_command(0x4E)  # SET_RAM_X_ADDRESS_COUNTER
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data(x & 0xFF)

        self.send_command(0x4F)  # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)
        self.wait_busy()

    def init(self):  # 初始化
        if epdconfig.module_init() != 0:
            return -1
        # EPD hardware init start
        self.reset()

        self.wait_busy()
        self.send_command(0x12)  # SWRESET
        self.wait_busy()

        self.send_command(0x01)  # Driver output control
        self.send_data(0x27)
        self.send_data(0x01)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x03)

        self.set_window(0, 0, self.width - 1, self.height - 1)

        self.send_command(0x21)  # Display update control
        self.send_data(0x00)
        self.send_data(0x80)

        self.set_cursor(0, 0)
        self.wait_busy()
        # EPD hardware init end
        return 0

    def get_buffer(self, image):  # 将图片转换为buffer
        # logging.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width / 8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logging.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if imwidth == self.width and imheight == self.height:
            # logging.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif imwidth == self.height and imheight == self.width:
            # logging.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy * self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def display(self, image):  # 显示图片
        if image is None:
            return
        self.send_command(0x24)  # WRITE_RAM
        # for j in range(0, self.height):
        # for i in range(0, int(self.width / 8)):
        # self.send_data(images[i + j * int(self.width / 8)])
        self.send_data2(image)
        self.turn_on_display()

    def display_base(self, image):  # 显示静态底图
        if image is None:
            return

        self.send_command(0x24)  # WRITE_RAM
        # for j in range(0, self.height):
        # for i in range(0, int(self.width / 8)):
        # self.send_data(images[i + j * int(self.width / 8)])
        self.send_data2(image)

        self.send_command(0x26)  # WRITE_RAM
        # for j in range(0, self.height):
        # for i in range(0, int(self.width / 8)):
        # self.send_data(images[i + j * int(self.width / 8)])
        self.send_data2(image)

        self.turn_on_display()

    def display_partial(self, image):  # 局部显示
        if image is None:
            return

        # epdconfig.digital_write(self.reset_pin, 0)
        # epdconfig.delay_ms(2)
        # epdconfig.digital_write(self.reset_pin, 1)
        # epdconfig.delay_ms(2)

        self.send_lut(1)
        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x40)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x3C)  # BorderWavefrom
        self.send_data(0x80)

        self.send_command(0x22)
        self.send_data(0xC0)
        self.send_command(0x20)
        self.wait_busy()

        self.set_window(0, 0, self.width - 1, self.height - 1)
        self.set_cursor(0, 0)

        self.send_command(0x24)  # WRITE_RAM
        # for j in range(0, self.height):
        # for i in range(0, int(self.width / 8)):
        # self.send_data(images[i + j * int(self.width / 8)])
        self.send_data2(image)

        self.turn_on_display_partial()

    def display_partial_wait(self, image):  # 局部显示并等待显示完成
        if image is None:
            return

        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(1)
        epdconfig.digital_write(self.reset_pin, 1)
        # epdconfig.delay_ms(2)

        self.send_lut(0)
        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x40)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x3C)  # BorderWavefrom
        self.send_data(0x80)

        self.send_command(0x22)
        self.send_data(0xC0)
        self.send_command(0x20)
        self.wait_busy()

        self.set_window(0, 0, self.width - 1, self.height - 1)
        self.set_cursor(0, 0)

        self.send_command(0x24)  # WRITE_RAM
        # for j in range(0, self.height):
        # for i in range(0, int(self.width / 8)):
        # self.send_data(images[i + j * int(self.width / 8)])
        self.send_data2(image)

        self.turn_on_display_partial_wait()

    def clear(self, color):  # 清屏
        self.send_command(0x24)  # WRITE_RAM
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(color)
        self.turn_on_display()

    def sleep(self):  # 睡眠模式
        self.send_command(0x10)  # DEEP_SLEEP_MODE
        self.send_data(0x01)

    @staticmethod
    def exit():  # 退出模块
        epdconfig.module_exit()


class Screen:
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self._driver = Epd2in9V2()

        self._driver.init()
        self._last_display = time.time()

        self.auto_sleep_time = 600  # seconds
        self._last_display = 0

        self._partial_time = 0  # times
        self.refresh_time = 60  # times

        self._status = True

        self._exit = False

        def auto_sleep_methode():
            self._last_display = time.time()
            while 1:
                time.sleep(self.auto_sleep_time)
                if self._exit:
                    return
                if time.time() - self._last_display >= self.auto_sleep_time:
                    self._driver.sleep()
                    self._status = False
                    self.logger.info("屏幕休眠")

        self.auto_refresh_thread = threading.Thread(target=auto_sleep_methode, daemon=True)
        self.auto_refresh_thread.start()

    def display_auto(self, image):
        if self.refresh_time > self._partial_time:
            self.display_partial(image)
            self._partial_time += 1
        else:
            self.display(image)

    def display(self, image):
        if not self._status:
            self._driver.init()
            self._status = True
        self._driver.display_base(self._driver.get_buffer(image))
        self._partial_time = 0
        self._last_display = time.time()

    def display_partial(self, image):
        if not self._status:
            self.display(image)
            return
        self._driver.display_partial(self._driver.get_buffer(image))
        self._last_display = time.time()

    def wait_busy(self):
        self._driver.wait_busy()

    def sleep(self):
        self._driver.sleep()
        self._status = False

    def quit(self):
        self._driver.exit()
