package com.phone.service;

import com.phone.pojo.Record;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Transactional
public interface RecordService {
    /**
     * 保存更新记录
     * @param record
     * @return
     */
    public Boolean saveRecord(Record record);

    /**
     * 查看更新记录
     * @return
     */
    public List<Record> getRecords();
}
