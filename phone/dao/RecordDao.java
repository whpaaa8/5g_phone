package com.phone.dao;

import com.phone.pojo.Record;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface RecordDao {

    @Insert("insert into update_record (update_time, update_type) values (#{update_time},#{update_type})")
    public Integer save(Record record);

    @Select("select * from update_record")
    public List<Record> getRecords();
}
