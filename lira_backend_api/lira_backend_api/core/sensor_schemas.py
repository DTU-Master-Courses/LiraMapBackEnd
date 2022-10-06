declare module namespace {

    export interface acc.xyz{
        id: string;
        @vid: number;
        start_time_utc: Date;
        end_time_utc: Date;
        @t: string;
        @ts: Date;
        @uid: string;
        @rec: Date;
        acc.xyz.z: number;
        acc.xyz.y: number;
        acc.xyz.x: number;
    }

}

declare module namespace {

    # ec2x.data_usage
    # obd.acc_long
    # obd.acc_trans
    # obd.acc_yaw
    # obd.asr_trq_req_dyn
    # obd.asr_trq_req_st
    # obd.brk_trq_elec
    # obd.brk_trq_req_dvr
    # obd.brk_trq_req_elec
    # obd.cons_avg
    # obd.f_dist
    # obd.msr_trq_req
    # obd.odo
    # obd.rpm_elec
    # obd.rpm_fl
    # obd.rpm_fr
    # obd.rpm_rl
    # obd.rpm_rr
    # obd.sb_rem_fl
    # obd.sb_rem_fr
    # obd.sb_stat_rc
    # obd.sb_stat_rl
    # obd.sb_stat_rr
    # odb.spd
    # odb.spd_veh
    # odb.strg_acc
    # odb.strg_ang
    # odb.strg_pos
    # odb.temp
    # odb.temp_ext
    # odb.time
    # odb.trac_cons
    # odb.trip_cons
    # odb.trip_con_avg
    # odb.trip_dist
    # odb.trip_spd_avg
    # odb.trq_eff
    # odb.trq_req
    # obd.whl_prs_fr
    # odb.whl_prs_rl
    # odb.whl_prs_rr
    # odb.whl_trq_est
    # odb.whl_trq_pot_ri
    # obd.ww_f_req
    # obd.ww_f_stat
    # obd.ww_f_stop


    export interface disk.percent {
        id: string;
        start_time_utc: Date;
        end_time_utc: Date;
        @vid: number;
        @uid: string;
        @ts: Date;
        @t: string;
        @rec: Date;
    }

}

declare module namespace {

    #  event.system.network.wwan0 is the same
    # event.system.sleep_timer.event_driven
    # event.system.sleep_timer.inactivity_after_sleep
    # event.system.sleep_timer.inactivity_fallback
    # event.system.stn
    # event.vehicle.battery
    # event.vehicle.engine
    # event.vehicle.motor
    # event.vehicle.position
    # 
    export interface event.system.device.ec2x.gnss
 {
        id: string;
        @vid: number;
        start_time_utc: Date;
        end_time_utc: Date;
        @tag: string;
        @t: string;
        @ts: Date;
        @uid: string;
        @rec: Date;
    }

}

declare module namespace {

    export interface event.system.power {
        id: string;
        @vid: number;
        start_time_utc: Date;
        end_time_utc: Date;
        @tag: string;
        @t: string;
        @ts: Date;
        @uid: string;
        @rec: Date;
        event.system.power.trigger: string;
    }

}


declare module namespace {

    export interface event.system.time
 {
        id: string;
        @vid: number;
        event.system.time.old: Date;
        start_time_utc: Date;
        end_time_utc: Date;
        @tag: string;
        @t: string;
        event.system.time.source: string;
        @ts: Date;
        @uid: string;
        @rec: Date;
        event.system.time.new: string;
    }

}

declare module namespace {

    export interface obd.bat {
        id: string;
        @vid: number;
        start_time_utc: Date;
        end_time_utc: Date;
        @t: string;
        @ts: Date;
        @uid: string;
        @rec: Date;
        obd.bat.voltage: number;
        obd.bat.state: string;
        obd.bat.level: number;
    }

}

declare module namespace {

    export interface obd.rpm {
        id: string;
        @vid: number;
        start_time_utc: Date;
        end_time_utc: Date;
        @t: string;
        @ts: Date;
        @uid: string;
        @rec: Date;
        obd.rpm.value: number;
    }

}

declare module namespace {
    # obd.whl_prs_rl

    export interface odb.whl_prs_fl {
        id: string;
        start_time_utc: Date;
        end_time_utc: Date;
        @vid: number;
        @uid: string;
        @ts: Date;
        @t: string;
        @rec: Date;
        obd.whl_prs_fl.value: number;
    }

}

declare module namespace {

    export interface RpiTempCpu {
        value: number;
        unit: string;
    }

    export interface RpiTempGpu {
        value: number;
        unit: string;
    }

    export interface rpi.temp {
        id: string;
        @vid: number;
        start_time_utc: Date;
        end_time_utc: Date;
        @t: string;
        @ts: Date;
        @uid: string;
        @rec: Date;
        rpi.temp.cpu: RpiTempCpu;
        rpi.temp.gpu: RpiTempGpu;
    }

}

declare module namespace {

    export interface TrackPosLoc {
        lat: number;
        lon: number;
    }

    export interface TrackPos {
        id: string;
        @vid: number;
        start_time_utc: Date;
        end_time_utc: Date;
        @t: string;
        @ts: Date;
        @uid: string;
        @rec: Date;
        track.pos.utc: Date;
        track.pos.cog: number;
        track.pos.nsat: number;
        track.pos.alt: number;
        track.pos.sog: number;
        track.pos.loc: TrackPosLoc;
    }

}

