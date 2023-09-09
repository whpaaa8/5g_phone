package com.phone.service.impl;

import com.phone.dao.CommentDao;
import com.phone.pojo.Comment;
import com.phone.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CommentServiceImpl implements CommentService {
    @Autowired
    private CommentDao commentDao;
    @Override
    public Boolean save(Comment comment) {
        int result = commentDao.save(comment);
        return result > 0;
    }

    @Override
    public Boolean batchSave(List<Comment> comments) {
        int result = 0;
        for (Comment c:comments)
        {
            commentDao.save(c);
        }
        return result > 0;
    }

    @Override
    public List<Comment> getById(String goods_id) {
        return commentDao.getById(goods_id);
    }

    @Override
    public List<Comment> getAll() {
        return commentDao.getAll();
    }
}
