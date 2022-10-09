#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Logging Receiver with parameters
# Author: WA1CYB
# Description: Logging Receiver ( AM, NBFM, WBFM, USB, LSB )
# GNU Radio version: 3.10.4.0-rc1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, GrRangeWidget
from PyQt5 import QtCore
import logging_receiver_b205_epy_block_0_0 as epy_block_0_0  # embedded python block
import numpy as np
import threading



from gnuradio import qtgui

class logging_receiver_b205(gr.top_block, Qt.QWidget):

    def __init__(self, bw=600, freq_start=433500000, gain_start=77, rcvr_file="log_my_rcvr_gps.csv"):
        gr.top_block.__init__(self, "Logging Receiver with parameters", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Logging Receiver with parameters")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "logging_receiver_b205")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.bw = bw
        self.freq_start = freq_start
        self.gain_start = gain_start
        self.rcvr_file = rcvr_file

        ##################################################
        # Variables
        ##################################################
        self.baseband_rate = baseband_rate = int(24e3)
        self.avg_count = avg_count = 6000*2
        self.volume = volume = 0.1
        self.samp_rate = samp_rate = int(32*48e3)
        self.rit = rit = -811
        self.probe_variable = probe_variable = 0
        self.mode = mode = 4
        self.lsb_taps = lsb_taps = firdes.band_pass(1.0, baseband_rate, 10, 2.5e3, 100, window.WIN_HAMMING, 6.76)
        self.gps_sig_offset = gps_sig_offset = 43.5
        self.gain = gain = gain_start
        self.freq = freq = freq_start*1+462565500*0
        self.avg_count_dB = avg_count_dB = 20*np.log10(avg_count)
        self.audio_rate = audio_rate = int(48000)

        ##################################################
        # Blocks
        ##################################################
        self.probe_signal = blocks.probe_signal_f()
        self._volume_range = Range(0.0, 1.0, 0.025, 0.1, 200)
        self._volume_win = GrRangeWidget(self._volume_range, self.set_volume, "Volume", "counter_slider", float, QtCore.Qt.Horizontal, "value")

        self.top_grid_layout.addWidget(self._volume_win, 0, 3, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rit_range = Range(-5000, 5000, 1, -811, 2000)
        self._rit_win = GrRangeWidget(self._rit_range, self.set_rit, "Linear Fine Tune-Hz", "counter_slider", float, QtCore.Qt.Horizontal, "value")

        self.top_grid_layout.addWidget(self._rit_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        def _probe_variable_probe():
          while True:

            val = self.probe_signal.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_probe_variable,val))
              except AttributeError:
                self.set_probe_variable(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (35))
        _probe_variable_thread = threading.Thread(target=_probe_variable_probe)
        _probe_variable_thread.daemon = True
        _probe_variable_thread.start()
        # Create the options list
        self._mode_options = [0, 1, 2, 3, 4]
        # Create the labels list
        self._mode_labels = ['AM', 'WBFM', 'USB', 'LSB', 'NBFM']
        # Create the combo box
        # Create the radio buttons
        self._mode_group_box = Qt.QGroupBox("Demodulation Type" + ": ")
        self._mode_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._mode_button_group = variable_chooser_button_group()
        self._mode_group_box.setLayout(self._mode_box)
        for i, _label in enumerate(self._mode_labels):
            radio_button = Qt.QRadioButton(_label)
            self._mode_box.addWidget(radio_button)
            self._mode_button_group.addButton(radio_button, i)
        self._mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._mode_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._mode_options.index(i)))
        self._mode_callback(self.mode)
        self._mode_button_group.buttonClicked[int].connect(
            lambda i: self.set_mode(self._mode_options[i]))
        self.top_grid_layout.addWidget(self._mode_group_box, 1, 3, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gps_sig_offset_range = Range(-40, 150, 0.5, 43.5, 2000)
        self._gps_sig_offset_win = GrRangeWidget(self._gps_sig_offset_range, self.set_gps_sig_offset, "Offset for logging in dB", "counter_slider", float, QtCore.Qt.Horizontal, "value")

        self.top_grid_layout.addWidget(self._gps_sig_offset_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = Range(0.0, 49+30, 0.5, gain_start, 200)
        self._gain_win = GrRangeWidget(self._gain_range, self.set_gain, "RX Gain", "counter_slider", float, QtCore.Qt.Horizontal, "value")

        self.top_grid_layout.addWidget(self._gain_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_range = Range(25e6*1+88e6*0, 6e9*1+167e6*0, 100, freq_start*1+462565500*0, 20000)
        self._freq_win = GrRangeWidget(self._freq_range, self.set_freq, "RX Frequency-Hz", "counter_slider", float, QtCore.Qt.Horizontal, "value")

        self.top_grid_layout.addWidget(self._freq_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='find=all',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_subdev_spec('A:A', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.rational_resampler_xxx_5 = filter.rational_resampler_fff(
                interpolation=2,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=2,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            2048, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            (freq+rit), #fc
            samp_rate, #bw
            '', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 7, 0, 1, 4)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_1.set_update_time(0.10)
        self.qtgui_number_sink_1.set_title("")

        labels = ['Log Level (delayed)', '', '', '', '',
            '', '', '', '', '']
        units = ['dB', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "red"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_1.set_min(i, -15)
            self.qtgui_number_sink_1.set_max(i, 115)
            self.qtgui_number_sink_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1.set_label(i, labels[i])
            self.qtgui_number_sink_1.set_unit(i, units[i])
            self.qtgui_number_sink_1.set_factor(i, factor[i])

        self.qtgui_number_sink_1.enable_autoscale(False)
        self._qtgui_number_sink_1_win = sip.wrapinstance(self.qtgui_number_sink_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_1_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title('')

        labels = ['S Meter', 'select out', '', '', '',
            '', '', '', '', '']
        units = ['dB relative', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -174+40)
            self.qtgui_number_sink_0.set_max(i, 0)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(True)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            (samp_rate/4/32), #bw
            "Fine Tune", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



        labels = ['Logging Bandwidth', 'Pre-Filtered Log Input', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_win, 6, 0, 1, 4)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (freq+rit), #fc
            (samp_rate/4), #bw
            "Received Spectrum", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.20)
        self.qtgui_freq_sink_x_0.set_y_axis((-150), (-20))
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['Input', 'Pre-Filtered Log Input', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2, 0, 1, 4)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_1 = qtgui.edit_box_msg(qtgui.STRING, 'Lattitude             Longitude          Signal Level (dB)', 'Add Notes to the file in real time (with Enter Key)', False, True, '', None)
        self._qtgui_edit_box_msg_1_win = sip.wrapinstance(self.qtgui_edit_box_msg_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_1_win, 3, 0, 1, 4)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.low_pass_filter_1 = filter.fir_filter_ccf(
            (int((samp_rate/4)/baseband_rate)),
            firdes.low_pass(
                1,
                (samp_rate/4),
                8e3,
                200,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0_0 = filter.fir_filter_ccf(
            (int(16*2)),
            firdes.low_pass(
                (16*2),
                (samp_rate/4),
                (bw/2),
                (bw/32),
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1.087,
                (samp_rate/4),
                8000,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            (4*1),
            firdes.low_pass(
                1,
                (samp_rate/1),
                100e3,
                10e3,
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccc(1, [1.0], rit, baseband_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, lsb_taps, (-2.5e3), baseband_rate)
        self.epy_block_0_0 = epy_block_0_0.blk(file_name=rcvr_file, Freq=freq, Gain=gain, Offset=gps_sig_offset)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,mode,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(20, 1, (-avg_count_dB))
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, (-132+76))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume)
        self.blocks_integrate_xx_0_0 = blocks.integrate_ff(int(avg_count), 1)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(2500, 1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_1 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(gps_sig_offset)
        self.band_pass_filter_1 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                baseband_rate,
                10,
                2.5e3,
                100,
                window.WIN_HAMMING,
                6.76))
        self.audio_sink_0_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=(samp_rate/4),
        	audio_decimation=(16*1),
        )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=baseband_rate,
        	quad_rate=baseband_rate,
        	tau=(5.305e-4),
        	max_dev=5e3,
          )
        self.analog_const_source_x_1 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, probe_variable)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=baseband_rate,
        	audio_decim=1,
        	audio_pass=5000,
        	audio_stop=5500,
        )
        self.analog_agc_xx_0 = analog.agc_cc((1e-3), 0.300, 1.0)
        self.analog_agc_xx_0.set_max_gain(1.0e10)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0_0, 'clear_input'), (self.qtgui_edit_box_msg_1, 'val'))
        self.msg_connect((self.qtgui_edit_box_msg_1, 'msg'), (self.epy_block_0_0, 'msg_in_attach'))
        self.connect((self.analog_agc_xx_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.analog_const_source_x_1, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_selector_0, 4))
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.band_pass_filter_1, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.epy_block_0_0, 0))
        self.connect((self.blocks_complex_to_mag_1, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.blocks_selector_0, 3))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_5, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.probe_signal, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.epy_block_0_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.epy_block_0_0, 0), (self.qtgui_number_sink_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.band_pass_filter_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.low_pass_filter_0_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.blocks_complex_to_mag_1, 0))
        self.connect((self.low_pass_filter_0_0_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.freq_xlating_fir_filter_xxx_1, 0))
        self.connect((self.low_pass_filter_1, 0), (self.qtgui_freq_sink_x_1, 1))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.rational_resampler_xxx_5, 0), (self.audio_sink_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "logging_receiver_b205")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass((16*2), (self.samp_rate/4), (self.bw/2), (self.bw/32), window.WIN_HAMMING, 6.76))

    def get_freq_start(self):
        return self.freq_start

    def set_freq_start(self, freq_start):
        self.freq_start = freq_start
        self.set_freq(self.freq_start*1+462565500*0)

    def get_gain_start(self):
        return self.gain_start

    def set_gain_start(self, gain_start):
        self.gain_start = gain_start
        self.set_gain(self.gain_start)

    def get_rcvr_file(self):
        return self.rcvr_file

    def set_rcvr_file(self, rcvr_file):
        self.rcvr_file = rcvr_file

    def get_baseband_rate(self):
        return self.baseband_rate

    def set_baseband_rate(self, baseband_rate):
        self.baseband_rate = baseband_rate
        self.set_lsb_taps(firdes.band_pass(1.0, self.baseband_rate, 10, 2.5e3, 100, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_1.set_taps(firdes.complex_band_pass(1, self.baseband_rate, 10, 2.5e3, 100, window.WIN_HAMMING, 6.76))

    def get_avg_count(self):
        return self.avg_count

    def set_avg_count(self, avg_count):
        self.avg_count = avg_count
        self.set_avg_count_dB(20*np.log10(self.avg_count))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, (self.samp_rate/1), 100e3, 10e3, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1.087, (self.samp_rate/4), 8000, 1000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass((16*2), (self.samp_rate/4), (self.bw/2), (self.bw/32), window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, (self.samp_rate/4), 8e3, 200, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range((self.freq+self.rit), (self.samp_rate/4))
        self.qtgui_freq_sink_x_1.set_frequency_range(self.freq, (self.samp_rate/4/32))
        self.qtgui_sink_x_0.set_frequency_range((self.freq+self.rit), self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_rit(self):
        return self.rit

    def set_rit(self, rit):
        self.rit = rit
        self.freq_xlating_fir_filter_xxx_1.set_center_freq(self.rit)
        self.qtgui_freq_sink_x_0.set_frequency_range((self.freq+self.rit), (self.samp_rate/4))
        self.qtgui_sink_x_0.set_frequency_range((self.freq+self.rit), self.samp_rate)

    def get_probe_variable(self):
        return self.probe_variable

    def set_probe_variable(self, probe_variable):
        self.probe_variable = probe_variable
        self.analog_const_source_x_1.set_offset(self.probe_variable)

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
        self._mode_callback(self.mode)
        self.blocks_selector_0.set_input_index(self.mode)

    def get_lsb_taps(self):
        return self.lsb_taps

    def set_lsb_taps(self, lsb_taps):
        self.lsb_taps = lsb_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.lsb_taps)

    def get_gps_sig_offset(self):
        return self.gps_sig_offset

    def set_gps_sig_offset(self, gps_sig_offset):
        self.gps_sig_offset = gps_sig_offset
        self.blocks_add_const_vxx_0.set_k(self.gps_sig_offset)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0.set_frequency_range((self.freq+self.rit), (self.samp_rate/4))
        self.qtgui_freq_sink_x_1.set_frequency_range(self.freq, (self.samp_rate/4/32))
        self.qtgui_sink_x_0.set_frequency_range((self.freq+self.rit), self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_avg_count_dB(self):
        return self.avg_count_dB

    def set_avg_count_dB(self, avg_count_dB):
        self.avg_count_dB = avg_count_dB

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate



def argument_parser():
    description = 'Logging Receiver ( AM, NBFM, WBFM, USB, LSB )'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--bw", dest="bw", type=eng_float, default=eng_notation.num_to_str(float(600)),
        help="Set Sig_Filter_BW [default=%(default)r]")
    parser.add_argument(
        "--freq-start", dest="freq_start", type=eng_float, default=eng_notation.num_to_str(float(433500000)),
        help="Set freq_start [default=%(default)r]")
    parser.add_argument(
        "--gain-start", dest="gain_start", type=eng_float, default=eng_notation.num_to_str(float(77)),
        help="Set gain_start [default=%(default)r]")
    parser.add_argument(
        "--rcvr-file", dest="rcvr_file", type=str, default="log_my_rcvr_gps.csv",
        help="Set log_my_rcvr_gps.csv [default=%(default)r]")
    return parser


def main(top_block_cls=logging_receiver_b205, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(bw=options.bw, freq_start=options.freq_start, gain_start=options.gain_start, rcvr_file=options.rcvr_file)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
