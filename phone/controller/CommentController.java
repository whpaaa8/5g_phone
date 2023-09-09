package com.phone.controller;

import com.phone.controller.pojo.Code;
import com.phone.controller.pojo.Result;
import com.phone.pojo.Comment;
import com.phone.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("comments")
public class CommentController {
    @Autowired
    private CommentService commentService;

    @GetMapping("{id}")
    @CrossOrigin
    public Result getById(@PathVariable String id)
    {
        List<Comment> comments = commentService.getById(id);
        if (comments.isEmpty()) return new Result(Code.GET_ERR,"该商品没有评论！");
        List<Comment> pos_comments = comments.stream().filter(comment -> comment.getType().equals("好评")).collect(Collectors.toList());
        List<Comment> neu_comments = comments.stream().filter(comment -> comment.getType().equals("中评")).collect(Collectors.toList());
        List<Comment> neg_comments = comments.stream().filter(comment -> comment.getType().equals("差评")).collect(Collectors.toList());
        Map<String, List<Comment>> map = new HashMap<>();
        map.put("好评", pos_comments);
        map.put("中评", neu_comments);
        map.put("差评", neg_comments);
        return new Result(Code.GET_OK,map,"获取成功！");
    }

    @PostMapping
    @CrossOrigin
    public Result save(@RequestBody Comment comment)
    {
        Boolean flag = commentService.save(comment);
        if (flag) return new Result(Code.SAVE_OK,"保存评论成功！");
        else return  new Result(Code.SAVE_ERR,"保存评论失败！");
    }


}
