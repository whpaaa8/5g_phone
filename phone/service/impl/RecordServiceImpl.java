package com.phone.service.impl;

import com.phone.dao.RecordDao;
import com.phone.pojo.Record;
import com.phone.service.RecordService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RecordServiceImpl implements RecordService {

    @Autowired
    RecordDao recordDao;
    @Override
    public Boolean saveRecord(Record record) {
        return recordDao.save(record) > 0;
    }

    @Override
    public List<Record> getRecords() {
        return recordDao.getRecords();
    }
}
