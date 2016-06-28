#!/usr/bin/env python

import argparse
import csv
import functools
import math
import multiprocessing
import numpy
import struct
import sys
import time
import yaml
import plot_method

try:
    import pyqtgraph
except:
    print "please install pyqtgraph. see http://www.pyqtgraph.org/"
    sys.exit(1)


# decorator for time measurement
def my_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print("start : " + func.func_name)
        result = func(*args, **kwargs)
        print('{0:>10} : {1:3.3f} [s]'.format(func.func_name,
                                              time.time() - start))
        return result
    return wrapper


# seems that we should declare global function for multiprocess
def readOneTopic(fname):
    tmp = []
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            dl = filter(lambda x: x != '', row)
            tmp.append([float(x) for x in dl])
    return numpy.array(tmp)


class DataloggerLogParser:
    def __init__(self, fname, plot_conf_name, layout_conf_name, title):
        self.fname = fname
        with open(plot_conf_name, "r") as f:
            self.plot_dict = yaml.load(f)
        with open(layout_conf_name, "r") as f:
            self.layout_list = yaml.load(f)
        # setup view
        self.view = pyqtgraph.GraphicsLayoutWidget()
        self.view.setBackground('w')
        self.view.setWindowTitle(title if title else fname.split('/')[-1])
        # self.dateListDict is set by self.readData()
        self.dataListDict = {}# todo: to list of dictionary
        # back up for plot items
        self.plotItemOrig = {}

    @my_time
    def readData(self):
        '''
        read log data from log files and store dataListDict
        # self.dataListDict[topic] = numpy.array([[t_0, x_0, y_0, ...],
        #                                         [t_1, x_1, y_1, ...],
        #                                         ...,
        #                                         [t_n, x_n, y_n, ...]])
        '''
        logs_list_list = [plot_conf[1]["log"] for plot_conf in self.plot_dict.items()]
        duplicated_list = [log for logs_list in logs_list_list for logs in logs_list for log in logs ]
        topic_list = list(set(duplicated_list))
        # store data in parallel
        fname_list = [self.fname+'.'+ext for ext in topic_list]
        pl = multiprocessing.Pool()
        data_list = pl.map(readOneTopic, fname_list)
        for topic, data in zip(topic_list, data_list):
            self.dataListDict[topic] = data
        # set the fastest time as 0
        min_time = min([self.dataListDict[topic][0][0] for topic in topic_list])
        for topic in topic_list:
            raw_time = self.dataListDict[topic][:, 0]
            self.dataListDict[topic][:, 0] = [x - min_time for x in raw_time]
        # fix servoState
        if 'RobotHardware0_servoState' in topic_list:
            def servoStatesConverter(x):
                return struct.unpack('f', struct.pack('i', int(x)))[0]
            vf = numpy.vectorize(servoStatesConverter)
            ss_tmp = self.dataListDict['RobotHardware0_servoState'][:, 1:]
            self.dataListDict['RobotHardware0_servoState'][:, 1:] = vf(ss_tmp)

    @my_time
    def setLayout(self):
        '''
        set layout of view according to self.plot_dict
        '''
        for x in self.layout_list:
            for i in range(len(x["indices"][0])):
                self.view.addPlot()
            self.view.nextRow()

    @my_time
    def plotData(self):
        '''
        plot
        '''
        color_list = pyqtgraph.functions.Colors.keys()
        cur_row = 0
        plot = None
        for row_layout in self.layout_list: # plot : ('joint_velocity', {'field':[[0,1],[2,3]], 'log':['rh_q', 'st_q']}) (loop of rows)
            if row_layout.has_key("group"):
                title = row_layout["group"]
                plot = self.plot_dict[title]
            assert plot != None
            indices_list = row_layout['indices']  # [[0,1,2,3],[4,5,6,7]]
            args_list = plot['log']      # [['sh_qOut'],['rh_q', 'st_q']]
            if plot.has_key('key'): key_list = plot['key']
            else: key_list = [args[0] for args in args_list]
            if plot.has_key('func'): func_list = plot['func']
            else: func_list = ['normal' for x in range(len(args_list))]
            arg_index_list = plot['arg_index']
            log_list = list(set(reduce(lambda x,y: x + y, args_list)))
            data_dict = {}
            for log in log_list: data_dict[log] = self.dataListDict[log][:, 1:]
            times = self.dataListDict[log_list[0]][:, 0]

            for cur_col, index in enumerate(indices_list[0]): # index : 0,1,2,3  (loop of plot areas)
                cur_item = self.view.ci.rows[cur_row][cur_col]
                cur_item.setTitle(title+" "+str(index))
                cur_item.showGrid(x=True, y=True)

                for i, (args, key, func, arg_indices) in enumerate(zip(args_list, key_list, func_list, arg_index_list)): # args : ['sh_qOut'], ['rh_q', 'st_q']  (loop of keys)
                    if i == 0: # we should call addLegend once a plot item
                        cur_item.addLegend(offset=(0, 0))
                    # plot
                    if args[0] == 'RobotHardware0_servoState':
                        urata_len = 16
                        if title == "ServoState":
                            getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)
                            # def RePack(x):
                            #     val = struct.unpack('i', struct.pack('f', float(x)))[0]
                            #     #calib = (val & 0x01)
                            #     #servo = (val & 0x02) >> 1
                            #     #power = (val & 0x04) >> 2
                            #     state = (val & 0x0007fff8) >> 3
                            #     #temp  = (val & 0xff000000) >> 24
                            #     return state
                            # vfr = numpy.vectorize(RePack)
                            # cur_item.plot(times, vfr(data_dict[args[0]][:, (urata_len+1) * index + (0+0)]),
                            #               pen=pyqtgraph.mkPen('r', width=2), name='ServoState')
                        if title == "CommNormal":
                            getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)
                            # cur_item.plot(times, data_dict[args[0]][:, (urata_len+1) * index + (13+1)],
                            #               pen=pyqtgraph.mkPen('r', width=2), name='CommNormal')
                        if title == "12V":
                            getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)
                            # cur_item.plot(times, data_dict[args[0]][:, (urata_len+1) * index + (9+1)],
                            #               pen=pyqtgraph.mkPen('r', width=2), name='12V')
                        elif title == "80V":
                            getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)
                            # cur_item.plot(times, data_dict[args[0]][:, (urata_len+1) * index + (2+1)],
                            #               pen=pyqtgraph.mkPen('g', width=2), name='80V')
                        elif title == "current":
                            getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)
                            # cur_item.plot(times, data_dict[args[0]][:, (urata_len+1) * index + (1+1)],
                            #               pen=pyqtgraph.mkPen('b', width=2), name='current')
                        elif title == "temperature":
                            getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)# fast
                            # getattr(DataloggerLogParser.plot_method, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)# fast
                        #     if key == "motor_temp":
                        #         cur_item.plot(times, data_dict[args[0]][:, (urata_len+1) * indices_list[arg_indices[0]][cur_col] + (0+1)],
                        #                       pen=pyqtgraph.mkPen(color_list[i], width=1), name=key)
                        #     else:
                        #         cur_item.plot(times, data_dict[args[0]][:, (urata_len+1) * indices_list[arg_indices[0]][cur_col] + (7+1)],
                        #                       pen=pyqtgraph.mkPen(color_list[i], width=1), name=key)
                        elif title == "tracking":
                            getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)
                            # cur_item.plot(times, [math.degrees(x) for x in data_dict[args[0]][:, (urata_len+1) * index + (6+1)]],
                            #               pen=pyqtgraph.mkPen('g', width=2), name='abs - enc')
                    elif title == "tracking":
                        if args[0] == "RobotHardware0_q":
                            getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)
                            # cur_item.plot(times, [math.degrees(x) for x in (data_dict[args[1]][:, index] - data_dict[args[0]][:, index])],
                            #               pen=pyqtgraph.mkPen('r', width=2), name=args[1]+" - rh_q")
                        else:
                            pass
                    elif title == "joint_angle" or title == "joint_velocity" or title == "attitude":
                        getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)
                        # cur_item.plot(times, [math.degrees(x) for x in data_dict[args[0]][:, index]],
                        #               pen=pyqtgraph.mkPen(color_list[i], width=len(args_list)-i), name=args[0])
                    elif title == "watt":
                        getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)
                        # if args[0] == "RobotHardware0_dq":
                        #     cur_item.plot(times, [math.degrees(x) for x in data_dict[args[1]][:, index] * data_dict[args[0]][:, index]],
                        #                   pen=pyqtgraph.mkPen(color_list[i], width=len(args_list)-i), name=args[0], fillLevel=0, fillBrush=color_list[i])
                        # else:
                        #     pass
                    elif title == "imu":
                        mod3 = index % 3
                        if args[0] == 'RobotHardware0_gsensor':
                            self.view.ci.rows[cur_row][0].plot(times, data_dict[args[0]][:, index],
                                                               pen=pyqtgraph.mkPen(color_list[mod3], width=3-mod3), name=['x', 'y', 'z'][mod3])
                        elif args[0] == 'RobotHardware0_gyrometer':
                            self.view.ci.rows[cur_row][1].plot(times, data_dict[args[0]][:, index],
                                                               pen=pyqtgraph.mkPen(color_list[mod3], width=3-mod3), name=['x', 'y', 'z'][mod3])
                    elif title == "comp":
                        cur_item.plot(times, data_dict[args[0]][:, index],
                                      pen=pyqtgraph.mkPen(color_list[i], width=len(args_list)-i), name=args[0])
                        if index % 6 < 3: # position
                            cur_item.setYRange(-0.025, +0.025) # compensation limit
                        else: # rotation
                            cur_item.setYRange(math.radians(-10), math.radians(+10)) # compensation limit
                    else:
                        getattr(plot_method.PlotMethod, func)(cur_item, times, data_dict, args, indices_list, arg_indices, cur_col, key, i)

            # increase current row
            cur_row = cur_row + 1

    @my_time
    def setLabel(self):
        '''
        set label: time for bottom plots, unit for left plots
        '''
        row_num = len(self.view.ci.rows)
        # left plot items
        for i in range(row_num):
            cur_item = self.view.ci.rows[i][0]
            title = cur_item.titleLabel.text
            tmp_units = None
            if ("12V" in title) or ("80V" in title):
                tmp_units = "V"
            elif "current" in title:
                tmp_units = "A"
            elif ("temperature" in title) or ("joint_angle" in title) or ("attitude" in title) or ("tracking" in title):
                tmp_units = "deg"
            elif ("joint_velocity" in title):
                tmp_units = "deg/s"
            elif ("watt" in title):
                tmp_units = "W"
            cur_item.setLabel("left", text="", units=tmp_units)
            # we need this to suppress si-prefix until https://github.com/pyqtgraph/pyqtgraph/pull/293 is merged
            for ax in cur_item.axes.values():
                ax['item'].enableAutoSIPrefix(enable=False)
                ax['item'].autoSIPrefixScale = 1.0
                ax['item'].labelUnitPrefix = ''
                ax['item'].setLabel()
        # bottom plot items
        col_num = len(self.view.ci.rows[row_num-1])
        for i in range(col_num):
            cur_item = self.view.ci.rows[row_num-1][i]
            cur_item.setLabel("bottom", text="time", units="s")

    @my_time
    def linkAxes(self):
        '''
        link all X axes and some Y axes
        '''
        # X axis
        all_items = self.view.ci.items.keys()
        target_item = all_items[0]
        for i, p in enumerate(all_items):
            if i != 0:
                p.setXLink(target_item)
            else:
                p.enableAutoRange()
        # Y axis
        for cur_row_dict in self.view.ci.rows.values():
            all_items = cur_row_dict.values()
            target_item = all_items[0]
            title = target_item.titleLabel.text
            if title.find("joint_angle") == -1 and title.find("_force") == -1 and title != "imu" and title.find("comp") == -1:
                y_min = min([ci.viewRange()[1][0] for ci in all_items])
                y_max = max([ci.viewRange()[1][1] for ci in all_items])
                target_item.setYRange(y_min, y_max)
                for i, p in enumerate(all_items):
                    if i != 0:
                        p.setYLink(target_item)

    @my_time
    def customMenu(self):
        '''
        customize right-click context menu
        '''
        self.plotItemOrig = self.view.ci.items.copy()
        all_items = self.view.ci.items.keys()
        for pi in all_items:
            vb = pi.getViewBox()
            hm = vb.menu.addMenu('Hide')
            qa1 = hm.addAction('hide this plot')
            qa2 = hm.addAction('hide this row')
            qa3 = hm.addAction('hide this column')
            qa4 = vb.menu.addAction('restore plots')
            qa5 = hm.addAction('hide except this plot')
            qa6 = hm.addAction('hide except this row')
            def hideCB(item):
                self.view.ci.removeItem(item)
            def hideRowCB(item):
                r, _c = self.view.ci.items[item][0]
                del_list = [self.view.ci.rows[r][c] for c in self.view.ci.rows[r].keys()]
                for i in del_list:
                    self.view.ci.removeItem(i)
            def hideColCB(item):
                _r, c = self.view.ci.items[item][0]
                del_list = []
                row_num = len(self.view.ci.rows)
                for r in range(row_num):
                    if c in self.view.ci.rows[r].keys():
                        del_list.append(self.view.ci.rows[r][c])
                for i in del_list:
                    self.view.ci.removeItem(i)
            def hideExcCB(item):
                del_list = self.view.ci.items.keys()
                del_list.remove(item)
                for i in del_list:
                    self.view.ci.removeItem(i)
            def hideExcRowCB(item):
                del_list = self.view.ci.items.keys()
                r, _c = self.view.ci.items[item][0]
                not_del_list=[self.view.ci.rows[r][c] for c in self.view.ci.rows[r].keys()]
                for i in self.view.ci.items.keys():
                    tmp_r, tmp_c = self.view.ci.items[i][0]
                    if i in not_del_list:
                        del_list.remove(i)
                for i in del_list:
                    tmp_r, tmp_c = self.view.ci.items[i][0]
                    self.view.ci.removeItem(i)
            def restoreCB():
                self.view.ci.clear()
                for key in self.plotItemOrig:
                    r, c = self.plotItemOrig[key][0]
                    self.view.ci.addItem(key, row=r, col=c)
            qa1.triggered.connect(functools.partial(hideCB, pi))
            qa2.triggered.connect(functools.partial(hideRowCB, pi))
            qa3.triggered.connect(functools.partial(hideColCB, pi))
            qa4.triggered.connect(restoreCB)
            qa5.triggered.connect(functools.partial(hideExcCB, pi))
            qa6.triggered.connect(functools.partial(hideExcRowCB, pi))

    def main(self):
        '''
        1. read log files
        2. decide layout
        3. plot data
        4. set label
        5. link axes
        6. customize context menu
        7. show
        '''
        self.readData()
        self.setLayout()
        self.plotData()
        self.setLabel()
        self.linkAxes()
        self.customMenu()
        self.view.showMaximized()

if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser(description='plot data from hrpsys log')
    parser.add_argument('-f', type=str, help='input file', metavar='file', required=False)
    parser.add_argument('--plot', type=str, help='plot configure file', metavar='file', required=False)
    parser.add_argument('--layout', type=str, help='layout configure file', metavar='file', required=False)
    parser.add_argument('-t', type=str, help='title', default=None)
    parser.set_defaults(feature=False)
    args = parser.parse_args()
    # main
    app = pyqtgraph.Qt.QtGui.QApplication([])
    fileName="jaxon_test_data/skate-log_JAXON_20151216220552"
    plotName="config/robot/jaxon/test.yaml"
    layoutName="config/robot/jaxon/test-layout.yaml"
    a = DataloggerLogParser(fileName, plotName, layoutName, args.t)
    a.main()
    # pyqtgraph.Qt.QtGui.QApplication.instance().exec_()
