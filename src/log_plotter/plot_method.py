#!/usr/bin/env python
import numpy
import struct
import math
import sys

try:
    import pyqtgraph
except:
    print "please install pyqtgraph. see http://www.pyqtgraph.org/"
    sys.exit(1)

class PlotMethod(object):
    urata_len = 16
    # color_list = pyqtgraph.functions.Colors.keys()
    #            = ['c', 'b', 'd', 'g', 'k', 'm', 'l', 's', 'r', 'w', 'y']
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'd','l', 's']

    @staticmethod
    def __plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, offset1, offset2=1):
        plot_item.plot(times, data_dict[logs[0]][:, (PlotMethod.urata_len+1) * log_cols[0] + (offset1+offset2)],
                       pen=pyqtgraph.mkPen(PlotMethod.color_list[i], width=2), name=key)

    @staticmethod
    def plot_servostate(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        def RePack(x):
            val = struct.unpack('i', struct.pack('f', float(x)))[0]
            #calib = (val & 0x01)
            #servo = (val & 0x02) >> 1
            #power = (val & 0x04) >> 2
            state = (val & 0x0007fff8) >> 3
            #temp  = (val & 0xff000000) >> 24
            return state
        vfr = numpy.vectorize(RePack)
        plot_item.plot(times, vfr(data_dict[logs[0]][:, (PlotMethod.urata_len+1) * log_cols[0] + (0+0)]),
                       pen=pyqtgraph.mkPen('r', width=2), name=key)

    @staticmethod
    def plot_commnormal(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 13)

    @staticmethod
    def plot_12V(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 9)

    @staticmethod
    def plot_80V(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 2)
    
    @staticmethod
    def plot_current(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 1)
    
    @staticmethod
    def plot_motor_temp(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 0)

    @staticmethod
    def plot_motor_outer_temp(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 7)

    @staticmethod
    def plot_pgain(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 10)

    @staticmethod
    def plot_dgain(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 11)

    @staticmethod
    def plot_abs_enc(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, [math.degrees(x) for x in data_dict[logs[0]][:, (PlotMethod.urata_len+1) * log_cols[0] + (6+1)]],
                       pen=pyqtgraph.mkPen('g', width=2), name='abs - enc')

    @staticmethod
    def plot_rh_q_st_q(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, [math.degrees(x) for x in (data_dict[logs[1]][:, log_cols[1]] - data_dict[logs[0]][:, log_cols[0]])],
                       pen=pyqtgraph.mkPen('r', width=2), name=logs[1]+" - rh_q")

    @staticmethod
    def plot_rad2deg(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        data_rad=data_dict[logs[0]][:, log_cols[0]]
        data_deg=[math.degrees(x) for x in data_rad]
        plot_item.plot(times, data_deg,pen=pyqtgraph.mkPen(PlotMethod.color_list[i], width=(len(logs)-0.2*i+2)), name=logs[0])

    @staticmethod
    def plot_watt(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        joint_vel=data_dict[logs[0]][:, log_cols[0]]
        joint_tau=data_dict[logs[1]][:, log_cols[1]]
        watt=joint_vel*joint_tau
        plot_item.plot(times, watt,pen=pyqtgraph.mkPen(PlotMethod.color_list[i], width=len(logs)-i), name=logs[0], fillLevel=0, fillBrush=PlotMethod.color_list[i])

    @staticmethod
    def plot_diff(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        data_minuend = data_dict[logs[0]][:, log_cols[0]]
        data_subtrahend = data_dict[logs[1]][:, log_cols[1]]
        data = data_minuend - data_subtrahend
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.color_list[i], width=len(logs)-i), name=key)

    @staticmethod
    def plot_rad2deg_diff(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, [math.degrees(x) for x in (data_dict[logs[1]][:, log_cols[1]] - data_dict[logs[0]][:, log_cols[0]])],
                       pen=pyqtgraph.mkPen('r', width=2), name=key)

    @staticmethod
    def plot_comp(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, data_dict[logs[0]][:, log_cols[0]],
                      pen=pyqtgraph.mkPen(PlotMethod.color_list[i], width=1+len(logs)-i), name=logs[0])
        if log_cols[0] % 6 < 3: # position
            plot_item.setYRange(-0.025, +0.025) # compensation limit
        else: # rotation
            plot_item.setYRange(math.radians(-10), math.radians(+10)) # compensation limit

    @staticmethod
    def plot_COP(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        offset = log_cols[0]*6
        arg = logs[min(len(logs)-1,cur_col)]
        f_z = data_dict[arg][:, offset+2]
        tau_x = data_dict[arg][:, offset+3]
        tau_y = data_dict[arg][:, offset+4]
        plot_item.plot(times, -tau_y/f_z, pen=pyqtgraph.mkPen(PlotMethod.color_list[2*i], width=2), name=key+"x")
        plot_item.plot(times,  tau_x/f_z, pen=pyqtgraph.mkPen(PlotMethod.color_list[2*i+1], width=2), name=key+"y")

    @staticmethod
    def normal(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, data_dict[logs[0]][:, log_cols[0]], pen=pyqtgraph.mkPen(PlotMethod.color_list[i], width=2), name=key)

    @staticmethod
    def plot_force_in_foot_mid_coords(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        sensor_log_name = logs[0]
        q_log_name = logs[1]
        output_key_name = '{}_world'.format(sensor_log_name) # rmfo_off_lhsensor_world
        generate_world_sensor_by_fk(data_dict, sensor_log_name, q_log_name, output_key_name)
        data = data_dict[output_key_name][:, log_cols[0]]
        plot_item.plot(times, data_dict[output_key_name][:, log_cols[0]], pen=pyqtgraph.mkPen(PlotMethod.color_list[i], width=2), name=key)

    @staticmethod
    def plot_estimated_static_balance_point(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        zmp_name, lhsensor_name, rhsensor_name, q_name, cog_name = logs
        generate_estimated_static_balance_point(data_dict, zmp_name, lhsensor_name, rhsensor_name, q_name, cog_name ,output_key_name='sbp')
        plot_item.plot(times, data_dict['sbp'][:, log_cols[0]], pen=pyqtgraph.mkPen(PlotMethod.color_list[i], width=2), name=key)

def generate_world_sensor_by_fk(data_dict, sensor_log_name, q_log_name, output_key_name=None):
    '''
    :param dict data_dict: ex. {st_q: [[...], [...], ...]}
    :param str sensor_name: ex. rmfo_off_rhsensor
    :param str q_log_name: ex. st_q
    :param str output_key_name: ex. rmfo_off_rhsensor_world
    '''
    if output_key_name is None:
        output_key_name = '{}_world'.format(sensor_log_name)
    import cnoidpy
    from cnoidpy.coordinate import coordinate
    forces = data_dict[sensor_log_name][:, 0:6]
    angle_vectors = data_dict[q_log_name][:, :]
    robot = cnoidpy.hrp2jsknt.instance()
    for sensor_name in ['rhsensor', 'lhsensor', 'rfsensor', 'lfsensor']:
        if sensor_name in sensor_log_name:
            sensor = robot.getDevice(sensor_name)
    if not data_dict.has_key(output_key_name):
        tmp_forces = []
        force_coords = coordinate()
        sensor_coords = coordinate()
        for row_idx, (f, av) in enumerate(zip(forces, angle_vectors)):
            robot.angleVector(av)
            robot.calcForwardKinematics()
            fmc = robot.footMidCoords()
            ff = f[0:3]
            fm = f[3:6]
            sensor_coords.__init__(sensor.position())
            f_world = fmc.inverseRotateVector(sensor_coords.rotateVector(ff))
            m_world = fmc.inverseRotateVector(sensor_coords.rotateVector(fm))
            tmp_forces.append(numpy.r_[f_world, m_world])
        data_dict[output_key_name] = numpy.array(tmp_forces)
        print data_dict

import scipy.constants
def generate_estimated_static_balance_point(data_dict, zmp_name, lhsensor_name, rhsensor_name, q_name, cog_name ,output_key_name=None):
    print 'generate_estimated_static_balance_point'
    import cnoidpy
    from cnoidpy.coordinate import coordinate
    if output_key_name is None:
        output_key_name = 'static balance point'

    generate_world_sensor_by_fk(data_dict, lhsensor_name, q_name)
    generate_world_sensor_by_fk(data_dict, rhsensor_name, q_name)
    lhforces = data_dict['{}_world'.format(lhsensor_name)]
    rhforces = data_dict['{}_world'.format(rhsensor_name)]
    qs = data_dict[q_name]
    cogs = data_dict[cog_name]

    robot = cnoidpy.hrp2jsknt.instance()
    lhsensor = robot.getDevice('lhsensor')
    rhsensor = robot.getDevice('rhsensor')

    if data_dict.has_key(output_key_name):
        return
    estimated_static_balance_point = []
    for i,_ in enumerate(qs):
        lhforce = lhforces[i]
        rhforce = rhforces[i]
        q = qs[i]
        cog = cogs[i]

        # stand on [0,0,0]
        robot.angleVector(q)
        robot.calcForwardKinematics()
        robot.fixLegToCoords(coordinate())
        robot.calcForwardKinematics()

        # hand pos
        lh_pos = lhsensor.position()[0:3,3]
        rh_pos = rhsensor.position()[0:3,3]
        m = robot.mass()
        g = scipy.constants.g

        # static balance point
        sbp_diff = static_balance_point_diff(m, cog, lhforce, lh_pos) + static_balance_point_diff(m, cog, rhforce, rh_pos)
        sbp = cog[0:2] + sbp_diff
        estimated_static_balance_point.append(sbp)
    data_dict[output_key_name] = numpy.array(estimated_static_balance_point)

def static_balance_point_diff(m, m_pos, f, f_pos):
    g = scipy.constants.g
    x = (m*m_pos[0]*g)/(m*g-f[2]) - (f_pos[0]*f[2]-f_pos[2]*f[0])/(m*g-f[2])
    y = (m*m_pos[1]*g)/(m*g-f[2]) - (f_pos[1]*f[2]-f_pos[2]*f[1])/(m*g-f[2])
    return numpy.array([x,y]) - m_pos[0:2]













