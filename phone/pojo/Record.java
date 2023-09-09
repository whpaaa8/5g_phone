package com.phone.pojo;

import java.sql.Timestamp;

public class Record {
    private Integer id;
    private Timestamp update_time;
    private String update_type;

    @Override
    public String toString() {
        return "Record{" +
                "id=" + id +
                ", update_time=" + update_time +
                ", update_type='" + update_type + '\'' +
                '}';
    }

    public Record(Timestamp update_time, String update_type) {
        this.update_time = update_time;
        this.update_type = update_type;
    }

    public Record(Integer id, Timestamp update_time, String update_type) {
        this.id = id;
        this.update_time = update_time;
        this.update_type = update_type;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Timestamp getUpdate_time() {
        return update_time;
    }

    public void setUpdate_time(Timestamp update_time) {
        this.update_time = update_time;
    }

    public String getUpdate_type() {
        return update_type;
    }

    public void setUpdate_type(String update_type) {
        this.update_type = update_type;
    }
}
