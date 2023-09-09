package com.phone.service.impl;

import com.phone.dao.CronDao;
import com.phone.pojo.Cron;
import com.phone.service.CronService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CronServiceImpl implements CronService {

    @Autowired
    CronDao cronDao;

    @Override
    public String getCron() {
        return cronDao.getCron();
    }

    @Override
    public Integer setCron(int id) {
        Cron cron = cronDao.getCronById(id);
        return cronDao.setCron(cron);
    }

    @Override
    public String getDesc(int id) {
        return cronDao.getCronById(id).getDesc();
    }
}
