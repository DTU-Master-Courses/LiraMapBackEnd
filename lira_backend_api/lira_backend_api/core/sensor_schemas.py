from pydantic import BaseModel
from datetime import datetime


class AccXyz(BaseModel):
    id: str
    # @vid: int
    vid: int
    # ISO 8601 Format
    start_time_utc: datetime
    end_time_utc: datetime
    # @t: str
    # @ts: datetime
    # @uid: str
    # @rec: datetime
    t: str
    ts: datetime
    uid: str
    rec: datetime
    acc_xyz_z: float
    acc_xyz_y: float
    acc_xyz_x: float

    # ec2x_data_usage
    # obd_acc_long
    # obd_acc_trans
    # obd_acc_yaw
    # obd_asr_trq_req_dyn
    # obd_asr_trq_req_st
    # obd_brk_trq_elec
    # obd_brk_trq_req_dvr
    # obd_brk_trq_req_elec
    # obd_cons_avg
    # obd_f_dist
    # obd_msr_trq_req
    # obd_odo
    # obd_rpm_elec
    # obd_rpm_fl
    # obd_rpm_fr
    # obd_rpm_rl
    # obd_rpm_rr
    # obd_sb_rem_fl
    # obd_sb_rem_fr
    # obd_sb_stat_rc
    # obd_sb_stat_rl
    # obd_sb_stat_rr
    # odb_spd
    # odb_spd_veh
    # odb_strg_acc
    # odb_strg_ang
    # odb_strg_pos
    # odb_temp
    # odb_temp_ext
    # odb_time
    # odb_trac_cons
    # odb_trip_cons
    # odb_trip_con_avg
    # odb_trip_dist
    # odb_trip_spd_avg
    # odb_trq_eff
    # odb_trq_req
    # obd_whl_prs_fr
    # odb_whl_prs_rl
    # odb_whl_prs_rr
    # odb_whl_trq_est
    # odb_whl_trq_pot_ri
    # obd_ww_f_req
    # obd_ww_f_stat
    # obd_ww_f_stop
    # disk_percent


class Something1(BaseModel):
    id: str
    start_time_utc: datetime
    end_time_utc: datetime
    vid: int
    uid: str
    ts: datetime
    t: str
    rec: datetime
    # @vid: int
    # @uid: str
    # @ts: datetime
    # @t: str
    # @rec: datetime

    # event_system_network_wwan0 is the same
    # event_system_sleep_timer_event_driven
    # event_system_sleep_timer_inactivity_after_sleep
    # event_system_sleep_timer_inactivity_fallback
    # event_system_stn
    # event_vehicle_battery
    # event_vehicle_engine
    # event_vehicle_motor
    # event_vehicle_position
    # event_system_device_ec2x_gnss


class Something2(BaseModel):
    id: str
    start_time_utc: datetime
    end_time_utc: datetime
    vid: int
    tag: str
    t: str
    ts: datetime
    uid: str
    rec: datetime
    # @vid: int
    # @tag: str
    # @t: str
    # @ts: datetime
    # @uid: str
    # @rec: datetime


class EventSystemPower(BaseModel):
    id: str
    start_time_utc: datetime
    end_time_utc: datetime
    # @vid: int
    # @tag: str
    # @t: str
    # @ts: datetime
    # @uid: str
    # @rec: datetime
    vid: int
    tag: str
    t: str
    ts: datetime
    uid: str
    rec: datetime
    event_system_power_trigger: str


class EventSystemTime(BaseModel):
    id: str
    event_system_time_old: datetime
    start_time_utc: datetime
    end_time_utc: datetime
    vid: int
    tag: str
    t: str
    ts: datetime
    uid: str
    rec: datetime
    # @vid: int
    # @tag: str
    # @t: str
    # @ts: datetime
    # @uid: str
    # @rec: datetime
    event_system_time_source: str
    event_system_time_new: str


class OdbBat(BaseModel):
    id: str
    start_time_utc: datetime
    end_time_utc: datetime
    vid: int
    t: str
    ts: datetime
    uid: str
    rec: datetime
    # @vid: int
    # @t: str
    # @ts: datetime
    # @uid: str
    # @rec: datetime
    obd_bat_voltage: float
    obd_bat_state: str
    obd_bat_level: int


class OdbRpm(BaseModel):
    id: str
    start_time_utc: datetime
    end_time_utc: datetime
    vid: int
    t: str
    ts: datetime
    uid: str
    rec: datetime
    # @vid: int
    # @t: str
    # @ts: datetime
    # @uid: str
    # @rec: datetime
    obd_rpm_value: float

    # obd_whl_prs_rl
    # odb_whl_prs_fl


class OdbWhlPrsFl(BaseModel):
    id: str
    start_time_utc: datetime
    end_time_utc: datetime
    vid: int
    uid: str
    ts: datetime
    t: str
    rec: datetime
    # @vid: int
    # @uid: str
    # @ts: datetime
    # @t: str
    # @rec: datetime
    obd_whl_prs_fl_value: float


class RpiTempCpu(BaseModel):
    value: float
    unit: str


class RpiTempGpu(BaseModel):
    value: float
    unit: str


class RpiTemp(BaseModel):
    id: str
    start_time_utc: datetime
    end_time_utc: datetime
    vid: int
    t: str
    ts: datetime
    uid: str
    rec: datetime
    # @vid: int
    # @t: str
    # @ts: datetime
    # @uid: str
    # @rec: datetime
    rpi_temp_cpu: RpiTempCpu
    rpi_temp_gpu: RpiTempGpu


class TrackPosLoc(BaseModel):
    lat: float
    lon: float


class TrackPos(BaseModel):
    id: str
    start_time_utc: datetime
    end_time_utc: datetime
    vid: int
    t: str
    ts: datetime
    uid: str
    rec: datetime
    # @vid: int
    # @t: str
    # @ts: datetime
    # @uid: str
    # @rec: datetime
    track_pos_utc: datetime
    track_pos_cog: float
    track_pos_nsat: float
    track_pos_alt: float
    track_pos_sog: float
    track_pos_loc: TrackPosLoc
