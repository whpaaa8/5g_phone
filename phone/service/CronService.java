package com.phone.service;

import org.springframework.transaction.annotation.Transactional;

@Transactional
public interface CronService {

    public String getCron();

    public Integer setCron(int id);

    public String getDesc(int id);
}
