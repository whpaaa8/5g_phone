package com.phone.dao;

import com.phone.pojo.Comment;
import com.phone.pojo.Phone;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface CommentDao {
    @Insert("REPLACE into comment_info (goods_id, comment_id, type, content, username) values (#{goods_id}, #{comment_id}, " +
            "#{type}, #{content}, #{username})")
    public int save(Comment comment);

    @Select("select * from comment_info where goods_id = #{goods_id}")
    public List<Comment> getById(String goods_id);

    @Select("select * from comment_info ")
    public List<Comment> getAll();



}