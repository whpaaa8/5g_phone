package com.phone.pojo;

public class Cron {
    private Integer id;
    private String desc;
    private String cron;

    public Cron(Integer id, String desc, String cron) {
        this.id = id;
        this.desc = desc;
        this.cron = cron;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    public String getCron() {
        return cron;
    }

    public void setCron(String cron) {
        this.cron = cron;
    }
}
