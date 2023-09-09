package com.phone.service;

import com.phone.pojo.Comment;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Transactional
public interface CommentService {
    /***
     * 保存评论数据
     * @param comment
     * @return
     */
    public Boolean save(Comment comment);

    /***
     * 批量保存数据
     * @param comments
     * @return
     */
    public Boolean batchSave(List<Comment> comments);

    /***
     * 获取某手机评论
     * @param goods_id
     * @return
     */
    public List<Comment> getById(String goods_id);

    /***
     * 获取所有评论
     * @return
     */
    public  List<Comment> getAll();

}
