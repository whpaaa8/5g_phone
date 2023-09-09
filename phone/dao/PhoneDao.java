package com.phone.dao;

import com.phone.pojo.Phone;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface PhoneDao {
    @Insert("insert into phone_info (goods_id, `desc`, link, img) values (#{goos_id},#{desc},#{link},#{img})")
    public int save(Phone phone);

    @Delete("delete from phone_info where goods_id = #{goods_id}")
    public int delete(String goods_id);

    @Select("select * from phone_info where brand = #{brand}")
    public List<Phone> getByBrand(String brand);

    @Select("select * from phone_info")
    public List<Phone> getAll();

    @Select("select count(*) from phone_info")
    public int getCount();

    @Select("select count(*) from phone_info where goods_id = #{goods_id}  limit 1")
    public int exist(String goods_id);
}
