package com.phone.dao;

import com.phone.pojo.Cron;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface CronDao {
    /**
     * 获取第一个id，即更新用的
     * @return
     */
    @Select("select cron from cron where id = 1")
    public String getCron();

    /**
     * 更新更新方式
     * @param id
     * @return
     */
    @Select("select * from cron where id = #{id}")
    public Cron getCronById(int id);

    @Update("update cron set cron = #{cron},`desc` = #{desc} where id = 1")
    public Integer setCron(Cron cron);

}
